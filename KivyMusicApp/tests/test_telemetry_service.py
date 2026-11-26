"""Priority 7 Telemetry Service Unit & Headless Integration Verification.

Covers:
1. Unit: Percentile & frame pacing stats (p50/p95/p99, missed 16.67ms & 33.33ms frames),
   bounded ring buffer limits, multi-thread write safety, and DSP real-time CPU load math.
2. Unit: TTFA single-consumption token semantics, multi-stream BufferManager delta tracking
   without double-counting, RSS reader availability, and provider error taxonomy counters.
3. Integration: Real `AudioEngine` local WAV playback exercising `DecoderManager`, `DSPPipeline`
   (10-band EQ + reverb), PCM output, TTFA recording, and DSP compute telemetry.
4. Integration: Real `BufferManager` HTTP stream retry/stall counters & `YouTubeExtractor`
   error-code failure tracking without live network dependency.
"""

import io
import math
import os
import struct
import sys
import tempfile
import threading
import time
import wave
from unittest.mock import patch

os.environ["KIVY_HEADLESS"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from services.telemetry_service import PerformanceTelemetry, get_telemetry, read_process_rss_mb
from services.audio_engine import AudioEngine
from services.buffer_manager import BufferManager, BufferState
from services.youtube_extractor import YouTubeExtractor, ExtractionErrorCode, YouTubeExtractionError


def _write_test_wav(path: str, duration_s: float = 0.6, sr: int = 44100, freq: float = 440.0) -> None:
    n_frames = int(duration_s * sr)
    frames = bytearray()
    for i in range(n_frames):
        val = int(12000.0 * math.sin(2.0 * math.pi * freq * (i / float(sr))))
        frames.extend(struct.pack("<hh", val, val))
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(bytes(frames))


def test_unit_percentiles_frame_pacing_and_thread_safety():
    t = PerformanceTelemetry(start_monotonic=time.perf_counter() - 0.5, max_samples=500)
    t.record_startup_stage("build_done", 120.0)
    cold = t.mark_cold_startup_complete(415.5)
    assert cold == 415.5, cold

    # Record 100 frames: 90 smooth (~10ms), 7 borderline (~20ms), 3 janky (>33.33ms)
    for _ in range(90):
        t.record_frame_dt(0.010)
    for _ in range(7):
        t.record_frame_dt(0.020)
    for _ in range(3):
        t.record_frame_dt(0.045)

    # DSP load: 0.05s compute for 5.0s audio => 1.0% realtime CPU load
    for _ in range(10):
        t.record_dsp_chunk(0.005, 0.5)

    # Concurrent ring writes from multiple threads must remain bounded & crash-free
    def worker():
        for _ in range(250):
            t.record_frame_dt(0.012)

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for th in threads:
        th.start()
    for th in threads:
        th.join(timeout=5.0)

    snap = t.snapshot(sample_rss_now=True)
    fp = snap["frame_pacing"]
    assert fp["total_frames_recorded"] == 1100, fp
    assert fp["count"] == 500, fp  # bounded maxlen honored
    assert fp["missed_16ms_count"] == 10, fp
    assert fp["jank_33ms_count"] == 3, fp
    assert fp["p95_ms"] <= fp["p99_ms"] <= fp["max_ms"], fp

    dsp = snap["dsp_cpu"]
    assert abs(dsp["realtime_cpu_load_pct"] - 1.0) < 0.01, dsp
    rss = snap["memory_rss_mb"]
    assert rss["current_mb"] is not None and rss["current_mb"] > 5.0, rss
    assert read_process_rss_mb() is not None
    print("[PASS] Unit: percentiles, bounded frame ring, DSP CPU %, RSS reader")


def test_unit_ttfa_buffer_deltas_and_provider_counters():
    t = PerformanceTelemetry()

    # Stale token vs active token
    tok1 = t.begin_play_request("Track A")
    time.sleep(0.01)
    tok2 = t.begin_play_request("Track B")
    time.sleep(0.015)
    ms2 = t.mark_first_audio(tok2, "Track B")
    assert ms2 is not None and ms2 >= 10.0, ms2
    assert t.mark_first_audio(tok2, "Track B") is None  # single consumption
    assert t.mark_first_audio(tok1, "Track A") is None  # consumed active token blocks stale

    # Repeated ticks on stream 1 should NOT double count cumulative stalls or bytes
    t.record_buffer_metrics(stream_key=1, stall_count=1, total_stall_seconds=0.8, buffer_safety_seconds=2.5, network_bps=400_000, bytes_downloaded=50_000, supports_range=True)
    t.record_buffer_metrics(stream_key=1, stall_count=1, total_stall_seconds=0.8, buffer_safety_seconds=4.5, network_bps=800_000, bytes_downloaded=120_000)
    # New stream 2 adds its own stalls & bytes cleanly
    t.record_buffer_metrics(stream_key=2, stall_count=2, total_stall_seconds=1.2, buffer_safety_seconds=1.0, network_bps=600_000, bytes_downloaded=80_000, supports_range=False)

    t.record_network_retry(stream_refresh=False)
    t.record_network_retry(stream_refresh=True)

    t.record_provider_outcome("jiosaavn", "search", True, 85.0)
    t.record_provider_outcome("jiosaavn", "search", False, 300.0, "timeout")

    snap = t.snapshot(sample_rss_now=False)
    assert snap["buffering"]["stall_count"] == 3, snap["buffering"]
    assert abs(snap["buffering"]["total_stall_seconds"] - 2.0) < 0.01, snap["buffering"]
    assert abs(snap["buffering"]["min_safety_seconds"] - 1.0) < 0.01, snap["buffering"]
    assert snap["network"]["total_bytes_downloaded"] == 200_000, snap["network"]
    assert snap["network"]["http_retry_count"] == 2, snap["network"]
    assert snap["network"]["stream_refresh_count"] == 1, snap["network"]
    assert snap["providers"]["jiosaavn:search"]["failure_rate_pct"] == 50.0, snap["providers"]
    assert snap["providers"]["jiosaavn:search"]["error_codes"]["timeout"] == 1
    print("[PASS] Unit: TTFA token arbitration, buffer deltas, retries, provider counters")


def test_integration_audio_engine_pcm_telemetry():
    telem = get_telemetry()
    telem.reset()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
        wav_path = tf.name
    try:
        _write_test_wav(wav_path, duration_s=0.65)
        engine = AudioEngine()
        engine.eq_bands = [3.0, 2.0, 0.0, -1.0, 0.0, 1.5, 2.5, 1.0, 0.0, 0.0]
        engine.eq_reverb = True
        ok = engine.start_play(wav_path, {"title": "TelemetrySine", "duration": 1})
        assert ok, "AudioEngine.start_play failed on generated WAV"

        deadline = time.time() + 4.0
        while time.time() < deadline:
            snap = telem.snapshot(sample_rss_now=True)
            if snap["time_to_first_audio"]["count"] >= 1 and snap["dsp_cpu"]["total_audio_seconds"] >= 0.1:
                break
            time.sleep(0.05)

        engine.cleanup_player(cancel_workers=True)
        snap = telem.snapshot(sample_rss_now=True)
        assert snap["time_to_first_audio"]["count"] >= 1, snap["time_to_first_audio"]
        assert snap["time_to_first_audio"]["avg_ms"] >= 0.0, snap["time_to_first_audio"]
        assert snap["dsp_cpu"]["count"] >= 1, snap["dsp_cpu"]
        assert snap["dsp_cpu"]["total_audio_seconds"] >= 0.08, snap["dsp_cpu"]
        assert snap["dsp_cpu"]["realtime_cpu_load_pct"] >= 0.0, snap["dsp_cpu"]
        print(
            f"[PASS] Integration AudioEngine PCM: TTFA={snap['time_to_first_audio']['avg_ms']:.2f}ms "
            f"DSP_CPU={snap['dsp_cpu']['realtime_cpu_load_pct']:.3f}%"
        )
    finally:
        if os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except Exception:
                pass


def test_integration_extractor_and_buffer_telemetry():
    telem = get_telemetry()
    telem.reset()

    ext = YouTubeExtractor(max_retries_per_tier=1)

    class _FailYdl:
        def __init__(self, opts):
            self.opts = opts
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            return False
        def extract_info(self, url, download=False):
            raise RuntimeError("This video is unavailable")

    with patch.object(ext, "_open_ydl", side_effect=lambda opts: _FailYdl(opts)):
        try:
            ext.extract_stream("K4cOLyY5o3I")
            assert False, "Expected YouTubeExtractionError"
        except YouTubeExtractionError as exc:
            assert exc.code == ExtractionErrorCode.UNAVAILABLE

    snap = telem.snapshot(sample_rss_now=False)
    yt_stats = snap["providers"].get("youtube:extract_stream")
    assert yt_stats and yt_stats["failure"] == 1, yt_stats
    assert yt_stats["error_codes"].get(ExtractionErrorCode.UNAVAILABLE) == 1, yt_stats

    # BufferManager direct stall + metrics emission
    bm = BufferManager(min_buffer_seconds=3.0)
    captured = []
    bm.on_metrics_update = lambda m: captured.append(m) or telem.record_buffer_metrics(
        stream_key=999,
        stall_count=m.stall_count,
        total_stall_seconds=m.total_stall_seconds,
        buffer_safety_seconds=m.buffer_safety_seconds,
        network_bps=m.network_bps,
        bytes_downloaded=m.bytes_downloaded,
    )
    bm.set_state(BufferState.BUFFERING)
    bm.update_download_progress(65536, total_bytes=1024000, duration_hint=60.0, network_bps=512000.0)
    bm.update_playhead(10.0)  # well ahead of buffered ~3.8s -> triggers safety check/stall

    snap2 = telem.snapshot(sample_rss_now=False)
    assert snap2["network"]["total_bytes_downloaded"] >= 65536, snap2["network"]
    assert len(captured) >= 2
    print("[PASS] Integration Extractor + Buffer telemetry counters")


if __name__ == "__main__":
    test_unit_percentiles_frame_pacing_and_thread_safety()
    test_unit_ttfa_buffer_deltas_and_provider_counters()
    test_integration_audio_engine_pcm_telemetry()
    test_integration_extractor_and_buffer_telemetry()
    print("ALL TELEMETRY SERVICE TESTS PASSED")
