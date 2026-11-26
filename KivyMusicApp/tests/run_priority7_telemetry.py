"""Priority 7 Real Runtime Telemetry & Device Verification Runner.

Executes REAL (non-headless, real SDL2/OpenGL window + real Windows SDL2 audio
hardware + live provider network probe + adb Android device probe) measurements
corresponding strictly to GEMINI.md Section 11 Tiers 3 and 4, and writes JSON
and Markdown reports under `KivyMusicApp/docs/performance/`.
"""

from __future__ import annotations

import json
import math
import os
import struct
import sys
import tempfile
import time
import wave

# Strictly NON-HEADLESS so Kivy creates a real OpenGL/SDL2 desktop window & real VSync pacing
os.environ.pop("KIVY_HEADLESS", None)
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KYM_FORCE_TELEMETRY"] = "1"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from services.telemetry_service import get_telemetry
from services.music_provider_router import MusicProviderRouter
from services.youtube_extractor import get_youtube_extractor
from tools.android_device_probe import inspect_android_device


def _write_gentle_wav(path: str, duration_s: float = 3.2, sr: int = 44100, freq: float = 220.0) -> None:
    n_frames = int(duration_s * sr)
    frames = bytearray()
    for i in range(n_frames):
        # Soft low-amplitude tone (-24 dBFS) multiplied further by engine.volume=0.05
        val = int(2000.0 * math.sin(2.0 * math.pi * freq * (i / float(sr))))
        frames.extend(struct.pack("<hh", val, val))
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(bytes(frames))


def run_desktop_live_telemetry() -> dict:
    from kivy.clock import Clock
    from main import MusicApp

    telem = get_telemetry()
    telem.sample_memory(min_interval_seconds=0.0)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
        wav_path = tf.name
    _write_gentle_wav(wav_path, duration_s=3.2)

    app = MusicApp()
    nav_screens = ["home", "search", "library", "player", "equalizer", "analytics", "settings", "home"]
    state = {"started_audio": False, "nav_idx": 0, "done": False}

    def _finish(dt=None):
        if state["done"]:
            return
        state["done"] = True
        try:
            if app.player_controller and app.player_controller.audio_engine:
                app.player_controller.audio_engine.cleanup_player(cancel_workers=True)
        except Exception:
            pass
        app.stop()

    def _poll_driver(dt):
        telem.sample_memory(min_interval_seconds=0.5)
        if not getattr(app, "_splash_completed", False):
            return
        sm = app.root.ids.screen_manager if (app.root and "screen_manager" in app.root.ids) else None
        if sm and state["nav_idx"] < len(nav_screens):
            target = nav_screens[state["nav_idx"]]
            state["nav_idx"] += 1
            try:
                app.switch_screen(target)
            except Exception:
                pass
            return

        if not state["started_audio"] and app.player_controller and app.player_controller.audio_engine:
            state["started_audio"] = True
            eng = app.player_controller.audio_engine
            eng.volume = 0.05
            eng.eq_bands = [2.5, 1.5, 0.0, -1.0, 0.0, 1.0, 2.0, 1.5, 0.0, 0.0]
            eng.eq_reverb = True
            eng.start_play(wav_path, {"title": "Telemetry Verification Sine", "artist": "QA", "duration": 3})
            # Allow ~3.6s of real stereo SDL2 playback + 60fps UI frame pacing before teardown
            Clock.schedule_once(_finish, 3.6)

    Clock.schedule_interval(_poll_driver, 0.16)
    Clock.schedule_once(_finish, 25.0)

    try:
        app.run()
    finally:
        if os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except Exception:
                pass

    # Live external provider health probe (JioSaavn + YouTube) after UI closes
    router = MusicProviderRouter()
    provider_probes = {}
    for pname, fn in [
        ("jiosaavn_search", lambda: router.search("Arijit Singh", provider="jiosaavn", limit=3)),
        ("youtube_search", lambda: router.search("lofi beats", provider="youtube", limit=3)),
        ("youtube_stream_extract", lambda: get_youtube_extractor().extract_stream("yKNxeF4KMsY")),
    ]:
        t0 = time.perf_counter()
        try:
            res = fn()
            ok = bool(res)
            provider_probes[pname] = {
                "ok": ok,
                "latency_ms": round((time.perf_counter() - t0) * 1000.0, 2),
                "count_or_ext": len(res) if isinstance(res, list) else (res.get("ext") if isinstance(res, dict) else None),
                "error": None,
            }
        except Exception as exc:
            provider_probes[pname] = {
                "ok": False,
                "latency_ms": round((time.perf_counter() - t0) * 1000.0, 2),
                "count_or_ext": 0,
                "error": f"{type(exc).__name__}: {exc}",
            }

    snap = telem.snapshot(sample_rss_now=True)
    snap["live_provider_probes"] = provider_probes
    return snap


def write_reports(desktop_snap: dict, android_report: dict) -> tuple[str, str]:
    out_dir = os.path.join(ROOT, "docs", "performance")
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, "priority7_telemetry_report.json")
    md_path = os.path.join(out_dir, "priority7_telemetry_report.md")

    combined = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "windows_desktop_live_telemetry": desktop_snap,
        "android_device_verification": android_report,
    }
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(combined, fh, indent=2, ensure_ascii=False)

    fp = desktop_snap["frame_pacing"]
    ttfa = desktop_snap["time_to_first_audio"]
    dsp = desktop_snap["dsp_cpu"]
    mem = desktop_snap["memory_rss_mb"]
    buf = desktop_snap["buffering"]
    net = desktop_snap["network"]
    cs = desktop_snap["cold_startup"]

    md_lines = [
        "# Priority 7 Device & Performance Telemetry Report",
        "",
        f"Generated UTC: `{combined['generated_utc']}`",
        "",
        "## Tier 4 — Live Windows Desktop Runtime Telemetry (Real SDL2/OpenGL + SDL2 Audio)",
        "",
        "| Metric | Measured Value | Notes |",
        "|---|---|---|",
        f"| Cold Startup (`app_usable`) | `{cs['cold_startup_ms']}` ms | `stages_ms={cs['stages_ms']}` |",
        f"| Time to First Audio (TTFA) | avg `{ttfa['avg_ms']}` ms (`n={ttfa['count']}`) | DecoderManager + DSPPipeline + SDL2PCMOutput |",
        f"| UI Frame Pacing (p50 / p95 / p99 / max) | `{fp['p50_ms']} / {fp['p95_ms']} / {fp['p99_ms']} / {fp['max_ms']}` ms | `{fp['total_frames_recorded']}` frames, avg `{fp['avg_fps']}` FPS, missed >16.67ms: `{fp['missed_16ms_count']}` (`{fp['missed_16ms_pct']}%`), >33.3ms: `{fp['jank_33ms_count']}` |",
        f"| Process RAM RSS (baseline / peak / current / delta) | `{mem['baseline_mb']} / {mem['peak_mb']} / {mem['current_mb']} / {mem['delta_mb']}` MiB | `{mem['sample_count']}` RSS samples |",
        f"| DSP CPU Load (real-time budget) | `{dsp['realtime_cpu_load_pct']}%` | `{dsp['total_compute_seconds']}s` DSP for `{dsp['total_audio_seconds']}s` audio (10-band RBJ EQ + Reverb), chunk p95=`{dsp['p95_ms']}` ms |",
        f"| Buffer Stalls / Safety | `{buf['stall_count']}` stalls (`{buf['total_stall_seconds']}s`) | Live audio test played local WAV; remote buffer samples=`{buf['sample_count']}` |",
        f"| Network Throughput / Retries | `{net['total_bytes_downloaded']}` bytes, `{net['http_retry_count']}` retries | Stream refreshes=`{net['stream_refresh_count']}` |",
        "",
        "### Provider Live Probe Results",
        "",
    ]
    for pname, info in desktop_snap.get("live_provider_probes", {}).items():
        md_lines.append(f"- `{pname}`: ok=`{info['ok']}`, latency=`{info['latency_ms']}` ms, result=`{info['count_or_ext']}`, err=`{info['error']}`")

    md_lines.extend([
        "",
        "## Tier 3 — Android Physical Hardware Probe (`adb`)",
        "",
        f"- Status: **{android_report.get('device_verification_status')}**",
        f"- Device: `{android_report.get('device_info', {}).get('manufacturer')}` `{android_report.get('device_info', {}).get('model')}` (`{android_report.get('device_info', {}).get('serial')}`), Android SDK `{android_report.get('device_info', {}).get('sdk_int')}`, ABIs `{android_report.get('device_info', {}).get('abi_list')}`",
        f"- APK Installed (`{android_report.get('package_id')}`): `{android_report.get('apk_installed')}`",
        f"- Blockers: `{android_report.get('blockers')}`",
    ])
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md_lines) + "\n")

    return json_path, md_path


if __name__ == "__main__":
    desk = run_desktop_live_telemetry()
    andr = inspect_android_device()
    jp, mp = write_reports(desk, andr)
    print(f"[Priority 7] Reports written:\n  JSON: {jp}\n  MD:   {mp}")
    print(json.dumps({"desktop": desk, "android": andr}, indent=2, ensure_ascii=False))
