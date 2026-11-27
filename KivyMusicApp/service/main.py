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


def _build_and_post_notification(service_obj, state: dict, media_token=None) -> None:
    """Create or update Android MediaStyle notification linked to MediaSession.Token and call startForeground()."""
    from jnius import autoclass

    BuildVersion = autoclass("android.os.Build$VERSION")
    sdk_int = int(BuildVersion.SDK_INT)

    title = str(state.get("title") or "Kivy Music")
    artist = str(state.get("artist") or "Playing Audio")
    album = str(state.get("album") or "")
    art_path = str(state.get("artwork") or "")
    is_playing = bool(state.get("is_playing", False))
    is_favorite = bool(state.get("is_favorite", False))
    is_shuffle = bool(state.get("is_shuffle", False))

    notif = None
    try:
        MediaSessionBridge = autoclass("org.shivam.music.MediaSessionBridge")
        notif = MediaSessionBridge.buildMediaNotification(
            service_obj,
            NOTIFICATION_CHANNEL_ID,
            title,
            artist,
            album,
            bool(is_playing),
            bool(is_favorite),
            bool(is_shuffle),
            art_path,
            media_token,
        )
    except Exception:
        notif = None

    if notif is None:
        Context = autoclass("android.content.Context")
        Intent = autoclass("android.content.Intent")
        PendingIntent = autoclass("android.app.PendingIntent")
        NotificationBuilder = autoclass("android.app.Notification$Builder")
        NotificationManager = autoclass("android.app.NotificationManager")
        Notification = autoclass("android.app.Notification")
        MediaStyle = autoclass("android.app.Notification$MediaStyle")

        notif_mgr = service_obj.getSystemService(Context.NOTIFICATION_SERVICE)
        if sdk_int >= 26:
            NotificationChannel = autoclass("android.app.NotificationChannel")
            chan = NotificationChannel(
                NOTIFICATION_CHANNEL_ID,
                "Music Playback",
                NotificationManager.IMPORTANCE_LOW,
            )
            chan.setDescription("Active audio playback & lock screen media controls")
            chan.setShowBadge(False)
            chan.setLockscreenVisibility(Notification.VISIBILITY_PUBLIC)
            notif_mgr.createNotificationChannel(chan)
            builder = NotificationBuilder(service_obj, NOTIFICATION_CHANNEL_ID)
        else:
            builder = NotificationBuilder(service_obj)

        builder.setContentTitle(title)
        builder.setContentText(artist)
        builder.setOngoing(is_playing)
        builder.setOnlyAlertOnce(True)
        builder.setVisibility(Notification.VISIBILITY_PUBLIC)
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
            R_drawable = autoclass("android.R$drawable")
            builder.addAction(int(R_drawable.ic_media_previous), "Previous", _action_pi("org.shivam.music.ACTION_PREV", 101))
            builder.addAction(
                int(R_drawable.ic_media_pause if is_playing else R_drawable.ic_media_play),
                "Pause" if is_playing else "Play",
                _action_pi("org.shivam.music.ACTION_PLAY_PAUSE", 102),
            )
            builder.addAction(int(R_drawable.ic_media_next), "Next", _action_pi("org.shivam.music.ACTION_NEXT", 103))
            style = MediaStyle()
            if media_token is not None:
                style.setMediaSession(media_token)
            style.setShowActionsInCompactView(0, 1, 2)
            builder.setStyle(style)
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

    token_holder = [None]
    receiver = None
    try:
        from android.broadcast import BroadcastReceiver
        Intent = autoclass("android.content.Intent")

        def _on_service_broadcast(context, intent):
            try:
                act = str(intent.getAction() or "")
                if act == "org.shivam.music.ACTION_SYNC_MEDIA_TOKEN":
                    tok = intent.getParcelableExtra("media_token")
                    if tok is not None:
                        token_holder[0] = tok
            except Exception:
                pass

        receiver = BroadcastReceiver(
            _on_service_broadcast,
            actions=["org.shivam.music.ACTION_SYNC_MEDIA_TOKEN"],
            use_intent_action=True,
        )
        receiver.start()
    except Exception:
        # Some p4a versions do not accept `use_intent_action` kwarg; retry cleanly with positional signature
        try:
            from android.broadcast import BroadcastReceiver

            def _on_service_broadcast_compat(context, intent):
                try:
                    act = str(intent.getAction() or "")
                    if act == "org.shivam.music.ACTION_SYNC_MEDIA_TOKEN":
                        tok = intent.getParcelableExtra("media_token")
                        if tok is not None:
                            token_holder[0] = tok
                except Exception:
                    pass

            receiver = BroadcastReceiver(
                _on_service_broadcast_compat,
                actions=["org.shivam.music.ACTION_SYNC_MEDIA_TOKEN"],
            )
            receiver.start()
        except Exception:
            receiver = None

    try:
        Intent = autoclass("android.content.Intent")
        req = Intent("org.shivam.music.ACTION_REQUEST_MEDIA_TOKEN")
        req.setPackage(service.getPackageName())
        service.sendBroadcast(req)
    except Exception:
        pass

    last_sig = None
    while True:
        state = _read_service_state()
        if state.get("stop_service"):
            if receiver is not None:
                try:
                    receiver.stop()
                except Exception:
                    pass
            try:
                service.stopForeground(True)
                service.stopSelf()
            except Exception:
                pass
            break

        sig = (
            state.get("title"),
            state.get("artist"),
            state.get("album"),
            state.get("artwork"),
            bool(state.get("is_playing")),
            bool(state.get("is_favorite")),
            bool(state.get("is_shuffle")),
            bool(token_holder[0] is not None),
        )
        if sig != last_sig:
            try:
                _build_and_post_notification(service, state, media_token=token_holder[0])
                last_sig = sig
            except Exception:
                pass

        time.sleep(0.35)


if __name__ == "__main__":
    run_foreground_loop()
