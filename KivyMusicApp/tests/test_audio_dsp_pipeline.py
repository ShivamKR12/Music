"""
Priority 1 & 2 Verification Battery:
Tier 1 (Unit): RBJ biquad frequency response, soft headroom limiter, correlated cos/sin crossfade.
Tier 2 (Integration - Real Codecs & HTTP Server): FFmpeg/WAV decoding across WAV/MP3/Opus/M4A,
        seek accuracy, BufferManager Range download + cancel safety, non-blocking PlayerController.play().
Tier 3 (Windows Hardware Audio Output): Real SDL2.dll PCM device open, queue, drain, flush, close.
Tier 4 (Performance Telemetry): First-chunk PCM decode latency & 10-band DSP CPU load.
"""

import http.server
import math
import os
import shutil
import socketserver
import struct
import subprocess
import sys
import tempfile
import threading
import time
import wave

os.environ["KIVY_HEADLESS"] = "1"
os.environ["KIVY_LOG_MODE"] = "PYTHON"

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

import numpy as np
from kivy.clock import Clock

from controllers.player_controller import PlayerController
from models.track_model import TrackModel
from services.audio_engine import AudioEngine
from services.audio_output import SDL2PCMOutput
from services.buffer_manager import BufferManager, BufferState, is_valid_audio_header
from services.decoder_manager import DecoderManager, probe_duration_seconds
from services.dsp_pipeline import DSPPipeline, ISO_EQ_FREQUENCIES, mix_crossfade


def _make_sine_pcm(freq_hz: float, seconds: float = 2.0, amp: float = 0.25, sr: int = 44100) -> np.ndarray:
    t = np.arange(int(seconds * sr), dtype=np.float64) / float(sr)
    sig = (amp * np.sin(2.0 * np.pi * freq_hz * t)).astype(np.float32)
    return np.column_stack((sig, sig))


def _write_wav(path: str, pcm_f32: np.ndarray, sr: int = 44100) -> None:
    i16 = np.clip(pcm_f32 * 32767.0, -32768, 32767).astype("<i2")
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(i16.tobytes())


def test_1_unit_biquad_eq_frequency_response():
    print("\n--- [Unit] 1. RBJ 10-Band Biquad EQ Gain & Cut ---")
    tone = _make_sine_pcm(1000.0, seconds=1.0, amp=0.15)
    steady = slice(22050, 44100)  # ignore first 0.5s filter transient

    dsp_flat = DSPPipeline(44100, 2)
    out_flat = dsp_flat.process(tone, volume=1.0)
    rms_flat = float(np.sqrt(np.mean(out_flat[steady] ** 2)))

    # Index 5 is 1000 Hz
    bands_boost = [0.0] * len(ISO_EQ_FREQUENCIES)
    bands_boost[5] = 12.0
    dsp_boost = DSPPipeline(44100, 2)
    dsp_boost.set_eq_bands(bands_boost, reverb=False)
    out_boost = dsp_boost.process(tone, volume=1.0)
    rms_boost = float(np.sqrt(np.mean(out_boost[steady] ** 2)))

    bands_cut = [0.0] * len(ISO_EQ_FREQUENCIES)
    bands_cut[5] = -12.0
    dsp_cut = DSPPipeline(44100, 2)
    dsp_cut.set_eq_bands(bands_cut, reverb=False)
    out_cut = dsp_cut.process(tone, volume=1.0)
    rms_cut = float(np.sqrt(np.mean(out_cut[steady] ** 2)))

    boost_ratio = rms_boost / rms_flat
    cut_ratio = rms_cut / rms_flat
    print(f"  1kHz RMS ratios -> flat=1.000, +12dB={boost_ratio:.3f}x, -12dB={cut_ratio:.3f}x")
    assert 3.5 < boost_ratio < 4.2, f"Expected ~3.98x amplitude boost at +12dB, got {boost_ratio}"
    assert 0.20 < cut_ratio < 0.30, f"Expected ~0.25x amplitude cut at -12dB, got {cut_ratio}"
    print("  [PASS] Unit EQ response matches mathematical gain/attenuation targets.")


def test_2_unit_correlated_crossfade_headroom():
    print("\n--- [Unit] 2. Correlated Equal-Power Crossfade & Soft-Clip Limiter ---")
    # Two identical full-scale 0.95 amplitude 440 Hz tones in-phase (worst case +3dB midpoint)
    a = _make_sine_pcm(440.0, seconds=1.0, amp=0.95)
    b = _make_sine_pcm(440.0, seconds=1.0, amp=0.95)
    mixed = mix_crossfade(a, b, 0.0, 1.0)
    peak = float(np.max(np.abs(mixed)))
    assert np.all(np.isfinite(mixed)), "Crossfade output contains non-finite samples"
    assert peak < 1.0, f"Correlated crossfade clipped >= 1.0! peak={peak}"
    # Verify ends match Track A start (~0.95 limit) and Track B end (~0.95 limit)
    start_rms = float(np.sqrt(np.mean(mixed[:2000] ** 2)))
    mid_rms = float(np.sqrt(np.mean(mixed[21000:23000] ** 2)))
    end_rms = float(np.sqrt(np.mean(mixed[-2000:] ** 2)))
    print(f"  Correlated mix peak={peak:.4f} (<1.0 safe); RMS start={start_rms:.3f}, mid={mid_rms:.3f}, end={end_rms:.3f}")
    assert start_rms > 0.5 and mid_rms > 0.5 and end_rms > 0.5
    print("  [PASS] Equal-power crossfade prevents correlated clipping while preserving loudness.")


def test_3_real_codec_decoding_and_seek():
    print("\n--- [Integration] 3. Real WAV / MP3 / Opus / M4A Decoding & Seeking ---")
    ffmpeg = shutil.which("ffmpeg")
    assert ffmpeg, "ffmpeg binary must exist on PATH for compressed codec verification"

    with tempfile.TemporaryDirectory() as tmpdir:
        src_wav = os.path.join(tmpdir, "tone.wav")
        _write_wav(src_wav, _make_sine_pcm(523.25, seconds=3.0, amp=0.35))

        targets = [
            ("wav", src_wav),
            ("mp3", os.path.join(tmpdir, "tone.mp3")),
            ("opus", os.path.join(tmpdir, "tone.opus")),
            ("m4a", os.path.join(tmpdir, "tone.m4a")),
        ]
        # Transcode real compressed fixtures
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", src_wav, "-c:a", "libmp3lame", "-b:a", "128k", targets[1][1]], check=True)
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", src_wav, "-c:a", "libopus", "-b:a", "96k", targets[2][1]], check=True)
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", src_wav, "-c:a", "aac", "-b:a", "128k", targets[3][1]], check=True)

        for codec, path in targets:
            assert is_valid_audio_header(path), f"Header validation failed for {codec}"
            dur = probe_duration_seconds(path)
            assert 2.7 <= dur <= 3.3, f"Duration probe inaccurate for {codec}: {dur}"

            t0 = time.perf_counter()
            dec = DecoderManager.open_stream(path)
            assert dec is not None, f"Failed to open PCM stream for {codec}"
            chunk = dec.read_frames(4096)
            t1 = time.perf_counter()
            assert chunk is not None and chunk.shape[1] == 2 and chunk.dtype == np.float32
            assert float(np.max(np.abs(chunk))) > 0.05, f"Decoded silent PCM for {codec}"

            ok_seek = dec.seek(1.5)
            assert ok_seek, f"Seek failed for {codec}"
            assert abs((dec.position_frames / 44100.0) - 1.5) < 0.05
            post_seek = dec.read_frames(4096)
            assert post_seek is not None and len(post_seek) > 0
            dec.close()
            print(f"  [{codec.upper():<4}] dur={dur:.2f}s | first_4096_pcm={(t1-t0)*1000:.1f}ms | peak={np.max(np.abs(chunk)):.3f} | seek_ok=True")

    print("  [PASS] Real WAV, MP3, Opus, and M4A decode cleanly with accurate duration and seek.")


def test_4_real_http_range_buffer_manager():
    print("\n--- [Integration] 4. Real HTTP Range BufferManager & Atomic Completion ---")
    ffmpeg = shutil.which("ffmpeg")
    assert ffmpeg, "ffmpeg binary required for test fixture"

    with tempfile.TemporaryDirectory() as tmpdir:
        wav_p = os.path.join(tmpdir, "src.wav")
        mp3_p = os.path.join(tmpdir, "sample.mp3")
        _write_wav(wav_p, _make_sine_pcm(440.0, seconds=6.0, amp=0.3))
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", wav_p, "-c:a", "libmp3lame", "-b:a", "192k", mp3_p], check=True)
        expected_size = os.path.getsize(mp3_p)

        class RangeHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass

            def do_HEAD(self):
                self.send_response(200)
                self.send_header("Content-Length", str(expected_size))
                self.send_header("Accept-Ranges", "bytes")
                self.end_headers()

            def do_GET(self):
                with open(mp3_p, "rb") as f:
                    data = f.read()
                rng = self.headers.get("Range")
                if rng and rng.startswith("bytes="):
                    start = int(rng.replace("bytes=", "").split("-")[0] or 0)
                    chunk = data[start:]
                    self.send_response(206)
                    self.send_header("Content-Range", f"bytes {start}-{expected_size - 1}/{expected_size}")
                    self.send_header("Content-Length", str(len(chunk)))
                    self.end_headers()
                    self.wfile.write(chunk)
                else:
                    self.send_response(200)
                    self.send_header("Content-Length", str(expected_size))
                    self.send_header("Accept-Ranges", "bytes")
                    self.end_headers()
                    # Stream in 32KB slices to exercise multi-chunk updates
                    for off in range(0, len(data), 32768):
                        self.wfile.write(data[off : off + 32768])
                        time.sleep(0.01)

        with socketserver.TCPServer(("127.0.0.1", 0), RangeHandler) as srv:
            port = srv.server_address[1]
            t_srv = threading.Thread(target=srv.serve_forever, daemon=True)
            t_srv.start()
            try:
                url = f"http://127.0.0.1:{port}/sample.mp3"
                bm = BufferManager(min_buffer_seconds=1.5)
                out_file = os.path.join(tmpdir, "cached_out.mp3")
                cancel_ev = threading.Event()
                completed_flag = []

                ok = bm.download_http_stream(
                    stream_url=url,
                    final_path=out_file,
                    cancel_event=cancel_ev,
                    duration_hint=6.0,
                    bitrate_bps=192000,
                    on_completed=lambda p, m: completed_flag.append((p, m)),
                )
                assert ok and len(completed_flag) == 1
                assert bm.metrics.state == BufferState.COMPLETED
                assert bm.metrics.supports_range is True
                assert abs(bm.metrics.download_progress - 1.0) < 1e-6
                assert bm.metrics.playable_buffer_seconds >= 5.5
                assert os.path.exists(out_file) and os.path.getsize(out_file) == expected_size
                assert not os.path.exists(f"{out_file}.part"), "Temporary .part file must be atomically promoted"

                # Test cancellation prevents partial corruption
                cancel_out = os.path.join(tmpdir, "cancelled.mp3")
                cancel_ev2 = threading.Event()
                cancel_ev2.set()
                ok_cancel = bm.download_http_stream(url, cancel_out, cancel_ev2)
                assert ok_cancel is False
                assert bm.metrics.state == BufferState.CANCELLED
                assert not os.path.exists(cancel_out)
            finally:
                srv.shutdown()

    print("  [PASS] HTTP Range probe, atomic .part promotion, 3-metric telemetry, and cancel cleanup verified.")


def test_5_nonblocking_controller_and_dsp_cpu_telemetry():
    print("\n--- [Integration + Telemetry] 5. Non-Blocking PlayerController & DSP CPU Load ---")
    pc = PlayerController()
    remote_track = TrackModel(
        video_id="yt_nonexistent_test_id",
        title="Remote Stream Test",
        artist="Test Artist",
        duration=210,
        source="spotify",
        url="",
    )
    pc.set_track(remote_track)
    t0 = time.perf_counter()
    pc.play()
    dt_ms = (time.perf_counter() - t0) * 1000.0
    pc.stop()
    print(f"  PlayerController.play() UI-thread return latency: {dt_ms:.2f}ms")
    assert dt_ms < 25.0, f"PlayerController.play() blocked calling thread for {dt_ms:.2f}ms!"

    # DSP 10-band active filtering CPU telemetry (10s of 44.1kHz stereo audio)
    dsp = DSPPipeline(44100, 2)
    dsp.set_eq_bands([4.0, 3.0, 1.5, 0.0, -1.0, 0.5, 2.0, 3.0, 2.0, 1.0], reverb=True)
    chunk = _make_sine_pcm(440.0, seconds=4096 / 44100.0, amp=0.5)
    t_dsp_0 = time.perf_counter()
    for _ in range(108):  # ~10 seconds of audio
        _ = dsp.process(chunk, volume=0.9)
    dsp_cpu_ms = (time.perf_counter() - t_dsp_0) * 1000.0
    cpu_pct = (dsp_cpu_ms / 10000.0) * 100.0
    print(f"  DSP 10-band + Reverb + Limiter 10s telemetry: {dsp_cpu_ms:.2f}ms ({cpu_pct:.2f}% of 1 core)")
    assert cpu_pct < 15.0, f"DSP CPU load unexpectedly high: {cpu_pct:.2f}%"
    print("  [PASS] Zero UI-thread blocking on play() and real DSP load within budget.")


def test_6_hardware_sdl2_device_smoke():
    print("\n--- [Device - Windows SDL2 Audio] 6. Real SDL2.dll PCM Device Open/Queue/Close ---")
    try:
        out = SDL2PCMOutput(44100, 2, buffer_samples=1024)
    except Exception as exc:
        print(f"  [SKIP] No interactive SDL2 audio device in this environment ({exc})")
        return
    try:
        # Very quiet sub-audible 440Hz pulse (0.001 amplitude, 0.5s) so hardware drain is verifiable
        pcm = _make_sine_pcm(440.0, seconds=0.5, amp=0.001)
        assert out.write(pcm.tobytes(), len(pcm))
        assert out.queued_seconds() > 0.0
        deadline = time.perf_counter() + 1.5
        while time.perf_counter() < deadline and out.played_seconds() <= 0.05:
            time.sleep(0.02)
        played = out.played_seconds()
        assert played > 0.05, f"Hardware device did not consume queued PCM (played={played})"
        out.flush()
        assert out.queued_seconds() == 0.0
        print(f"  [PASS] Real Windows SDL2 audio device drained PCM cleanly (played={played:.3f}s).")
    finally:
        out.close()


def test_7_dual_deck_equal_power_crossfade_promotion():
    print("\n--- [Integration - Dual Deck Crossfade] 7. AudioEngine Deck B Promotion & Handle Cleanup ---")
    with tempfile.TemporaryDirectory() as tmpdir:
        wav_a = os.path.join(tmpdir, "deck_a.wav")
        wav_b = os.path.join(tmpdir, "deck_b.wav")
        _write_wav(wav_a, _make_sine_pcm(440.0, seconds=6.0, amp=0.0005))
        _write_wav(wav_b, _make_sine_pcm(523.25, seconds=2.0, amp=0.0005))

        engine = AudioEngine()
        engine.crossfade_duration = 1.0
        triggered = []
        promoted = []

        def _on_trigger():
            if not triggered:
                triggered.append(True)
                engine.stage_next_deck(
                    {"title": "Deck B", "artist": "Unit", "local_path": wav_b, "duration": 2.0}
                )

        engine.on_crossfade_trigger = _on_trigger
        engine.on_crossfade_track_advanced = lambda info: promoted.append(dict(info))

        try:
            started = engine.start_play(
                wav_a, {"title": "Deck A", "artist": "Unit", "local_path": wav_a, "duration": 6.0}
            )
            assert started, "AudioEngine.start_play returned False for Deck A"

            # Wait briefly for render loop startup, then seek near end (2.2s remaining)
            warmup_end = time.perf_counter() + 0.25
            while time.perf_counter() < warmup_end:
                Clock.tick()
                time.sleep(0.02)

            engine.seek(3.8)
            deadline = time.perf_counter() + 4.5
            while time.perf_counter() < deadline and not promoted:
                Clock.tick()
                time.sleep(0.03)

            assert triggered, "AudioEngine did not fire on_crossfade_trigger near track end"
            assert promoted, "AudioEngine did not promote Deck B via on_crossfade_track_advanced"
            assert promoted[0].get("title") == "Deck B", f"Unexpected promoted track: {promoted[0]}"
            print("  [PASS] Dual-deck crossfade triggered Deck B staging and promoted cleanly.")
        finally:
            engine.cleanup_player()

        # Verify zero leaked file handles on Windows after cleanup_player()
        os.remove(wav_a)
        os.remove(wav_b)
        print("  [PASS] Zero leaked open file handles after cleanup_player().")


if __name__ == "__main__":
    print("=" * 72)
    print("PRIORITY 1 & 2 REAL AUDIO, PCM DSP & PROGRESSIVE BUFFERING TESTS")
    print("=" * 72)
    test_1_unit_biquad_eq_frequency_response()
    test_2_unit_correlated_crossfade_headroom()
    test_3_real_codec_decoding_and_seek()
    test_4_real_http_range_buffer_manager()
    test_5_nonblocking_controller_and_dsp_cpu_telemetry()
    test_6_hardware_sdl2_device_smoke()
    test_7_dual_deck_equal_power_crossfade_promotion()
    print("\nALL AUDIO & PCM DSP PIPELINE CHECKS PASSED (Desktop Verified; Android Device Unverified).")
