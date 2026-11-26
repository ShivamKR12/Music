"""
Python-for-Android Background Media Playback Foreground Service (`MusicPlayback`).

Runs when launched via `android.AndroidService` on Android devices to keep audio
playback active in the background with a persistent Media notification.
Status: Designed & Implemented; runtime execution on Android OS is unverified
without a physical device (`adb`).
"""

import json
import os
import time

try:
    from kivy.utils import platform
except Exception:
    platform = "unknown"


NOTIFICATION_CHANNEL_ID = "kivymusic_playback_channel"
NOTIFICATION_ID = 4109
SERVICE_STATE_FILENAME = "playback_service_state.json"


def _service_state_path() -> str:
    env_dir = os.environ.get("ANDROID_PRIVATE") or os.path.dirname(os.path.dirname(__file__))
    return os.path.join(env_dir, SERVICE_STATE_FILENAME)


def _read_service_state() -> dict:
    path = _service_state_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f) or {}
    except Exception:
        return {}


def _build_and_post_notification(service_obj, state: dict) -> None:
    """Create or update Android Media notification and call startForeground()."""
    from jnius import autoclass

    Context = autoclass("android.content.Context")
    Intent = autoclass("android.content.Intent")
    PendingIntent = autoclass("android.app.PendingIntent")
    NotificationBuilder = autoclass("android.app.Notification$Builder")
    NotificationManager = autoclass("android.app.NotificationManager")
    BuildVersion = autoclass("android.os.Build$VERSION")

    sdk_int = int(BuildVersion.SDK_INT)
    notif_mgr = service_obj.getSystemService(Context.NOTIFICATION_SERVICE)

    if sdk_int >= 26:
        NotificationChannel = autoclass("android.app.NotificationChannel")
        chan = NotificationChannel(
            NOTIFICATION_CHANNEL_ID,
            "Music Playback",
            NotificationManager.IMPORTANCE_LOW,
        )
        chan.setDescription("Active audio playback transport controls")
        chan.setShowBadge(False)
        notif_mgr.createNotificationChannel(chan)
        builder = NotificationBuilder(service_obj, NOTIFICATION_CHANNEL_ID)
    else:
        builder = NotificationBuilder(service_obj)

    title = str(state.get("title") or "Kivy Music")
    artist = str(state.get("artist") or "Playing Audio")
    is_playing = bool(state.get("is_playing", False))

    builder.setContentTitle(title)
    builder.setContentText(artist)
    builder.setOngoing(is_playing)
    builder.setOnlyAlertOnce(True)
    try:
        app_info = service_obj.getApplicationInfo()
        builder.setSmallIcon(int(app_info.icon))
    except Exception:
        pass

    flags = PendingIntent.FLAG_UPDATE_CURRENT | (PendingIntent.FLAG_IMMUTABLE if sdk_int >= 23 else 0)
    pkg = service_obj.getPackageName()

    def _action_pi(action_name: str, req_code: int):
        it = Intent(action_name)
        it.setPackage(pkg)
        return PendingIntent.getBroadcast(service_obj, req_code, it, flags)

    try:
        builder.addAction(0, "Prev", _action_pi("org.shivam.music.ACTION_PREV", 101))
        builder.addAction(0, "Pause" if is_playing else "Play", _action_pi("org.shivam.music.ACTION_PLAY_PAUSE", 102))
        builder.addAction(0, "Next", _action_pi("org.shivam.music.ACTION_NEXT", 103))
    except Exception:
        pass

    notif = builder.build()
    try:
        if sdk_int >= 29:
            ServiceInfo = autoclass("android.content.pm.ServiceInfo")
            service_obj.startForeground(
                NOTIFICATION_ID,
                notif,
                ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK,
            )
        else:
            service_obj.startForeground(NOTIFICATION_ID, notif)
    except Exception:
        service_obj.startForeground(NOTIFICATION_ID, notif)


def run_foreground_loop() -> None:
    """Entry loop executed by python-for-android service process."""
    if platform != "android":
        return

    from jnius import autoclass

    PythonService = autoclass("org.kivy.android.PythonService")
    service = PythonService.mService
    if service is None:
        return

    try:
        service.setAutoRestartService(False)
    except Exception:
        pass

    last_sig = None
    while True:
        state = _read_service_state()
        if state.get("stop_service"):
            try:
                service.stopForeground(True)
                service.stopSelf()
            except Exception:
                pass
            break

        sig = (state.get("title"), state.get("artist"), bool(state.get("is_playing")))
        if sig != last_sig:
            try:
                _build_and_post_notification(service, state)
                last_sig = sig
            except Exception:
                pass

        time.sleep(0.75)


if __name__ == "__main__":
    run_foreground_loop()
