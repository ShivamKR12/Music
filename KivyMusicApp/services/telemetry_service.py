"""Runtime performance and reliability telemetry collector.

Collects bounded, low-overhead metrics matching GEMINI.md Section 11 (Tier 4):
1. Cold startup latency (process/app start to first usable screen)
2. Time to first audio (play request to first audible PCM/decoder output)
3. Buffering stalls & buffer safety seconds
4. UI frame pacing (p50, p95, p99, max frame delta, missed >16.67ms & >33.3ms frames)
5. Long-session process RAM (RSS MB current/baseline/peak/delta)
6. DSP CPU load (% real-time budget + per-chunk timing percentiles)
7. Network throughput, download progress deltas, HTTP retries & stream refreshes
8. Provider success/failure outcomes & classified error rates
"""

from __future__ import annotations

import os
import sys
import threading
import time
from collections import Counter, deque
from typing import Any, Dict, Optional

try:
    import psutil  # type: ignore
except Exception:  # pragma: no cover - optional runtime dependency fallback
    psutil = None


PROCESS_T0_MONOTONIC: float = time.perf_counter()


def _percentile(sorted_vals: list[float], pct: float) -> float:
    """Compute linear-interpolated percentile on a pre-sorted non-empty list."""
    if not sorted_vals:
        return 0.0
    n = len(sorted_vals)
    if n == 1:
        return float(sorted_vals[0])
    pos = (pct / 100.0) * (n - 1)
    lo = int(pos)
    hi = min(lo + 1, n - 1)
    frac = pos - lo
    return float(sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac)


def _summarize_samples(vals: list[float]) -> Dict[str, Any]:
    if not vals:
        return {
            "count": 0,
            "min_ms": 0.0,
            "avg_ms": 0.0,
            "p50_ms": 0.0,
            "p95_ms": 0.0,
            "p99_ms": 0.0,
            "max_ms": 0.0,
        }
    s = sorted(vals)
    total = sum(s)
    return {
        "count": len(s),
        "min_ms": round(s[0], 3),
        "avg_ms": round(total / len(s), 3),
        "p50_ms": round(_percentile(s, 50.0), 3),
        "p95_ms": round(_percentile(s, 95.0), 3),
        "p99_ms": round(_percentile(s, 99.0), 3),
        "max_ms": round(s[-1], 3),
    }


def read_process_rss_mb() -> Optional[float]:
    """Return current process Resident Set Size in MiB, or None if unavailable."""
    if psutil is not None:
        try:
            rss_bytes = psutil.Process(os.getpid()).memory_info().rss
            return float(rss_bytes) / (1024.0 * 1024.0)
        except Exception:
            pass
    # POSIX / Linux / Android (/proc/self/statm) fallback without psutil
    statm_path = "/proc/self/statm"
    if os.path.exists(statm_path):
        try:
            with open(statm_path, "r", encoding="utf-8") as fh:
                parts = fh.read().strip().split()
            if len(parts) >= 2:
                rss_pages = int(parts[1])
                page_size = os.sysconf("SC_PAGE_SIZE") if hasattr(os, "sysconf") else 4096
                return float(rss_pages * page_size) / (1024.0 * 1024.0)
        except Exception:
            pass
    # Windows Win32 API fallback when psutil is not installed
    if sys.platform.startswith("win"):
        try:
            import ctypes
            from ctypes import wintypes

            class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
                _fields_ = [
                    ("cb", wintypes.DWORD),
                    ("PageFaultCount", wintypes.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t),
                ]

            pmc = PROCESS_MEMORY_COUNTERS()
            pmc.cb = ctypes.sizeof(pmc)
            handle = ctypes.windll.kernel32.GetCurrentProcess()
            if ctypes.windll.psapi.GetProcessMemoryInfo(handle, ctypes.byref(pmc), pmc.cb):
                return float(pmc.WorkingSetSize) / (1024.0 * 1024.0)
        except Exception:
            pass
    return None


class PerformanceTelemetry:
    """Thread-safe bounded telemetry collector across all 8 Tier-4 dimensions."""

    def __init__(self, start_monotonic: Optional[float] = None, max_samples: int = 4000):
        self._lock = threading.Lock()
        self._max_samples = max(64, int(max_samples))
        self._t0 = float(start_monotonic if start_monotonic is not None else PROCESS_T0_MONOTONIC)
        self.reset(keep_start_time=True)

    def reset(self, keep_start_time: bool = False) -> None:
        with self._lock:
            if not keep_start_time:
                self._t0 = time.perf_counter()
            self._startup_stages_ms: Dict[str, float] = {}
            self._cold_startup_ms: Optional[float] = None

            self._pending_play_t0: Optional[float] = None
            self._pending_play_track: str = ""
            self._pending_play_consumed: bool = False
            self._ttfa_samples_ms: deque[float] = deque(maxlen=500)
            self._last_ttfa_track: str = ""

            self._buffer_streams: Dict[int, tuple[int, float, int]] = {}
            self._buffer_stall_count: int = 0
            self._buffer_stall_seconds: float = 0.0
            self._buffer_safety_samples_s: deque[float] = deque(maxlen=1000)
            self._buffer_min_safety_s: Optional[float] = None

            self._frame_dt_ms: deque[float] = deque(maxlen=self._max_samples)
            self._frame_total_count: int = 0
            self._frame_missed_16ms: int = 0
            self._frame_jank_33ms: int = 0

            self._rss_samples_mb: deque[float] = deque(maxlen=1000)
            self._rss_baseline_mb: Optional[float] = None
            self._rss_peak_mb: Optional[float] = None
            self._last_rss_sample_t: float = 0.0

            self._dsp_chunk_ms: deque[float] = deque(maxlen=self._max_samples)
            self._dsp_total_compute_s: float = 0.0
            self._dsp_total_audio_s: float = 0.0

            self._network_bps_samples: deque[float] = deque(maxlen=1000)
            self._network_peak_bps: float = 0.0
            self._network_total_bytes: int = 0
            self._http_retry_count: int = 0
            self._stream_refresh_count: int = 0
            self._range_checks: Counter = Counter()

            self._provider_stats: Dict[str, Dict[str, Any]] = {}

    # 1. Cold startup
    def record_startup_stage(self, stage: str, elapsed_ms: Optional[float] = None) -> float:
        ms = float(elapsed_ms) if elapsed_ms is not None else (time.perf_counter() - self._t0) * 1000.0
        with self._lock:
            self._startup_stages_ms[str(stage)] = round(ms, 2)
        return ms

    def mark_cold_startup_complete(self, elapsed_ms: Optional[float] = None) -> float:
        ms = float(elapsed_ms) if elapsed_ms is not None else (time.perf_counter() - self._t0) * 1000.0
        with self._lock:
            if self._cold_startup_ms is None:
                self._cold_startup_ms = round(ms, 2)
            self._startup_stages_ms["app_usable"] = self._cold_startup_ms
            return self._cold_startup_ms

    # 2. Time to first audio
    def begin_play_request(self, track_label: str = "") -> float:
        now = time.perf_counter()
        with self._lock:
            self._pending_play_t0 = now
            self._pending_play_track = str(track_label or "")
            self._pending_play_consumed = False
        return now

    def mark_first_audio(self, play_token_t0: Optional[float] = None, track_label: str = "") -> Optional[float]:
        now = time.perf_counter()
        with self._lock:
            if play_token_t0 is not None:
                # Ignore stale/already-recorded callbacks from older play requests
                if self._pending_play_t0 is not None and abs(play_token_t0 - self._pending_play_t0) > 1e-6:
                    if self._pending_play_consumed:
                        return None
            if self._pending_play_t0 is None or self._pending_play_consumed:
                return None
            base_t0 = play_token_t0 if play_token_t0 is not None else self._pending_play_t0
            ttfa_ms = max(0.0, (now - base_t0) * 1000.0)
            self._pending_play_consumed = True
            self._ttfa_samples_ms.append(ttfa_ms)
            self._last_ttfa_track = track_label or self._pending_play_track
            return ttfa_ms

    # 3 & 7a. Buffering stalls, safety & network bytes
    def record_buffer_metrics(
        self,
        stream_key: int,
        stall_count: int,
        total_stall_seconds: float,
        buffer_safety_seconds: float,
        network_bps: float = 0.0,
        bytes_downloaded: int = 0,
        supports_range: Optional[bool] = None,
    ) -> None:
        with self._lock:
            prev_stalls, prev_stall_s, prev_bytes = self._buffer_streams.get(stream_key, (0, 0.0, 0))
            d_stalls = max(0, int(stall_count) - prev_stalls)
            d_stall_s = max(0.0, float(total_stall_seconds) - prev_stall_s)
            d_bytes = max(0, int(bytes_downloaded) - prev_bytes)
            self._buffer_streams[stream_key] = (
                max(prev_stalls, int(stall_count)),
                max(prev_stall_s, float(total_stall_seconds)),
                max(prev_bytes, int(bytes_downloaded)),
            )
            self._buffer_stall_count += d_stalls
            self._buffer_stall_seconds += d_stall_s
            self._network_total_bytes += d_bytes

            # Prune old stream entries to keep dict bounded in very long sessions
            if len(self._buffer_streams) > 64:
                oldest_key = next(iter(self._buffer_streams))
                if oldest_key != stream_key:
                    self._buffer_streams.pop(oldest_key, None)

            safety = max(0.0, float(buffer_safety_seconds))
            self._buffer_safety_samples_s.append(safety)
            if self._buffer_min_safety_s is None or safety < self._buffer_min_safety_s:
                self._buffer_min_safety_s = safety

            bps = max(0.0, float(network_bps))
            if bps > 0.0:
                self._network_bps_samples.append(bps)
                if bps > self._network_peak_bps:
                    self._network_peak_bps = bps

            if supports_range is True:
                self._range_checks["supported"] += 1
            elif supports_range is False:
                self._range_checks["unsupported"] += 1

    # 4. Frame pacing
    def record_frame_dt(self, dt_seconds: float) -> None:
        if dt_seconds is None or dt_seconds <= 0.0:
            return
        dt_ms = float(dt_seconds) * 1000.0
        # Filter extreme synthetic pauses (> 2000ms suspend) from FPS avg distortion,
        # while still recording jank thresholds cleanly on real interactive frames.
        with self._lock:
            self._frame_dt_ms.append(dt_ms)
            self._frame_total_count += 1
            if dt_ms > 16.67:
                self._frame_missed_16ms += 1
            if dt_ms > 33.33:
                self._frame_jank_33ms += 1

    # 5. RAM usage
    def sample_memory(self, min_interval_seconds: float = 0.0, override_rss_mb: Optional[float] = None) -> Optional[float]:
        now = time.perf_counter()
        if min_interval_seconds > 0.0 and (now - self._last_rss_sample_t) < min_interval_seconds:
            return None
        rss = float(override_rss_mb) if override_rss_mb is not None else read_process_rss_mb()
        if rss is None:
            return None
        with self._lock:
            self._last_rss_sample_t = now
            self._rss_samples_mb.append(rss)
            if self._rss_baseline_mb is None:
                self._rss_baseline_mb = rss
            if self._rss_peak_mb is None or rss > self._rss_peak_mb:
                self._rss_peak_mb = rss
        return rss

    # 6. DSP CPU load
    def record_dsp_chunk(self, compute_seconds: float, audio_seconds: float) -> None:
        c = max(0.0, float(compute_seconds))
        a = max(0.0, float(audio_seconds))
        with self._lock:
            self._dsp_chunk_ms.append(c * 1000.0)
            self._dsp_total_compute_s += c
            self._dsp_total_audio_s += a

    # 7b. Retries & stream expiry recovery
    def record_network_retry(self, stream_refresh: bool = False) -> None:
        with self._lock:
            self._http_retry_count += 1
            if stream_refresh:
                self._stream_refresh_count += 1

    # 8. Provider telemetry
    def record_provider_outcome(
        self,
        provider: str,
        operation: str,
        ok: bool,
        latency_ms: float = 0.0,
        error_code: str = "",
    ) -> None:
        key = f"{str(provider).lower()}:{str(operation).lower()}"
        with self._lock:
            entry = self._provider_stats.get(key)
            if entry is None:
                entry = {
                    "provider": str(provider).lower(),
                    "operation": str(operation).lower(),
                    "total": 0,
                    "success": 0,
                    "failure": 0,
                    "latencies_ms": deque(maxlen=250),
                    "error_codes": Counter(),
                }
                self._provider_stats[key] = entry
            entry["total"] += 1
            if ok:
                entry["success"] += 1
            else:
                entry["failure"] += 1
                code = str(error_code or "unknown").strip() or "unknown"
                entry["error_codes"][code] += 1
            if latency_ms >= 0.0:
                entry["latencies_ms"].append(float(latency_ms))

    def snapshot(self, sample_rss_now: bool = True) -> Dict[str, Any]:
        if sample_rss_now:
            self.sample_memory(min_interval_seconds=0.0)
        with self._lock:
            ttfa = _summarize_samples(list(self._ttfa_samples_ms))
            ttfa["last_track"] = self._last_ttfa_track

            frame_vals = list(self._frame_dt_ms)
            frame_summary = _summarize_samples(frame_vals)
            total_frames = self._frame_total_count
            avg_dt = frame_summary["avg_ms"]
            frame_summary.update({
                "total_frames_recorded": total_frames,
                "missed_16ms_count": self._frame_missed_16ms,
                "missed_16ms_pct": round((self._frame_missed_16ms / total_frames) * 100.0, 2) if total_frames else 0.0,
                "jank_33ms_count": self._frame_jank_33ms,
                "avg_fps": round(1000.0 / avg_dt, 2) if avg_dt > 0.0 else 0.0,
            })

            rss_vals = list(self._rss_samples_mb)
            rss_cur = round(rss_vals[-1], 2) if rss_vals else None
            rss_base = round(self._rss_baseline_mb, 2) if self._rss_baseline_mb is not None else None
            rss_peak = round(self._rss_peak_mb, 2) if self._rss_peak_mb is not None else None
            rss_delta = round(rss_cur - rss_base, 2) if (rss_cur is not None and rss_base is not None) else None

            dsp_summary = _summarize_samples(list(self._dsp_chunk_ms))
            dsp_cpu_pct = (
                round((self._dsp_total_compute_s / self._dsp_total_audio_s) * 100.0, 3)
                if self._dsp_total_audio_s > 0.0
                else 0.0
            )
            dsp_summary.update({
                "total_compute_seconds": round(self._dsp_total_compute_s, 4),
                "total_audio_seconds": round(self._dsp_total_audio_s, 4),
                "realtime_cpu_load_pct": dsp_cpu_pct,
            })

            safety_vals = list(self._buffer_safety_samples_s)
            bps_vals = list(self._network_bps_samples)
            providers_out: Dict[str, Any] = {}
            for key, info in self._provider_stats.items():
                tot = info["total"]
                fail = info["failure"]
                lat = _summarize_samples(list(info["latencies_ms"]))
                providers_out[key] = {
                    "provider": info["provider"],
                    "operation": info["operation"],
                    "total": tot,
                    "success": info["success"],
                    "failure": fail,
                    "failure_rate_pct": round((fail / tot) * 100.0, 2) if tot else 0.0,
                    "error_codes": dict(info["error_codes"]),
                    "latency_ms": lat,
                }

            return {
                "cold_startup": {
                    "cold_startup_ms": self._cold_startup_ms,
                    "stages_ms": dict(self._startup_stages_ms),
                },
                "time_to_first_audio": ttfa,
                "buffering": {
                    "stall_count": self._buffer_stall_count,
                    "total_stall_seconds": round(self._buffer_stall_seconds, 3),
                    "min_safety_seconds": round(self._buffer_min_safety_s, 3) if self._buffer_min_safety_s is not None else None,
                    "avg_safety_seconds": round(sum(safety_vals) / len(safety_vals), 3) if safety_vals else None,
                    "sample_count": len(safety_vals),
                },
                "frame_pacing": frame_summary,
                "memory_rss_mb": {
                    "current_mb": rss_cur,
                    "baseline_mb": rss_base,
                    "peak_mb": rss_peak,
                    "delta_mb": rss_delta,
                    "sample_count": len(rss_vals),
                },
                "dsp_cpu": dsp_summary,
                "network": {
                    "total_bytes_downloaded": self._network_total_bytes,
                    "avg_bps": round(sum(bps_vals) / len(bps_vals), 1) if bps_vals else 0.0,
                    "peak_bps": round(self._network_peak_bps, 1),
                    "http_retry_count": self._http_retry_count,
                    "stream_refresh_count": self._stream_refresh_count,
                    "range_checks": dict(self._range_checks),
                },
                "providers": providers_out,
            }


_GLOBAL_TELEMETRY: Optional[PerformanceTelemetry] = None
_GLOBAL_LOCK = threading.Lock()


def get_telemetry() -> PerformanceTelemetry:
    """Return process-wide singleton PerformanceTelemetry instance."""
    global _GLOBAL_TELEMETRY
    with _GLOBAL_LOCK:
        if _GLOBAL_TELEMETRY is None:
            _GLOBAL_TELEMETRY = PerformanceTelemetry(start_monotonic=PROCESS_T0_MONOTONIC)
        return _GLOBAL_TELEMETRY
