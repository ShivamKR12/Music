"""
Progressive Streaming & Atomic Download Buffer Manager (Priority 2 Subsystem).

Separates streaming state and buffer metrics cleanly from AudioEngine:
- Distinct states: IDLE -> PROBING -> BUFFERING -> READY -> STREAMING -> COMPLETED | FAILED | CANCELLED
- Tracks three independent telemetry metrics:
  1. download_progress:       bytes_downloaded / total_bytes
  2. playable_buffer_seconds: decodable seconds buffered cleanly
  3. buffer_safety_seconds:   seconds of playable audio strictly ahead of the playhead
- Atomic cache promotion (.part -> final file): never opens a growing file alongside
  a destructive postprocessor delete, and never reports completion until validated.
"""

import os
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

import requests

from services.logger import get_logger
from services.telemetry_service import get_telemetry
from services.youtube_extractor import redact_sensitive_text
from utils.local_audio_utils import parse_audio_duration

logger = get_logger("BufferManager")


class _HTTPStatusError(RuntimeError):
    def __init__(self, status_code: int, message: str = ""):
        self.status_code = int(status_code)
        super().__init__(message or f"HTTP {status_code}")


class BufferState:
    IDLE = "IDLE"
    PROBING = "PROBING"
    BUFFERING = "BUFFERING"
    READY = "READY"
    STREAMING = "STREAMING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass
class BufferMetrics:
    state: str = BufferState.IDLE
    bytes_downloaded: int = 0
    total_bytes: int = 0
    download_progress: float = 0.0
    playable_buffer_seconds: float = 0.0
    buffer_safety_seconds: float = 0.0
    estimated_bitrate_bps: int = 128000
    supports_range: bool = False
    stall_count: int = 0
    total_stall_seconds: float = 0.0
    network_bps: float = 0.0
    error_message: str = ""


def is_valid_audio_header(path: str) -> bool:
    """Verify minimum size and recognized container/codec header before playback or promotion."""
    try:
        if not path or not os.path.exists(path) or not os.path.isfile(path):
            return False
        if os.path.getsize(path) < 1024:
            return False
        with open(path, "rb") as f:
            header = f.read(64)
        if len(header) < 32:
            return False
        if header[:3] == b"ID3":
            return True
        if header[0] == 0xFF and (header[1] & 0xE0) == 0xE0:
            return True
        if header[:4] == b"OggS" or header[:4] == b"fLaC":
            return True
        if header[:4] == b"RIFF" and b"WAVE" in header[:16]:
            return True
        if b"ftyp" in header[:16] or b"moov" in header[:16]:
            return True
        # EBML/WebM container (Opus/Vorbis from YouTube WebM audio streams)
        if header[:4] == b"\x1a\x45\xdf\xa3":
            return True
        return False
    except Exception:
        return False


class BufferManager:
    """Manages HTTP Range-aware progressive caching and real playback buffer telemetry."""

    def __init__(
        self,
        min_buffer_seconds: float = 3.5,
        assumed_bitrate_bps: int = 128000,
    ):
        self.min_buffer_seconds = float(min_buffer_seconds)
        self.metrics = BufferMetrics(estimated_bitrate_bps=int(assumed_bitrate_bps))
        self._lock = threading.RLock()
        self._playhead_seconds: float = 0.0
        self._stall_started_at: Optional[float] = None
        self.on_metrics_update: Optional[Callable[[BufferMetrics], None]] = None

    def reset(self, duration: float = 0.0, bitrate_bps: int = 128000) -> None:
        with self._lock:
            self._playhead_seconds = 0.0
            self._stall_started_at = None
            self.metrics = BufferMetrics(
                state=BufferState.IDLE,
                estimated_bitrate_bps=max(16000, int(bitrate_bps or 128000)),
            )
            self._expected_duration = max(0.0, float(duration or 0.0))

    def set_state(self, new_state: str, error_message: str = "") -> None:
        with self._lock:
            self.metrics.state = new_state
            if error_message:
                self.metrics.error_message = error_message
        self._emit()

    def update_playhead(self, playhead_seconds: float, decoder_stalled: bool = False) -> BufferMetrics:
        """Update current playhead and track stalls + safety margin ahead of playhead."""
        now = time.monotonic()
        with self._lock:
            self._playhead_seconds = max(0.0, float(playhead_seconds or 0.0))
            self.metrics.buffer_safety_seconds = max(
                0.0, self.metrics.playable_buffer_seconds - self._playhead_seconds
            )
            if decoder_stalled and self._stall_started_at is None:
                self._stall_started_at = now
                self.metrics.stall_count += 1
            elif not decoder_stalled and self._stall_started_at is not None:
                self.metrics.total_stall_seconds += max(0.0, now - self._stall_started_at)
                self._stall_started_at = None
            snapshot = BufferMetrics(**self.metrics.__dict__)
        return snapshot

    def update_download_progress(
        self,
        bytes_downloaded: int,
        total_bytes: int = 0,
        duration_hint: float = 0.0,
        network_bps: float = 0.0,
    ) -> BufferMetrics:
        """Compute byte progress plus honest playable buffer & safety seconds."""
        with self._lock:
            self.metrics.bytes_downloaded = max(0, int(bytes_downloaded))
            if total_bytes > 0:
                self.metrics.total_bytes = int(total_bytes)
            tot = self.metrics.total_bytes

            if tot > 0:
                self.metrics.download_progress = max(0.0, min(1.0, self.metrics.bytes_downloaded / float(tot)))
            else:
                self.metrics.download_progress = 0.0

            dur = float(duration_hint or getattr(self, "_expected_duration", 0.0) or 0.0)
            if dur > 0 and tot > 0:
                playable = dur * (self.metrics.bytes_downloaded / float(tot))
            else:
                bytes_per_sec = max(2000.0, self.metrics.estimated_bitrate_bps / 8.0)
                playable = self.metrics.bytes_downloaded / bytes_per_sec

            self.metrics.playable_buffer_seconds = playable
            self.metrics.buffer_safety_seconds = max(0.0, playable - self._playhead_seconds)
            if network_bps > 0:
                self.metrics.network_bps = float(network_bps)

            if self.metrics.state == BufferState.BUFFERING:
                if self.metrics.buffer_safety_seconds >= self.min_buffer_seconds or (tot > 0 and self.metrics.bytes_downloaded >= tot):
                    self.metrics.state = BufferState.READY

            snapshot = BufferMetrics(**self.metrics.__dict__)
        self._emit()
        return snapshot

    def mark_completed(self, final_path: str, duration: float = 0.0) -> BufferMetrics:
        """Mark download and local cache completion only after final file is verified."""
        with self._lock:
            size = os.path.getsize(final_path) if os.path.exists(final_path) else self.metrics.bytes_downloaded
            actual_dur = float(duration or parse_audio_duration(final_path) or getattr(self, "_expected_duration", 0.0) or 0.0)
            self.metrics.bytes_downloaded = size
            self.metrics.total_bytes = max(self.metrics.total_bytes, size)
            self.metrics.download_progress = 1.0
            if actual_dur > 0:
                self.metrics.playable_buffer_seconds = actual_dur
                self.metrics.buffer_safety_seconds = max(0.0, actual_dur - self._playhead_seconds)
            self.metrics.state = BufferState.COMPLETED
            snapshot = BufferMetrics(**self.metrics.__dict__)
        self._emit()
        return snapshot

    def _emit(self) -> None:
        if self.on_metrics_update:
            with self._lock:
                snap = BufferMetrics(**self.metrics.__dict__)
            self.on_metrics_update(snap)

    def download_http_stream(
        self,
        stream_url: str,
        final_path: str,
        cancel_event: threading.Event,
        duration_hint: float = 0.0,
        bitrate_bps: int = 128000,
        http_headers: Optional[Dict[str, str]] = None,
        on_ready_to_play: Optional[Callable[[str], None]] = None,
        on_completed: Optional[Callable[[str, BufferMetrics], None]] = None,
        on_error: Optional[Callable[[str], None]] = None,
        on_refresh_stream: Optional[Callable[[], Optional[str]]] = None,
        max_retries: int = 2,
    ) -> bool:
        """
        Resilient chunked HTTP downloader supporting Range resumption, expired stream
        URL refresh callbacks (on 403/410), and atomic `.part -> final_path` promotion.
        """
        part_path = f"{final_path}.part"
        self.reset(duration=duration_hint, bitrate_bps=bitrate_bps)
        self.set_state(BufferState.PROBING)
        base_headers: Dict[str, str] = dict(http_headers or {})

        # Probe content-length and byte-range support (with optional refresh on 403/410)
        total_len = 0
        supports_range = False
        refreshed_probe = False
        for _ in range(2):
            try:
                head_resp = requests.head(stream_url, headers=base_headers, allow_redirects=True, timeout=10)
                if head_resp.status_code < 400:
                    total_len = int(head_resp.headers.get("content-length", 0) or 0)
                    supports_range = "bytes" in (head_resp.headers.get("accept-ranges", "").lower())
                    break
                if head_resp.status_code in (403, 410) and on_refresh_stream and not refreshed_probe:
                    refreshed_probe = True
                    fresh = on_refresh_stream()
                    if fresh:
                        stream_url = fresh
                        continue
                break
            except Exception:
                break

        with self._lock:
            self.metrics.total_bytes = total_len
            self.metrics.supports_range = supports_range
            self.metrics.state = BufferState.BUFFERING
        self._emit()

        dl_bytes = os.path.getsize(part_path) if (supports_range and os.path.exists(part_path)) else 0
        if not supports_range and os.path.exists(part_path):
            try:
                os.remove(part_path)
            except Exception:
                pass
            dl_bytes = 0

        notified_ready = False
        attempt = 0
        t_start = time.monotonic()

        while attempt <= max_retries:
            if cancel_event.is_set():
                self.set_state(BufferState.CANCELLED)
                return False

            headers: Dict[str, str] = dict(base_headers)
            mode = "wb"
            if dl_bytes > 0 and supports_range:
                headers["Range"] = f"bytes={dl_bytes}-"
                mode = "ab"
            elif dl_bytes > 0:
                dl_bytes = 0

            try:
                with requests.get(stream_url, headers=headers, stream=True, timeout=15) as resp:
                    if resp.status_code not in (200, 206):
                        raise _HTTPStatusError(resp.status_code)
                    if resp.status_code == 200:
                        dl_bytes = 0
                        mode = "wb"
                        total_len = int(resp.headers.get("content-length", 0) or total_len or 0)
                    elif resp.status_code == 206 and not total_len:
                        cr = resp.headers.get("content-range", "")
                        if "/" in cr:
                            tail = cr.split("/")[-1]
                            if tail.isdigit():
                                total_len = int(tail)

                    with open(part_path, mode) as out_f:
                        for chunk in resp.iter_content(chunk_size=65536):
                            if cancel_event.is_set():
                                self.set_state(BufferState.CANCELLED)
                                return False
                            if not chunk:
                                continue
                            out_f.write(chunk)
                            out_f.flush()
                            dl_bytes += len(chunk)
                            dt = max(0.05, time.monotonic() - t_start)
                            bps = (dl_bytes * 8.0) / dt
                            snap = self.update_download_progress(
                                dl_bytes,
                                total_bytes=total_len,
                                duration_hint=duration_hint,
                                network_bps=bps,
                            )
                            if (not notified_ready) and snap.state == BufferState.READY and is_valid_audio_header(part_path):
                                notified_ready = True
                                self.set_state(BufferState.STREAMING)
                                if on_ready_to_play:
                                    on_ready_to_play(part_path)

                # Verify completeness if content-length known
                if total_len > 0 and dl_bytes < total_len:
                    raise IOError(f"Incomplete HTTP body ({dl_bytes}/{total_len} bytes)")

                if not is_valid_audio_header(part_path):
                    raise ValueError("Downloaded stream failed audio container validation")

                os.replace(part_path, final_path)
                done_metrics = self.mark_completed(final_path, duration=duration_hint)
                if on_completed:
                    on_completed(final_path, done_metrics)
                return True

            except Exception as exc:
                attempt += 1
                safe_exc = redact_sensitive_text(exc)
                logger.warning("HTTP stream attempt %d failed: %s", attempt, safe_exc)
                refreshed = False
                if isinstance(exc, _HTTPStatusError) and exc.status_code in (403, 410) and on_refresh_stream and attempt <= max_retries:
                    try:
                        fresh = on_refresh_stream()
                        if fresh:
                            logger.info("Refreshed expired HTTP stream URL cleanly (HTTP %d)", exc.status_code)
                            stream_url = fresh
                            refreshed = True
                            if not supports_range and os.path.exists(part_path):
                                try:
                                    os.remove(part_path)
                                except Exception:
                                    pass
                                dl_bytes = 0
                    except Exception as ref_exc:
                        logger.warning("Stream refresh hook failed: %s", redact_sensitive_text(ref_exc))
                get_telemetry().record_network_retry(stream_refresh=refreshed)
                if attempt > max_retries:
                    if not notified_ready and os.path.exists(part_path):
                        try:
                            os.remove(part_path)
                        except Exception:
                            pass
                    self.set_state(BufferState.FAILED, safe_exc)
                    if on_error and not cancel_event.is_set():
                        on_error(f"Stream download failed: {safe_exc}")
                    return False
                backoff = min(2.0, 0.4 * (2 ** (attempt - 1)))
                if cancel_event.wait(timeout=backoff):
                    self.set_state(BufferState.CANCELLED)
                    return False

        return False
