"""
Android Native Media Lifecycle Coordinator (`GEMINI.md §23`).

Manages:
1. Foreground media service lifecycle state + IPC manifest synchronization (`service/main.py`).
2. Android `MediaSession` metadata & lock-screen / Bluetooth AVRCP transport callbacks.
3. OS Audio Focus negotiation (permanent loss, transient call interruption, navigation ducking, regain).
4. Route-change protection (`ACTION_AUDIO_BECOMING_NOISY`, wired headset unplug, Bluetooth A2DP disconnect).
5. Partial `WakeLock` management while playing audio.
6. Process-recreation playback state snapshot persistence & restoration (`playback_session_snapshot`).
7. Android API-version-aware storage & notification permission selection (`API 33+ READ_MEDIA_AUDIO`).

IMPORTANT STATUS NOTE:
- Designed & Implemented cleanly across Desktop and Android layers using injectable JNI bridges.
- Pure-Python state machines and mocked-JNI contracts are verified in headless suites;
  actual Android runtime behavior requires physical/emulated APK execution via `adb`.
"""

from __future__ import annotations

import json
import os
import threading
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, List, Optional

from kivy.clock import Clock
from kivy.utils import platform

from services.logger import get_logger

logger = get_logger("AndroidMediaLifecycle")

# Standard Android AudioManager audio focus constants (kept exact for unit/JNI parity)
AUDIOFOCUS_NONE = 0
AUDIOFOCUS_GAIN = 1
AUDIOFOCUS_LOSS = -1
AUDIOFOCUS_LOSS_TRANSIENT = -2
AUDIOFOCUS_LOSS_TRANSIENT_CAN_DUCK = -3
AUDIOFOCUS_REQUEST_FAILED = 0
AUDIOFOCUS_REQUEST_GRANTED = 1

# Transport action broadcast strings
ACTION_PLAY = "org.shivam.music.ACTION_PLAY"
ACTION_PAUSE = "org.shivam.music.ACTION_PAUSE"
ACTION_PLAY_PAUSE = "org.shivam.music.ACTION_PLAY_PAUSE"
ACTION_NEXT = "org.shivam.music.ACTION_NEXT"
ACTION_PREV = "org.shivam.music.ACTION_PREV"
ACTION_STOP = "org.shivam.music.ACTION_STOP"
ACTION_SEEK = "org.shivam.music.ACTION_SEEK"
ACTION_FAVORITE = "org.shivam.music.ACTION_FAVORITE"
ACTION_SHUFFLE = "org.shivam.music.ACTION_SHUFFLE"
ACTION_REQUEST_MEDIA_TOKEN = "org.shivam.music.ACTION_REQUEST_MEDIA_TOKEN"
ACTION_SYNC_MEDIA_TOKEN = "org.shivam.music.ACTION_SYNC_MEDIA_TOKEN"

SNAPSHOT_CACHE_KEY = "playback_session_snapshot"


def required_storage_permissions_for_sdk(sdk_int: int) -> List[str]:
    """
    Return exact runtime Android permissions appropriate for the device's OS API level.
    - API 33+ (Android 13+): Scoped audio permission `READ_MEDIA_AUDIO` (never legacy
      `READ_EXTERNAL_STORAGE`, which fails/confuses modern grant dialogs).
    - API <= 32: `READ_EXTERNAL_STORAGE`.
    """
    if int(sdk_int or 0) >= 33:
        return ["android.permission.READ_MEDIA_AUDIO"]
    return ["android.permission.READ_EXTERNAL_STORAGE"]


def required_notification_permissions_for_sdk(sdk_int: int) -> List[str]:
    """Return `POST_NOTIFICATIONS` on Android 13+ (API 33+), empty list on older Android."""
    if int(sdk_int or 0) >= 33:
        return ["android.permission.POST_NOTIFICATIONS"]
    return []


@dataclass
class PlaybackSessionSnapshot:
    """Serializable playback session state for Android process-recreation recovery."""
    video_id: str = ""
    title: str = ""
    artist: str = ""
    url: str = ""
    local_path: str = ""
    artwork: str = ""
    duration: float = 0.0
    position_seconds: float = 0.0
    is_playing: bool = False
    repeat_mode: str = "off"
    is_shuffle: bool = False
    source: str = "youtube"
    queue_tracks: List[Dict[str, Any]] = field(default_factory=list)
    queue_index: int = 0
    saved_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["PlaybackSessionSnapshot"]:
        if not data or not isinstance(data, dict):
            return None
        vid = str(data.get("video_id") or "").strip()
        title = str(data.get("title") or "").strip()
        if not vid and not title:
            return None
        return cls(
            video_id=vid,
            title=title,
            artist=str(data.get("artist") or ""),
            url=str(data.get("url") or ""),
            local_path=str(data.get("local_path") or ""),
            artwork=str(data.get("artwork") or ""),
            duration=float(data.get("duration") or 0.0),
            position_seconds=max(0.0, float(data.get("position_seconds") or 0.0)),
            is_playing=bool(data.get("is_playing", False)),
            repeat_mode=str(data.get("repeat_mode") or "off"),
            is_shuffle=bool(data.get("is_shuffle", False)),
            source=str(data.get("source") or "youtube"),
            queue_tracks=list(data.get("queue_tracks") or [])[:50],
            queue_index=max(0, int(data.get("queue_index") or 0)),
            saved_at=float(data.get("saved_at") or time.time()),
        )


class AndroidMediaLifecycleCoordinator:
    """
    Coordinates Android native media lifecycle with PlayerController cleanly on both
    Android (via pyjnius + ForegroundService) and Desktop/Test environments (injectable bridge).
    """

    def __init__(self, controller=None, jni_backend=None):
        self._controller = controller
        self._jni = jni_backend
        self._lock = threading.RLock()

        # Runtime states
        self.has_audio_focus: bool = False
        self.is_ducked: bool = False
        self.paused_by_transient_focus: bool = False
        self.foreground_service_running: bool = False
        self.wakelock_held: bool = False
        self._session_initialized: bool = False

        # Native Android JNI references (populated only on Android or injected mocks)
        self._media_session = None
        self._media_session_cb = None
        self._media_token = None
        self._audio_manager = None
        self._focus_listener = None
        self._focus_request = None
        self._wakelock = None
        self._broadcast_receiver = None

        self._last_state_sync_ts: float = 0.0
        self._state_file_dir: Optional[str] = None
        self._last_service_sig: Optional[tuple] = None

    def bind_controller(self, controller) -> None:
        self._controller = controller

    def _service_state_path(self) -> str:
        if self._state_file_dir:
            return os.path.join(self._state_file_dir, "playback_service_state.json")
        if platform == "android":
            try:
                from kivy.app import App
                app = App.get_running_app()
                if app and getattr(app, "user_data_dir", None):
                    base = os.path.dirname(app.user_data_dir)
                    if base:
                        return os.path.join(base, "files", "playback_service_state.json")
            except Exception:
                pass
        env_dir = os.environ.get("ANDROID_PRIVATE")
        if env_dir:
            return os.path.join(env_dir, "playback_service_state.json")
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache", "playback_service_state.json")

    def _write_service_state(self, state: Dict[str, Any]) -> None:
        try:
            p = self._service_state_path()
            os.makedirs(os.path.dirname(p), exist_ok=True)
            tmp = f"{p}.tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False)
            os.replace(tmp, p)
        except Exception as exc:
            logger.debug("Service state sync write skipped: %s", exc)

    # =========================================================================
    # 1. Native Initialization (MediaSession, Noisy Receiver, WakeLock)
    # =========================================================================
    def ensure_initialized(self) -> bool:
        """Lazily initialize Android MediaSession, AudioFocus listener, WakeLock, and receivers."""
        with self._lock:
            if self._session_initialized:
                return True

        if self._jni is not None:
            ok = self._jni.init_native(self)
            with self._lock:
                self._session_initialized = bool(ok)
            return bool(ok)

        if platform != "android":
            return False

        try:
            from jnius import PythonJavaClass, autoclass, java_method
            from android.broadcast import BroadcastReceiver

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            activity = PythonActivity.mActivity
            if not activity:
                return False

            Context = autoclass("android.content.Context")
            AudioManager = autoclass("android.media.AudioManager")
            MediaSession = autoclass("android.media.session.MediaSession")
            PowerManager = autoclass("android.os.PowerManager")

            self._audio_manager = activity.getSystemService(Context.AUDIO_SERVICE)
            try:
                pm = activity.getSystemService(Context.POWER_SERVICE)
                if pm:
                    self._wakelock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "KivyMusicApp:PlaybackWakeLock")
            except Exception as w_exc:
                logger.warning("Android WakeLock setup skipped: %s", w_exc)

            coord = self

            # Attach native Java MediaSession.Callback bridge on Android MainLooper
            # (Kivy SDLThread has no Looper) so lock-screen Now Bar / Quick Settings play,
            # pause, skip, seek, and Heart/Shuffle actions dispatch cleanly on Android 13-17.
            try:
                ms = MediaSession(activity, "KivyMusicSession")
                ms.setFlags(MediaSession.FLAG_HANDLES_MEDIA_BUTTONS | MediaSession.FLAG_HANDLES_TRANSPORT_CONTROLS)
                try:
                    MediaSessionBridge = autoclass("org.shivam.music.MediaSessionBridge")
                    cb = MediaSessionBridge.attachSession(ms, activity)
                    self._media_session_cb = cb
                    logger.info("Attached native Java MediaSession.Callback bridge on MainLooper")
                except Exception as cb_exc:
                    logger.warning("Native MediaSession.Callback bridge unavailable: %s", cb_exc)
                ms.setActive(True)
                self._media_session = ms
                self._media_token = ms.getSessionToken()
            except Exception as ms_exc:
                logger.warning("Android MediaSession setup skipped: %s", ms_exc)

            try:
                class _AudioFocusCb(PythonJavaClass):
                    __javainterfaces__ = ["android/media/AudioManager$OnAudioFocusChangeListener"]
                    __javacontext__ = "app"

                    @java_method("(I)V")
                    def onAudioFocusChange(self, focus_change):
                        coord.on_os_audio_focus_change(int(focus_change))

                self._focus_listener = _AudioFocusCb()
            except Exception as af_exc:
                logger.warning("Android AudioFocus listener setup skipped: %s", af_exc)

            def _on_broadcast(context, intent):
                try:
                    act = str(intent.getAction() or "")
                    coord.on_os_broadcast(act, intent)
                except Exception as be:
                    logger.warning("Android broadcast handler error: %s", be)

            registered_java_rx = False
            try:
                MediaSessionBridge = autoclass("org.shivam.music.MediaSessionBridge")

                class _MediaBridgeListener(PythonJavaClass):
                    __javainterfaces__ = ["org/shivam/music/MediaSessionBridge$BroadcastListener"]
                    __javacontext__ = "app"

                    @java_method("(Ljava/lang/String;JI)V")
                    def onBroadcastAction(self, action, seek_ms, int_extra):
                        act = str(action or "")
                        if act == ACTION_SEEK and int(seek_ms) >= 0:
                            coord.dispatch_transport_action("seek", float(seek_ms) / 1000.0)
                        elif act == "android.intent.action.HEADSET_PLUG":
                            if int(int_extra) == 0:
                                logger.info("Wired headset unplugged -> pausing playback")
                                Clock.schedule_once(lambda dt: coord._pause_on_route_disconnect(), 0)
                        elif "bluetooth" in act.lower() and "CONNECTION_STATE_CHANGED" in act:
                            if int(int_extra) == 0:
                                logger.info("Bluetooth audio route disconnected -> pausing playback")
                                Clock.schedule_once(lambda dt: coord._pause_on_route_disconnect(), 0)
                        else:
                            coord.on_os_broadcast(act, None)

                listener = _MediaBridgeListener()
                if bool(MediaSessionBridge.registerLifecycleReceiver(activity, listener)):
                    self._broadcast_receiver = listener
                    registered_java_rx = True
                    logger.info("Registered Java MainLooper lifecycle BroadcastReceiver")
            except Exception as jbr_exc:
                logger.debug("Java lifecycle receiver fallback to p4a BroadcastReceiver: %s", jbr_exc)

            if not registered_java_rx:
                try:
                    br = BroadcastReceiver(
                        _on_broadcast,
                        actions=[
                            AudioManager.ACTION_AUDIO_BECOMING_NOISY,
                            "android.intent.action.HEADSET_PLUG",
                            "android.bluetooth.headset.profile.action.CONNECTION_STATE_CHANGED",
                            "android.bluetooth.a2dp.profile.action.CONNECTION_STATE_CHANGED",
                            ACTION_PLAY,
                            ACTION_PAUSE,
                            ACTION_PLAY_PAUSE,
                            ACTION_NEXT,
                            ACTION_PREV,
                            ACTION_STOP,
                            ACTION_SEEK,
                            ACTION_FAVORITE,
                            ACTION_SHUFFLE,
                            ACTION_REQUEST_MEDIA_TOKEN,
                        ],
                    )
                    br.start()
                    self._broadcast_receiver = br
                except Exception as br_exc:
                    logger.warning("Android BroadcastReceiver setup skipped: %s", br_exc)

            self._broadcast_media_token()

            with self._lock:
                self._session_initialized = True
            logger.info("Android MediaSession, AudioFocus & Noisy Receiver initialized")
            return True
        except Exception as exc:
            logger.warning("Android native media init failed (non-fatal): %s", exc)
            return False

    def _broadcast_media_token(self) -> None:
        """Broadcast live MediaSession.Token to `:service_MusicPlayback` for MediaStyle binding."""
        if platform != "android" or not self._media_token:
            return
        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            activity = PythonActivity.mActivity
            if not activity:
                return
            try:
                MediaSessionBridge = autoclass("org.shivam.music.MediaSessionBridge")
                MediaSessionBridge.broadcastToken(activity, self._media_token)
                return
            except Exception:
                pass
            Intent = autoclass("android.content.Intent")
            it = Intent(ACTION_SYNC_MEDIA_TOKEN)
            it.setPackage(activity.getPackageName())
            it.putExtra("media_token", self._media_token)
            activity.sendBroadcast(it)
        except Exception as exc:
            logger.debug("MediaSession token broadcast skipped: %s", exc)

    # =========================================================================
    # 2. Foreground Service Lifecycle + WakeLock Management
    # =========================================================================
    def start_foreground_service(
        self,
        title: str,
        artist: str,
        is_playing: bool,
        album: str = "",
        artwork: str = "",
        is_favorite: bool = False,
        is_shuffle: bool = False,
    ) -> bool:
        """Persist service state and start python-for-android foreground playback service."""
        sig = (
            str(title or "Kivy Music"),
            str(artist or "Playing Audio"),
            bool(is_playing),
            str(album or ""),
            str(artwork or ""),
            bool(is_favorite),
            bool(is_shuffle),
        )
        if sig != self._last_service_sig:
            self._last_service_sig = sig
            self._write_service_state(
                {
                    "title": sig[0],
                    "artist": sig[1],
                    "is_playing": sig[2],
                    "album": sig[3],
                    "artwork": sig[4],
                    "is_favorite": sig[5],
                    "is_shuffle": sig[6],
                    "stop_service": False,
                    "updated_at": time.time(),
                }
            )
            self._broadcast_media_token()
        self._set_wakelock(bool(is_playing))

        if self._jni is not None:
            ok = self._jni.start_service(title, artist, is_playing)
            self.foreground_service_running = bool(ok)
            return bool(ok)

        if platform != "android":
            self.foreground_service_running = False
            return False

        try:
            if not self.foreground_service_running:
                from jnius import autoclass
                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                pkg = PythonActivity.mActivity.getPackageName()
                service_cls = autoclass(f"{pkg}.ServiceMusicplayback")
                service_cls.start(PythonActivity.mActivity, "")
                self.foreground_service_running = True
                logger.info("Started Android ForegroundService MusicPlayback")
                self._broadcast_media_token()
            return True
        except Exception as exc:
            logger.debug("Foreground service start fallback: %s", exc)
            return False

    def stop_foreground_service(self) -> None:
        self._write_service_state({"stop_service": True, "is_playing": False, "updated_at": time.time()})
        self._set_wakelock(False)
        if self._jni is not None:
            self._jni.stop_service()
        elif platform == "android" and self.foreground_service_running:
            try:
                from jnius import autoclass
                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                pkg = PythonActivity.mActivity.getPackageName()
                service_cls = autoclass(f"{pkg}.ServiceMusicplayback")
                service_cls.stop(PythonActivity.mActivity)
            except Exception:
                pass
        self.foreground_service_running = False

    def _set_wakelock(self, acquire: bool) -> None:
        if self._jni is not None and hasattr(self._jni, "set_wakelock"):
            self._jni.set_wakelock(bool(acquire))
            self.wakelock_held = bool(acquire)
            return
        if not self._wakelock:
            self.wakelock_held = False
            return
        try:
            held = bool(self._wakelock.isHeld())
            if acquire and not held:
                self._wakelock.acquire()
                self.wakelock_held = True
            elif not acquire and held:
                self._wakelock.release()
                self.wakelock_held = False
        except Exception:
            self.wakelock_held = False

    # =========================================================================
    # 3. Audio Focus Negotiation & Route-Disconnect Handling
    # =========================================================================
    def request_audio_focus(self) -> bool:
        """
        Request system playback focus before starting playback.
        Returns True if focus is granted (always True on Desktop).
        """
        if self._jni is not None:
            granted = bool(self._jni.request_audio_focus())
            self.has_audio_focus = granted
            return granted

        if platform != "android":
            self.has_audio_focus = True
            return True

        self.ensure_initialized()
        if not self._audio_manager or not self._focus_listener:
            return True

        try:
            from jnius import autoclass
            AudioManager = autoclass("android.media.AudioManager")
            BuildVersion = autoclass("android.os.Build$VERSION")
            sdk_int = int(BuildVersion.SDK_INT)

            if sdk_int >= 26:
                AudioAttributesBuilder = autoclass("android.media.AudioAttributes$Builder")
                AudioAttributes = autoclass("android.media.AudioAttributes")
                FocusReqBuilder = autoclass("android.media.AudioFocusRequest$Builder")
                attrs = (
                    AudioAttributesBuilder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build()
                )
                req = (
                    FocusReqBuilder(AudioManager.AUDIOFOCUS_GAIN)
                    .setAudioAttributes(attrs)
                    .setAcceptsDelayedFocusGain(True)
                    .setOnAudioFocusChangeListener(self._focus_listener)
                    .build()
                )
                self._focus_request = req
                res = int(self._audio_manager.requestAudioFocus(req))
            else:
                res = int(
                    self._audio_manager.requestAudioFocus(
                        self._focus_listener,
                        AudioManager.STREAM_MUSIC,
                        AudioManager.AUDIOFOCUS_GAIN,
                    )
                )

            self.has_audio_focus = (res == AUDIOFOCUS_REQUEST_GRANTED)
            self.is_ducked = False
            self.paused_by_transient_focus = False
            return self.has_audio_focus
        except Exception as exc:
            logger.warning("AudioFocus request error (allowing playback fallback): %s", exc)
            return True

    def abandon_audio_focus(self) -> None:
        self.has_audio_focus = False
        self.is_ducked = False
        if self._jni is not None:
            self._jni.abandon_audio_focus()
            return
        if platform != "android" or not self._audio_manager:
            return
        try:
            if self._focus_request is not None:
                self._audio_manager.abandonAudioFocusRequest(self._focus_request)
            elif self._focus_listener is not None:
                self._audio_manager.abandonAudioFocus(self._focus_listener)
        except Exception:
            pass

    def on_os_audio_focus_change(self, focus_change: int) -> None:
        """Marshal Android OS AudioFocus transitions safely onto the Kivy UI thread."""
        Clock.schedule_once(lambda dt, fc=int(focus_change): self._apply_audio_focus_change(fc), 0)

    def _apply_audio_focus_change(self, focus_change: int) -> None:
        pc = self._controller
        if focus_change == AUDIOFOCUS_LOSS:
            logger.info("AudioFocus LOST permanently -> pausing playback")
            self.has_audio_focus = False
            self.is_ducked = False
            self.paused_by_transient_focus = False
            if pc and pc.is_playing:
                pc.pause()
                self.abandon_audio_focus()
        elif focus_change == AUDIOFOCUS_LOSS_TRANSIENT:
            logger.info("AudioFocus LOST transiently (call/interruption) -> pausing")
            self.has_audio_focus = False
            if pc and pc.is_playing:
                self.paused_by_transient_focus = True
                pc.pause()
        elif focus_change == AUDIOFOCUS_LOSS_TRANSIENT_CAN_DUCK:
            logger.info("AudioFocus DUCK -> lowering gain smoothly")
            self.is_ducked = True
            if pc and hasattr(pc, "audio_engine"):
                pc.audio_engine.set_ducked(True, duck_factor=0.25)
        elif focus_change == AUDIOFOCUS_GAIN:
            logger.info("AudioFocus GAIN -> restoring volume/playback")
            self.has_audio_focus = True
            if self.is_ducked and pc and hasattr(pc, "audio_engine"):
                self.is_ducked = False
                pc.audio_engine.set_ducked(False)
            if self.paused_by_transient_focus:
                self.paused_by_transient_focus = False
                if pc and pc.active_track and not pc.is_playing:
                    pc.play()

    def on_os_broadcast(self, action: str, intent: Any = None) -> None:
        """
        Handle Android noisy-audio / Bluetooth / notification transport intents.
        Can also be invoked directly in unit/integration tests with mock intents.
        """
        act = str(action or "")
        if act == "android.media.AUDIO_BECOMING_NOISY":
            logger.info("ACTION_AUDIO_BECOMING_NOISY received -> pausing immediately")
            Clock.schedule_once(lambda dt: self._pause_on_route_disconnect(), 0)
            return

        if act == "android.intent.action.HEADSET_PLUG" and intent is not None:
            try:
                state = int(intent.getIntExtra("state", -1))
                if state == 0:  # 0 = unplugged
                    logger.info("Wired headset unplugged -> pausing playback")
                    Clock.schedule_once(lambda dt: self._pause_on_route_disconnect(), 0)
            except Exception:
                pass
            return

        if "bluetooth" in act.lower() and "CONNECTION_STATE_CHANGED" in act and intent is not None:
            try:
                # BluetoothProfile.EXTRA_STATE ("android.bluetooth.profile.extra.STATE"): 0 = DISCONNECTED
                bt_state = int(intent.getIntExtra("android.bluetooth.profile.extra.STATE", -1))
                if bt_state == 0:
                    logger.info("Bluetooth audio route disconnected -> pausing playback")
                    Clock.schedule_once(lambda dt: self._pause_on_route_disconnect(), 0)
            except Exception:
                pass
            return

        if act == ACTION_REQUEST_MEDIA_TOKEN:
            self._broadcast_media_token()
            return

        if act == ACTION_PLAY:
            self.dispatch_transport_action("play")
        elif act == ACTION_PAUSE:
            self.dispatch_transport_action("pause")
        elif act == ACTION_PLAY_PAUSE:
            self.dispatch_transport_action("play_pause")
        elif act == ACTION_NEXT:
            self.dispatch_transport_action("next")
        elif act == ACTION_PREV:
            self.dispatch_transport_action("previous")
        elif act == ACTION_STOP:
            self.dispatch_transport_action("stop")
        elif act == ACTION_FAVORITE:
            self.dispatch_transport_action("favorite")
        elif act == ACTION_SHUFFLE:
            self.dispatch_transport_action("shuffle")
        elif act == ACTION_SEEK and intent is not None:
            try:
                seek_ms = int(intent.getLongExtra("seek_ms", -1))
                if seek_ms >= 0:
                    self.dispatch_transport_action("seek", float(seek_ms) / 1000.0)
            except Exception:
                pass

    def _pause_on_route_disconnect(self) -> None:
        self.paused_by_transient_focus = False
        pc = self._controller
        if pc and pc.is_playing:
            pc.pause()

    def dispatch_transport_action(self, command: str, value: float = 0.0) -> None:
        """Marshal MediaSession / Notification / AVRCP buttons cleanly onto Kivy main thread."""
        def _exec(dt):
            pc = self._controller
            if not pc:
                return
            if command == "play":
                if not pc.is_playing:
                    pc.play()
            elif command == "pause":
                if pc.is_playing:
                    pc.pause()
            elif command == "play_pause":
                pc.toggle_play()
            elif command == "next":
                pc.next_track()
            elif command == "previous":
                pc.prev_track()
            elif command == "seek":
                pc.seek(max(0.0, float(value or 0.0)))
            elif command == "favorite":
                pc.toggle_favorite()
            elif command == "shuffle":
                pc.toggle_shuffle()
            elif command == "stop":
                pc.stop()
                self.stop_foreground_service()
                self.abandon_audio_focus()

        Clock.schedule_once(_exec, 0)

    @staticmethod
    def _resolve_artwork_path(raw_art: Any) -> str:
        art = str(raw_art or "").strip()
        if not art or art.startswith(("http://", "https://")):
            return ""
        if os.path.exists(art) and os.path.isfile(art):
            return os.path.abspath(art)
        candidate = os.path.join(os.path.dirname(os.path.dirname(__file__)), art)
        if os.path.exists(candidate) and os.path.isfile(candidate):
            return os.path.abspath(candidate)
        return ""

    # =========================================================================
    # 4. MediaSession Metadata & PlaybackState Synchronization
    # =========================================================================
    def sync_playback_state(
        self,
        track,
        is_playing: bool,
        position_seconds: float,
        duration_seconds: float,
        force: bool = False,
    ) -> None:
        """Update MediaSession metadata, artwork, PlaybackState, CustomActions, WakeLock & ForegroundService."""
        now = time.monotonic()
        if (not force) and (now - self._last_state_sync_ts) < 1.0:
            return
        self._last_state_sync_ts = now

        title = getattr(track, "title", "Kivy Music") if track else "Kivy Music"
        artist = getattr(track, "artist", "") if track else ""
        album = getattr(track, "album", "") if track else ""
        art_path = self._resolve_artwork_path(getattr(track, "album_art", "") if track else "")
        pc = self._controller
        is_fav = bool(getattr(pc, "is_favorite", False) or getattr(track, "is_favorite", False)) if track else False
        is_shuf = bool(getattr(pc, "is_shuffle", False))
        dur_ms = max(0, int(float(duration_seconds or 0.0) * 1000))
        pos_ms = max(0, int(float(position_seconds or 0.0) * 1000))

        self._set_wakelock(bool(is_playing))
        if track and (is_playing or self.foreground_service_running):
            self.start_foreground_service(
                title,
                artist,
                is_playing,
                album=album,
                artwork=art_path,
                is_favorite=is_fav,
                is_shuffle=is_shuf,
            )

        if self._jni is not None:
            self._jni.update_media_session(title, artist, dur_ms, pos_ms, bool(is_playing))
            return

        if platform != "android" or not self._media_session:
            return

        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            activity = PythonActivity.mActivity
            try:
                MediaSessionBridge = autoclass("org.shivam.music.MediaSessionBridge")
                MediaSessionBridge.updateSession(
                    self._media_session,
                    activity,
                    str(title),
                    str(artist),
                    str(album),
                    int(dur_ms),
                    int(pos_ms),
                    bool(is_playing),
                    bool(is_fav),
                    bool(is_shuf),
                    str(art_path),
                )
                return
            except Exception:
                pass

            MediaMetadata = autoclass("android.media.MediaMetadata")
            MediaMetadataBuilder = autoclass("android.media.MediaMetadata$Builder")
            PlaybackState = autoclass("android.media.session.PlaybackState")
            PlaybackStateBuilder = autoclass("android.media.session.PlaybackState$Builder")

            mb = (
                MediaMetadataBuilder()
                .putString(MediaMetadata.METADATA_KEY_TITLE, str(title))
                .putString(MediaMetadata.METADATA_KEY_ARTIST, str(artist))
                .putLong(MediaMetadata.METADATA_KEY_DURATION, dur_ms)
            )
            if album:
                mb.putString(MediaMetadata.METADATA_KEY_ALBUM, str(album))
            if art_path and os.path.exists(art_path):
                try:
                    BitmapFactory = autoclass("android.graphics.BitmapFactory")
                    bmp = BitmapFactory.decodeFile(art_path)
                    if bmp is not None:
                        mb.putBitmap(MediaMetadata.METADATA_KEY_ALBUM_ART, bmp)
                except Exception:
                    pass
            self._media_session.setMetadata(mb.build())

            actions = (
                PlaybackState.ACTION_PLAY
                | PlaybackState.ACTION_PAUSE
                | PlaybackState.ACTION_PLAY_PAUSE
                | PlaybackState.ACTION_SKIP_TO_NEXT
                | PlaybackState.ACTION_SKIP_TO_PREVIOUS
                | PlaybackState.ACTION_SEEK_TO
                | PlaybackState.ACTION_STOP
            )
            state_code = PlaybackState.STATE_PLAYING if is_playing else PlaybackState.STATE_PAUSED
            pstate = (
                PlaybackStateBuilder()
                .setActions(actions)
                .setState(state_code, pos_ms, 1.0 if is_playing else 0.0)
                .build()
            )
            self._media_session.setPlaybackState(pstate)
        except Exception as exc:
            logger.debug("MediaSession state sync skipped: %s", exc)

    # =========================================================================
    # 5. Process-Recreation State Persistence & Restoration
    # =========================================================================
    def persist_snapshot(self, wait: bool = False) -> Optional[PlaybackSessionSnapshot]:
        """Persist current active track, queue, and playhead to SQLite cache_store."""
        pc = self._controller
        if not pc or not pc.active_track:
            return None
        tr = pc.active_track
        queue_dicts = []
        for qt in (pc.queue or [])[:50]:
            try:
                queue_dicts.append(qt.to_dict() if hasattr(qt, "to_dict") else {
                    "video_id": getattr(qt, "video_id", ""),
                    "title": getattr(qt, "title", "Unknown"),
                    "artist": getattr(qt, "artist", "Unknown"),
                    "duration": getattr(qt, "duration", 180),
                    "artwork": getattr(qt, "album_art", ""),
                    "local_path": getattr(qt, "local_path", ""),
                    "url": getattr(qt, "url", ""),
                    "source": getattr(qt, "source", "youtube"),
                })
            except Exception:
                continue

        snap = PlaybackSessionSnapshot(
            video_id=str(getattr(tr, "video_id", "")),
            title=str(getattr(tr, "title", "")),
            artist=str(getattr(tr, "artist", "")),
            url=str(getattr(tr, "url", "")),
            local_path=str(getattr(tr, "local_path", "")),
            artwork=str(getattr(tr, "album_art", "")),
            duration=float(pc.duration or getattr(tr, "duration", 0) or 0.0),
            position_seconds=max(0.0, float(pc.current_time or 0.0)),
            is_playing=bool(pc.is_playing),
            repeat_mode=str(pc.repeat_mode or "off"),
            is_shuffle=bool(pc.is_shuffle),
            source=str(getattr(tr, "source", "youtube")),
            queue_tracks=queue_dicts,
            queue_index=max(0, int(pc.queue_index or 0)),
        )
        try:
            from models.database import save_cache_payload
            save_cache_payload(SNAPSHOT_CACHE_KEY, snap.to_dict(), wait=wait)
        except Exception as exc:
            logger.debug("persist_snapshot failed: %s", exc)
        return snap

    @staticmethod
    def load_saved_snapshot() -> Optional[PlaybackSessionSnapshot]:
        """Load persisted playback snapshot from SQLite for process-recreation recovery."""
        try:
            from models.database import load_cache_payload
            raw = load_cache_payload(SNAPSHOT_CACHE_KEY, None)
            return PlaybackSessionSnapshot.from_dict(raw)
        except Exception:
            return None

    def restore_saved_session(self) -> Optional[PlaybackSessionSnapshot]:
        """
        Restore queue, active track, repeat/shuffle settings, and saved timeline
        position cleanly onto PlayerController after OS process recreation (paused
        safely so audio does not startle the user unexpectedly).
        """
        pc = self._controller
        if not pc:
            return None
        snap = self.load_saved_snapshot()
        if not snap:
            return None

        from models.track_model import TrackModel
        queue_objs = [TrackModel.from_dict(d) for d in snap.queue_tracks if isinstance(d, dict)]
        active = None
        if queue_objs:
            if 0 <= snap.queue_index < len(queue_objs):
                cand = queue_objs[snap.queue_index]
                if not snap.video_id or cand.video_id == snap.video_id:
                    active = cand
            if active is None and snap.video_id:
                active = next((q for q in queue_objs if q.video_id == snap.video_id), None)

        if active is None:
            active = TrackModel.from_dict({
                "video_id": snap.video_id,
                "title": snap.title,
                "artist": snap.artist,
                "url": snap.url,
                "local_path": snap.local_path,
                "artwork": snap.artwork,
                "duration": int(snap.duration or 180),
                "source": snap.source,
            })
            if not queue_objs:
                queue_objs = [active]

        pc.is_shuffle = bool(snap.is_shuffle)
        pc.repeat_mode = snap.repeat_mode if snap.repeat_mode in ("off", "all", "one") else "off"
        pc.is_repeat = (pc.repeat_mode in ("all", "one"))
        pc.audio_engine.repeat_one = (pc.repeat_mode == "one")
        pc.set_custom_queue(queue_objs, start_track=active)
        pc.set_track(active)
        # Restore playhead metadata cleanly in paused state
        pos = min(snap.position_seconds, snap.duration) if snap.duration > 0 else snap.position_seconds
        pc.current_time = float(pos)
        active.current_time = float(pos)
        sec = max(0, int(pos))
        m, s = divmod(sec, 60)
        pc.formatted_current_time = f"{m:02d}:{s:02d}"
        pc.is_playing = False
        logger.info("Restored playback snapshot: '%s' at %s", active.title, pc.formatted_current_time)
        return snap

    def release(self) -> None:
        self.stop_foreground_service()
        self.abandon_audio_focus()
        if self._broadcast_receiver:
            try:
                self._broadcast_receiver.stop()
            except Exception:
                pass
            self._broadcast_receiver = None
        if self._media_session:
            try:
                self._media_session.setActive(False)
                self._media_session.release()
            except Exception:
                pass
            self._media_session = None
        with self._lock:
            self._session_initialized = False
