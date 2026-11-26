"""
Priority 3 Verification Battery: Hardened YouTube Extraction Pipeline.
Tier 1 (Unit): Error taxonomy classification, URL/PO-token secret redaction,
        YtdlpLogBridge non-silence, signed URL expiry detection, DRM/codec filtering.
Tier 2 (Integration - Deterministic Fakes & Live Local HTTP 403 Refresh):
        Client-tier fallback + PO-token provider hook injection, exponential backoff &
        cancellation, non-retryable early exit, HTTP 403->refresh->200 recovery in
        BufferManager, and fail-safe bounded queue error protection in PlayerController.
"""

import http.server
import os
import socketserver
import struct
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

from kivy.clock import Clock

from controllers.player_controller import PlayerController
from models.track_model import TrackModel
from services.buffer_manager import BufferManager, BufferState
from services.youtube_extractor import (
    ClientTier,
    ExtractionErrorCode,
    PoTokenProviderManager,
    YouTubeExtractionError,
    YouTubeExtractor,
    YtdlpLogBridge,
    classify_extraction_error,
    is_stream_url_expired,
    parse_stream_expiry,
    redact_sensitive_text,
    validate_and_select_audio_format,
)


def _make_valid_wav_bytes(seconds: float = 0.2, sr: int = 44100) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "sample.wav")
        with wave.open(p, "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            frames = struct.pack("<hh", 0, 0) * int(seconds * sr)
            wf.writeframes(frames)
        with open(p, "rb") as f:
            return f.read()


def test_1_unit_error_taxonomy_and_secret_redaction():
    print("\n--- [Unit] 1. Error Taxonomy & URL / Token Redaction ---")
    cases = [
        ("Sign in to confirm you're not a bot. Use --cookies", ExtractionErrorCode.PO_TOKEN_REQUIRED, True),
        ("Sign in to confirm your age. This video may be inappropriate", ExtractionErrorCode.AGE_RESTRICTED, False),
        ("Video unavailable. This video has been removed", ExtractionErrorCode.UNAVAILABLE, False),
        ("The uploader has not made this video available in your country", ExtractionErrorCode.GEO_BLOCKED, False),
        ("HTTP Error 403: Forbidden", ExtractionErrorCode.STREAM_EXPIRED, True),
        ("HTTP Error 429: Too Many Requests", ExtractionErrorCode.RATE_LIMITED, True),
        ("Read timed out after 15s", ExtractionErrorCode.NETWORK_TRANSIENT, True),
        ("Requested format is not available", ExtractionErrorCode.NO_VALID_FORMAT, True),
    ]
    for msg, exp_code, exp_retry in cases:
        code, user_msg, retryable = classify_extraction_error(msg)
        assert code == exp_code, f"Expected {exp_code}, got {code} for {msg!r}"
        assert retryable is exp_retry, f"Expected retryable={exp_retry}, got {retryable} for {msg!r}"
        assert user_msg

    # Verify secret & signed query redaction + non-silent YtdlpLogBridge
    raw_secret = (
        "Failed on https://rr1---sn.googlevideo.com/videoplayback?expire=1799999999&sig=TOPSECRET_SIG&lsig=LEAK "
        "with po_token=SECRET_POT_VALUE and web.gvs+ANOTHER_SECRET_POT"
    )
    redacted = redact_sensitive_text(raw_secret)
    for leak in ("TOPSECRET_SIG", "LEAK", "SECRET_POT_VALUE", "ANOTHER_SECRET_POT"):
        assert leak not in redacted, f"Redactor leaked {leak!r} in {redacted!r}"
    assert "https://rr1---sn.googlevideo.com/videoplayback?<redacted>" in redacted

    bridge = YtdlpLogBridge()
    bridge.warning(raw_secret)
    bridge.error("HTTP Error 403 on https://cdn.example.com/audio?token=SHOULD_HIDE")
    captured = "\n".join(bridge.snapshot_messages())
    assert "TOPSECRET_SIG" not in captured and "SHOULD_HIDE" not in captured
    assert len(bridge.warnings) == 1 and len(bridge.errors) == 1
    print("  [PASS] All error classes and URL/PO-token redaction checks passed.")


def test_2_unit_expiry_and_format_validation():
    print("\n--- [Unit] 2. Signed URL Expiry & Audio Format Validation ---")
    now = int(time.time())
    exp_url = f"https://rr2.googlevideo.com/videoplayback?expire={now + 30}&itag=251"
    fresh_url = f"https://rr2.googlevideo.com/videoplayback?expire={now + 3600}&itag=251"
    path_exp_url = f"https://manifest.googlevideo.com/api/manifest/expire/{now - 10}/source/yt"
    static_url = "http://127.0.0.1:8080/track.mp3"

    assert parse_stream_expiry(exp_url) == float(now + 30)
    assert parse_stream_expiry(path_exp_url) == float(now - 10)
    assert parse_stream_expiry(static_url) == 0.0

    # Within 60s leeway -> treated as expired
    assert is_stream_url_expired(exp_url, leeway_sec=60.0) is True
    assert is_stream_url_expired(path_exp_url, leeway_sec=60.0) is True
    assert is_stream_url_expired(fresh_url, leeway_sec=60.0) is False
    assert is_stream_url_expired(static_url, leeway_sec=60.0) is False

    # Reject DRM & video-only formats, select highest-ranking Opus audio format
    drm_only = {"has_drm": True, "url": fresh_url, "acodec": "opus", "ext": "webm"}
    assert validate_and_select_audio_format(drm_only) is None

    mixed_info = {
        "title": "Test Track",
        "uploader": "Test Artist",
        "duration": 185,
        "formats": [
            {"url": fresh_url, "acodec": "none", "vcodec": "vp9", "ext": "webm", "abr": 0},
            {"url": fresh_url, "acodec": "opus", "vcodec": "none", "ext": "webm", "has_drm": True, "abr": 160},
            {"url": fresh_url + "&sel=aac", "acodec": "mp4a.40.2", "vcodec": "none", "ext": "m4a", "abr": 128, "protocol": "https"},
            {"url": fresh_url + "&sel=opus", "acodec": "opus", "vcodec": "none", "ext": "webm", "abr": 160, "protocol": "https"},
        ],
    }
    picked = validate_and_select_audio_format(mixed_info)
    assert picked is not None
    assert picked["ext"] == "webm" and picked["acodec"] == "opus"
    assert picked["url"].endswith("&sel=opus")
    assert picked["expires_at"] == float(now + 3600)
    print("  [PASS] Expiry detection, leeway checks, and DRM/codec filtering passed.")


def test_3_integration_client_tiers_pot_hook_backoff_and_cache():
    print("\n--- [Integration] 3. Client Tiers, PO-Token Hook, Backoff & Cache ---")
    now = int(time.time())
    calls = []
    pot_calls = []

    class _FakeYDL:
        def __init__(self, opts, behavior):
            self.opts = opts
            self.behavior = behavior

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def extract_info(self, url, download=False):
            return self.behavior(self.opts, url)

    tiers = (
        ClientTier("tier_mobile", ("ios", "android_vr"), allow_missing_pot_fallback=False),
        ClientTier("tier_web", ("mweb", "web"), allow_missing_pot_fallback=False),
    )

    pot_mgr = PoTokenProviderManager()
    pot_mgr.register_callback(lambda vid, client, ctx: pot_calls.append((vid, client, ctx)) or (
        "BASE64_TEST_POT" if client == "web" else None
    ))

    def _behavior_pot_recovery(opts, url):
        yt_args = opts["extractor_args"]["youtube"]
        calls.append(dict(yt_args))
        if yt_args["player_client"] == ["ios", "android_vr"]:
            raise RuntimeError("Sign in to confirm you're not a bot (PO Token required)")
        if "po_token" in yt_args and "web.gvs+BASE64_TEST_POT" in yt_args["po_token"]:
            return {
                "title": "Recovered Track",
                "uploader": "Hook Artist",
                "duration": 200,
                "url": f"https://rr3.googlevideo.com/videoplayback?expire={now + 7200}&v=1",
                "ext": "m4a",
                "abr": 128,
                "acodec": "mp4a.40.2",
            }
        raise RuntimeError("Missing expected PO token")

    extractor = YouTubeExtractor(
        po_token_manager=pot_mgr,
        client_tiers=tiers,
        max_retries_per_tier=2,
        base_backoff_sec=0.02,
        max_backoff_sec=0.05,
        ydl_factory=lambda opts: _FakeYDL(opts, _behavior_pot_recovery),
    )

    res = extractor.extract_stream("dQw4w9WgXcQ")
    assert res["client_tier"] == "tier_web"
    assert res["title"] == "Recovered Track"
    assert len(calls) >= 2 and any("web.gvs+BASE64_TEST_POT" in c.get("po_token", []) for c in calls)
    assert len(pot_calls) >= 1

    # Second lookup hits in-memory valid URL cache (zero additional ydl calls)
    before_count = len(calls)
    cached_res = extractor.extract_stream("dQw4w9WgXcQ")
    assert len(calls) == before_count and cached_res["url"] == res["url"]

    # force_refresh=True bypasses cache and re-extracts cleanly
    refreshed = extractor.extract_stream("dQw4w9WgXcQ", force_refresh=True)
    assert len(calls) > before_count and refreshed["title"] == "Recovered Track"

    # Non-retryable error (AGE_RESTRICTED) exits immediately on first failure
    age_calls = []
    age_extractor = YouTubeExtractor(
        client_tiers=tiers,
        max_retries_per_tier=3,
        base_backoff_sec=0.01,
        ydl_factory=lambda opts: _FakeYDL(
            opts,
            lambda o, u: age_calls.append(1) or (_ for _ in ()).throw(
                RuntimeError("Sign in to confirm your age")
            ),
        ),
    )
    try:
        age_extractor.extract_stream("ageVid00001")
        raise AssertionError("Expected YouTubeExtractionError for age-restricted video")
    except YouTubeExtractionError as err:
        assert err.code == ExtractionErrorCode.AGE_RESTRICTED
        assert err.retryable is False
        assert len(age_calls) == 1, f"Non-retryable error retried unexpectedly ({len(age_calls)} calls)"

    # Cancellation during transient backoff aborts promptly
    cancel_ev = threading.Event()
    cancel_calls = []

    def _transient_fail(o, u):
        cancel_calls.append(1)
        cancel_ev.set()
        raise RuntimeError("HTTP Error 429: Too Many Requests")

    cancel_extractor = YouTubeExtractor(
        client_tiers=tiers,
        max_retries_per_tier=3,
        base_backoff_sec=1.0,
        ydl_factory=lambda opts: _FakeYDL(opts, _transient_fail),
    )
    t0 = time.perf_counter()
    try:
        cancel_extractor.extract_stream("cancelVid01", cancel_event=cancel_ev)
        raise AssertionError("Expected CANCELLED YouTubeExtractionError")
    except YouTubeExtractionError as err:
        assert err.code == ExtractionErrorCode.CANCELLED
        assert (time.perf_counter() - t0) < 0.35
    print("  [PASS] Client-tier fallback, PO-token injection, cache refresh, non-retryable abort, and cancellation passed.")


def test_4_integration_http_403_stream_url_refresh_recovery():
    print("\n--- [Integration] 4. BufferManager HTTP 403 -> Stream Refresh -> 200 Recovery ---")
    wav_payload = _make_valid_wav_bytes(seconds=0.25)

    class _RefreshHandler(http.server.BaseHTTPRequestHandler):
        def do_HEAD(self):
            if "expired=1" in self.path:
                self.send_response(403)
                self.end_headers()
                return
            self.send_response(200)
            self.send_header("Content-Length", str(len(wav_payload)))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()

        def do_GET(self):
            if "expired=1" in self.path:
                self.send_response(403)
                self.end_headers()
                return
            self.send_response(200)
            self.send_header("Content-Length", str(len(wav_payload)))
            self.end_headers()
            self.wfile.write(wav_payload)

        def log_message(self, format, *args):
            pass

    class _Srv(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True

    with tempfile.TemporaryDirectory() as tmpdir:
        srv = _Srv(("127.0.0.1", 0), _RefreshHandler)
        port = srv.server_address[1]
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            expired_url = f"http://127.0.0.1:{port}/audio.wav?expired=1&sig=OLD_SIG"
            fresh_url = f"http://127.0.0.1:{port}/audio.wav?expired=0&sig=FRESH_SIG"
            out_path = os.path.join(tmpdir, "recovered.wav")
            refresh_calls = []

            def _refresh_cb():
                refresh_calls.append(True)
                return fresh_url

            bm = BufferManager(min_buffer_seconds=0.1)
            cancel_ev = threading.Event()
            ok = bm.download_http_stream(
                stream_url=expired_url,
                final_path=out_path,
                cancel_event=cancel_ev,
                duration_hint=0.25,
                on_refresh_stream=_refresh_cb,
                max_retries=2,
            )
            assert ok is True, f"Download recovery failed: {bm.metrics.error_message}"
            assert refresh_calls, "Expected on_refresh_stream callback to be invoked on HTTP 403"
            assert bm.metrics.state == BufferState.COMPLETED
            assert os.path.exists(out_path) and os.path.getsize(out_path) == len(wav_payload)
            assert not os.path.exists(f"{out_path}.part")
            print("  [PASS] HTTP 403 cleanly triggered stream URL refresh -> completed atomic promotion.")
        finally:
            srv.shutdown()
            srv.server_close()


def test_5_integration_player_controller_failsafe_queue():
    print("\n--- [Integration] 5. PlayerController Fail-Safe Queue Error Bounds ---")
    pc = PlayerController()
    tracks = [
        TrackModel(video_id=f"bad_vid_{i}", title=f"Track {i}", artist="Artist", duration=120)
        for i in range(5)
    ]
    pc.set_custom_queue(tracks, start_track=tracks[0])

    # Avoid network calls when testing queue error auto-advance bounding cleanly
    play_calls = []
    pc.audio_engine.resolve_and_play_track = lambda meta: play_calls.append(meta.get("video_id")) or True
    pc.play()
    assert pc._manual_stopped is False and pc.is_playing is True

    # Simulate repeated blocked extraction errors with secret URL leak
    for _ in range(5):
        pc._on_audio_error("HTTP 403 on https://rr1.googlevideo.com/videoplayback?sig=LEAK_ME&po_token=BAD_POT")
        Clock.tick()
        time.sleep(0.28)
        Clock.tick()

    assert "LEAK_ME" not in pc.status_text and "BAD_POT" not in pc.status_text
    assert pc.is_playing is False and pc.is_loading is False
    # Capped strictly at <= 3 consecutive skips (initial play + 3 fail-safe advances)
    assert pc._consecutive_error_skips <= 3
    assert len(play_calls) <= 4, f"Expected bounded skips (<=4 play attempts), got {len(play_calls)}"
    pc.stop()
    print(f"  [PASS] Bounded fail-safe queue handled 5 consecutive errors safely ({len(play_calls)} total attempts).")


if __name__ == "__main__":
    print("=" * 72)
    print("PRIORITY 3 YOUTUBE EXTRACTION RESILIENCE VERIFICATION")
    print("=" * 72)
    test_1_unit_error_taxonomy_and_secret_redaction()
    test_2_unit_expiry_and_format_validation()
    test_3_integration_client_tiers_pot_hook_backoff_and_cache()
    test_4_integration_http_403_stream_url_refresh_recovery()
    test_5_integration_player_controller_failsafe_queue()
    print("\nALL YOUTUBE EXTRACTION RESILIENCE CHECKS PASSED.")
