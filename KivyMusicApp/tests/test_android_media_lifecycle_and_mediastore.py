"""
Priority 6 Verification Battery: Android Native Media Lifecycle & API 33+ MediaStore Bridges.

VERIFICATION SCOPE DISCLAIMER (GEMINI.md §11 & §20):
- Tier 1 (Unit) & Tier 2 (Mocked JNI / ContentResolver Integration):
  Tests permission selection by SDK API level, PlaybackSessionSnapshot serialization &
  process-recreation restoration via SQLite, AudioFocus loss/duck/regain transitions,
  noisy/headset/Bluetooth route disconnect pausing, MediaSession transport controls,
  ForegroundService state synchronization, and Android MediaStore scanning/deduplication.
- Physical Android APK runtime execution (actual Android OS ForegroundService, lock-screen
  MediaSession rendering, hardware BT unplug broadcast, real MediaStore Cursor) CANNOT run
  on Windows and remains explicitly UNVERIFIED until tested on hardware via `adb`.
"""

import configparser
import json
import os
import struct
import sys
import tempfile
import time
import wave

os.environ["KIVY_HEADLESS"] = "1"
os.environ["KIVY_LOG_MODE"] = "PYTHON"

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from kivy.clock import Clock

from controllers.player_controller import PlayerController
from models import database as db
from models.track_model import TrackModel
from services.android_media_lifecycle import (
    ACTION_FAVORITE,
    ACTION_NEXT,
    ACTION_PAUSE,
    ACTION_PLAY,
    ACTION_PLAY_PAUSE,
    ACTION_PREV,
    ACTION_SEEK,
    ACTION_SHUFFLE,
    ACTION_STOP,
    AUDIOFOCUS_GAIN,
    AUDIOFOCUS_LOSS,
    AUDIOFOCUS_LOSS_TRANSIENT,
    AUDIOFOCUS_LOSS_TRANSIENT_CAN_DUCK,
    AndroidMediaLifecycleCoordinator,
    PlaybackSessionSnapshot,
    required_notification_permissions_for_sdk,
    required_storage_permissions_for_sdk,
)
from utils.local_audio_utils import query_android_mediastore_audio, scan_device_offline_songs


def _make_wav(path: str, seconds: float = 2.0, sr: int = 44100) -> None:
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(struct.pack("<hh", 5, 5) * int(seconds * sr))


class _MockJNIBackend:
    def __init__(self, focus_granted: bool = True):
        self.focus_granted = focus_granted
        self.started_calls = []
        self.stop_calls = 0
        self.wakelock_states = []
        self.media_updates = []
        self.abandoned_count = 0

    def init_native(self, coord):
        return True

    def start_service(self, title, artist, is_playing):
        self.started_calls.append((title, artist, is_playing))
        return True

    def stop_service(self):
        self.stop_calls += 1

    def set_wakelock(self, held: bool):
        self.wakelock_states.append(bool(held))

    def request_audio_focus(self) -> bool:
        return self.focus_granted

    def abandon_audio_focus(self):
        self.abandoned_count += 1

    def update_media_session(self, title, artist, dur_ms, pos_ms, is_playing):
        self.media_updates.append((title, artist, dur_ms, pos_ms, is_playing))


class _MockIntent:
    def __init__(self, extras=None):
        self._extras = dict(extras or {})

    def getIntExtra(self, key: str, default: int = -1) -> int:
        return int(self._extras.get(key, default))

    def getLongExtra(self, key: str, default: int = -1) -> int:
        return int(self._extras.get(key, default))


def test_1_unit_sdk_permissions_and_snapshot_contract():
    print("\n--- [Unit] 1. Android SDK Permission Rules & Buildozer Service Manifest ---")
    assert required_storage_permissions_for_sdk(33) == ["android.permission.READ_MEDIA_AUDIO"]
    assert required_storage_permissions_for_sdk(34) == ["android.permission.READ_MEDIA_AUDIO"]
    assert required_storage_permissions_for_sdk(32) == ["android.permission.READ_EXTERNAL_STORAGE"]
    assert required_storage_permissions_for_sdk(21) == ["android.permission.READ_EXTERNAL_STORAGE"]

    assert required_notification_permissions_for_sdk(33) == ["android.permission.POST_NOTIFICATIONS"]
    assert required_notification_permissions_for_sdk(32) == []

    # Verify buildozer.spec foreground service declaration & API 33 permissions
    cfg = configparser.ConfigParser()
    cfg.read(os.path.join(APP_DIR, "buildozer.spec"), encoding="utf-8")
    perms = cfg.get("app", "android.permissions")
    svcs = cfg.get("app", "services")
    assert "READ_MEDIA_AUDIO" in perms
    assert "POST_NOTIFICATIONS" in perms
    assert "FOREGROUND_SERVICE_MEDIA_PLAYBACK" in perms
    assert "WAKE_LOCK" in perms
    assert "MusicPlayback:service/main.py:foreground" in svcs
    assert os.path.exists(os.path.join(APP_DIR, "service", "main.py"))
    assert os.path.exists(os.path.join(APP_DIR, "android_src", "org", "shivam", "music", "MediaSessionBridge.java"))
    for res_name in (
        "ic_music_note.xml",
        "ic_media_prev.xml",
        "ic_media_pause.xml",
        "ic_media_play.xml",
        "ic_media_next.xml",
        "ic_favorite_border.xml",
        "ic_favorite_filled.xml",
        "ic_shuffle.xml",
    ):
        assert os.path.exists(os.path.join(APP_DIR, "android_res", "drawable", res_name)), res_name
    assert "android_src" in cfg.get("app", "android.add_src")
    assert "android_res/drawable:drawable" in cfg.get("app", "android.add_resources")

    # Verify service/main.py compiles cleanly
    with open(os.path.join(APP_DIR, "service", "main.py"), "r", encoding="utf-8") as sf:
        compile(sf.read(), "service/main.py", "exec")

    snap = PlaybackSessionSnapshot(
        video_id="v123", title="Song X", artist="Artist Y", duration=200.0, position_seconds=42.5, is_playing=True
    )
    rt = PlaybackSessionSnapshot.from_dict(snap.to_dict())
    assert rt is not None and rt.video_id == "v123" and rt.position_seconds == 42.5
    assert PlaybackSessionSnapshot.from_dict({}) is None
    print("  [PASS] API 33+ scoped permissions, foreground service buildozer config, and snapshot serialization passed.")


def test_2_integration_audio_focus_routes_and_transport():
    print("\n--- [Integration - Mocked JNI] 2. AudioFocus, Noisy/Bluetooth Disconnects & Transport Controls ---")
    with tempfile.TemporaryDirectory() as tmpdir:
        wav_path = os.path.join(tmpdir, "sample.wav")
        _make_wav(wav_path, seconds=2.5)

        pc = PlayerController()
        jni = _MockJNIBackend(focus_granted=True)
        pc.media_lifecycle = AndroidMediaLifecycleCoordinator(pc, jni_backend=jni)
        pc.media_lifecycle._state_file_dir = tmpdir

        tracks = [
            TrackModel(video_id="t1", title="Track One", artist="Artist A", local_path=wav_path, duration=3),
            TrackModel(video_id="t2", title="Track Two", artist="Artist B", local_path=wav_path, duration=3),
        ]
        pc.set_custom_queue(tracks, start_track=tracks[0])
        pc.audio_engine.muted = True
        pc.audio_engine.volume = 0.8

        # 2a. Focus denied blocks starting playback
        jni.focus_granted = False
        pc.play()
        assert pc.is_playing is False, "Playback must not start when AudioFocus is denied"

        # 2b. Focus granted -> starts playback + foreground service + MediaSession
        jni.focus_granted = True
        pc.play()
        Clock.tick()
        assert pc.is_playing is True
        assert jni.started_calls and jni.started_calls[-1][0] == "Track One"
        assert jni.wakelock_states[-1] is True
        assert os.path.exists(os.path.join(tmpdir, "playback_service_state.json"))

        # 2c. AUDIOFOCUS_LOSS_TRANSIENT_CAN_DUCK -> reduces output multiplier while keeping user volume 0.8
        pc.media_lifecycle.on_os_audio_focus_change(AUDIOFOCUS_LOSS_TRANSIENT_CAN_DUCK)
        Clock.tick()
        assert pc.audio_engine._is_ducked is True
        assert pc.audio_engine.volume == 0.8
        assert pc.is_playing is True

        pc.media_lifecycle.on_os_audio_focus_change(AUDIOFOCUS_GAIN)
        Clock.tick()
        assert pc.audio_engine._is_ducked is False

        # 2d. AUDIOFOCUS_LOSS_TRANSIENT (phone call) pauses and AUDIOFOCUS_GAIN resumes cleanly
        pc.media_lifecycle.on_os_audio_focus_change(AUDIOFOCUS_LOSS_TRANSIENT)
        Clock.tick()
        assert pc.is_playing is False
        assert pc.media_lifecycle.paused_by_transient_focus is True

        pc.media_lifecycle.on_os_audio_focus_change(AUDIOFOCUS_GAIN)
        Clock.tick()
        assert pc.is_playing is True
        assert pc.media_lifecycle.paused_by_transient_focus is False

        # 2e. ACTION_AUDIO_BECOMING_NOISY & Bluetooth disconnect pause immediately
        pc.media_lifecycle.on_os_broadcast("android.media.AUDIO_BECOMING_NOISY")
        Clock.tick()
        assert pc.is_playing is False

        pc.play()
        Clock.tick()
        assert pc.is_playing is True
        pc.media_lifecycle.on_os_broadcast(
            "android.bluetooth.a2dp.profile.action.CONNECTION_STATE_CHANGED",
            _MockIntent({"android.bluetooth.profile.extra.STATE": 0}),
        )
        Clock.tick()
        assert pc.is_playing is False

        # 2f. Wired headset unplug pauses immediately
        pc.play()
        Clock.tick()
        pc.media_lifecycle.on_os_broadcast("android.intent.action.HEADSET_PLUG", _MockIntent({"state": 0}))
        Clock.tick()
        assert pc.is_playing is False

        # 2g. AUDIOFOCUS_LOSS (permanent loss) pauses & abandons focus cleanly
        pc.play()
        Clock.tick()
        pc.media_lifecycle.on_os_audio_focus_change(AUDIOFOCUS_LOSS)
        Clock.tick()
        assert pc.is_playing is False
        assert jni.abandoned_count >= 1

        # 2h. Notification broadcast transport controls (PLAY_PAUSE -> PAUSE -> PLAY -> FAVORITE -> SHUFFLE -> SEEK -> NEXT -> STOP)
        pc.media_lifecycle.on_os_broadcast(ACTION_PLAY_PAUSE)
        Clock.tick()
        assert pc.is_playing is True
        pc.media_lifecycle.on_os_broadcast(ACTION_PAUSE)
        Clock.tick()
        assert pc.is_playing is False
        pc.media_lifecycle.on_os_broadcast(ACTION_PLAY)
        Clock.tick()
        assert pc.is_playing is True
        prev_fav = bool(pc.is_favorite)
        pc.media_lifecycle.on_os_broadcast(ACTION_FAVORITE)
        Clock.tick()
        assert bool(pc.is_favorite) is (not prev_fav)
        prev_shuf = bool(pc.is_shuffle)
        pc.media_lifecycle.on_os_broadcast(ACTION_SHUFFLE)
        Clock.tick()
        assert bool(pc.is_shuffle) is (not prev_shuf)
        pc.media_lifecycle.on_os_broadcast(ACTION_SEEK, _MockIntent({"seek_ms": 1200}))
        Clock.tick()
        assert abs(float(pc.current_time) - 1.2) < 0.05
        svc_state = json.load(open(os.path.join(tmpdir, "playback_service_state.json"), "r", encoding="utf-8"))
        assert "is_favorite" in svc_state and "is_shuffle" in svc_state and "artwork" in svc_state
        pc.media_lifecycle.on_os_broadcast(ACTION_NEXT)
        Clock.tick()
        assert pc.active_track.video_id == "t2"
        pc.media_lifecycle.on_os_broadcast(ACTION_STOP)
        Clock.tick()
        assert pc.is_playing is False
        assert jni.stop_calls >= 1

        pc.stop()
        print("  [PASS] AudioFocus duck/transient/loss, noisy/BT/headset unplug, and MediaSession/notification controls passed.")


def test_3_integration_process_recreation_restore():
    print("\n--- [Integration] 3. Process-Recreation Playback Snapshot Persistence & Restoration ---")
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = os.path.join(tmpdir, "lifecycle_restore.db")
        orig_path = db._WORKER.get_active_path()
        try:
            db.init_db(db_file)
            pc1 = PlayerController()
            queue = [
                TrackModel(video_id="r1", title="First Song", artist="A1", duration=180),
                TrackModel(video_id="r2", title="Resume Me", artist="A2", duration=240),
                TrackModel(video_id="r3", title="Third Song", artist="A3", duration=210),
            ]
            pc1.set_custom_queue(queue, start_track=queue[1])
            pc1.repeat_mode = "all"
            pc1.is_repeat = True
            pc1.is_shuffle = True
            pc1.current_time = 93.0
            pc1.duration = 240.0
            pc1.persist_session_snapshot(wait=True)
            db.flush_db_writes()

            # Simulate cold process recreation with fresh PlayerController instance
            pc2 = PlayerController()
            restored = pc2.restore_session_snapshot()
            assert restored is not None
            assert pc2.active_track is not None and pc2.active_track.video_id == "r2"
            assert abs(pc2.current_time - 93.0) < 0.01
            assert pc2.formatted_current_time == "01:33"
            assert pc2.repeat_mode == "all" and pc2.is_shuffle is True
            assert len(pc2.queue) == 3
            assert pc2.is_playing is False  # Always restores safely paused
            pc1.stop()
            pc2.stop()
            print("  [PASS] Process-recreation snapshot restored track, queue, flags, and 01:33 timeline cleanly.")
        finally:
            time.sleep(0.08)  # Allow daemon set_track() DB init checks to exit cleanly before releasing temp DB
            db.flush_db_writes()
            db._WORKER.set_db_path(orig_path)
            db.init_db(orig_path)
            db._WORKER.reset_connections()


def test_4_integration_android_mediastore_scoped_storage():
    print("\n--- [Integration - Mocked ContentResolver] 4. Android MediaStore & Path Deduplication ---")
    with tempfile.TemporaryDirectory() as tmpdir:
        real_wav = os.path.join(tmpdir, "desi_vibe.wav")
        _make_wav(real_wav, seconds=1.2)

        rows = [
            (101, "Desi Vibe", "Artist M", "Album M", 125000, real_wav, "audio/wav", 1),
            # Strict scoped storage entry without local filesystem path readable
            (202, "Scoped Only Track", "Indie Singer", "Scoped Album", 215000, "", "audio/mp4", 1),
        ]

        class _MockCursor:
            cols = ["_id", "title", "artist", "album", "duration", "_data", "mime_type", "is_music"]

            def __init__(self):
                self._idx = -1
                self.closed = False

            def getColumnIndex(self, name):
                return self.cols.index(name) if name in self.cols else -1

            def moveToNext(self):
                self._idx += 1
                return self._idx < len(rows)

            def getString(self, col_i):
                v = rows[self._idx][col_i]
                return str(v) if v is not None else ""

            def getLong(self, col_i):
                return int(rows[self._idx][col_i] or 0)

            def close(self):
                self.closed = True

        class _MockResolver:
            def __init__(self):
                self.cursors = []

            def query(self, uri, projection, selection, selection_args, sort_order):
                c = _MockCursor()
                self.cursors.append(c)
                return c

        res1 = _MockResolver()
        ms_tracks = query_android_mediastore_audio(cache_dir=tmpdir, resolver=res1)
        assert res1.cursors and res1.cursors[-1].closed is True
        assert len(ms_tracks) == 2
        assert ms_tracks[0]["title"] == "Desi Vibe" and ms_tracks[0]["local_path"] == os.path.realpath(real_wav)
        assert ms_tracks[1]["video_id"] == "ms_202"
        assert ms_tracks[1]["duration"] == 215
        assert ms_tracks[1]["local_path"] == "content://media/external/audio/media/202"

        # Deduplicate cleanly when scanning BOTH MediaStore and overlapping directory
        scanned = scan_device_offline_songs(
            directories=[tmpdir],
            cache_dir=tmpdir,
            use_mediastore=True,
            mediastore_querier=lambda cache_dir=None, limit=None: query_android_mediastore_audio(
                cache_dir=cache_dir, limit=limit, resolver=_MockResolver()
            ),
        )
        # Note: mock_cursor resets cleanly on fresh _MockResolver(); verify 2 unique tracks (no dup of real_wav!)
        assert len(scanned) == 2, f"Expected deduplicated 2 tracks across MediaStore + directory, got {len(scanned)}"
        print("  [PASS] Mocked MediaStore ContentResolver + Scoped URI + directory deduplication verified.")


if __name__ == "__main__":
    print("=" * 72)
    print("PRIORITY 6 ANDROID LIFECYCLE & SCOPED STORAGE BRIDGE VERIFICATION")
    print("=" * 72)
    test_1_unit_sdk_permissions_and_snapshot_contract()
    test_2_integration_audio_focus_routes_and_transport()
    test_3_integration_process_recreation_restore()
    test_4_integration_android_mediastore_scoped_storage()
    print("\nALL PRIORITY 6 ANDROID BRIDGE CHECKS PASSED (Mocked JNI Verified; Physical APK Unverified).")
