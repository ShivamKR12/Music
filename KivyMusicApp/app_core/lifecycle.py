"""Application Lifecycle Coordinator (Pause, Resume, Restore, Smooth Exit & Stop)."""

from __future__ import annotations

from typing import Any

from kivy.clock import Clock

from models.database import flush_db_writes
from services.logger import app_logger


class ApplicationLifecycle:
    """Coordinates Android/Desktop background lifecycle hooks and graceful shutdown."""

    def __init__(self, app: Any):
        self.app = app

    def on_request_close(self, *args, **kwargs) -> bool:
        """Intercept window close requests to perform smooth exit sequence."""
        if not getattr(self.app, "_is_exiting", False):
            self.smooth_exit()
            return True
        return False

    def smooth_exit(self) -> None:
        """Gracefully fade out audio and UI before stopping the application."""
        app = self.app
        if getattr(app, "_is_exiting", False):
            return
        app._is_exiting = True

        if hasattr(app, "player_controller") and app.player_controller:
            try:
                app.player_controller.fade_out_and_stop(duration=0.25)
            except Exception as e:
                app_logger.debug(f"Audio fadeout error: {e}")

        from kivy.animation import Animation
        if hasattr(app, "root") and app.root:
            anim = Animation(opacity=0.0, duration=0.25, t="out_quad")

            def _finish_exit(*args):
                Clock.schedule_once(lambda dt: app.stop(), 0)

            anim.bind(on_complete=_finish_exit)
            anim.start(app.root)
            Clock.schedule_once(lambda dt: app.stop(), 0.35)
        else:
            app.stop()

    def on_pause(self) -> bool:
        """
        Kivy/Android background lifecycle hook: persist active playback snapshot and
        sync ForegroundService + MediaSession while keeping audio alive (`return True`).
        """
        app = self.app
        try:
            if hasattr(app, "player_controller") and app.player_controller:
                pc = app.player_controller
                pc.persist_session_snapshot(wait=False)
                if pc.active_track:
                    pc.media_lifecycle.sync_playback_state(
                        pc.active_track, pc.is_playing, pc.current_time, pc.duration, force=True
                    )
            flush_db_writes(timeout=1.5)
        except Exception as e:
            app_logger.debug("on_pause lifecycle sync skipped: %s", e)
        return True

    def on_resume(self) -> None:
        """Re-synchronize MediaSession and UI player state after returning from background."""
        app = self.app
        try:
            if hasattr(app, "player_controller") and app.player_controller:
                pc = app.player_controller
                if pc.active_track:
                    pc.media_lifecycle.sync_playback_state(
                        pc.active_track, pc.is_playing, pc.current_time, pc.duration, force=True
                    )
        except Exception as e:
            app_logger.debug("on_resume lifecycle sync skipped: %s", e)

    def restore_last_session(self):
        """Restore previously interrupted playback session snapshot into paused PlayerController."""
        app = self.app
        if not hasattr(app, "player_controller") or not app.player_controller:
            return None
        snap = app.player_controller.restore_session_snapshot()
        if snap and app.player_controller.active_track:
            app.mini_player_dismissed = False
            app.mini_player_visible = True
            app.sync_player_carousel_track(app.player_controller.active_track)
        return snap

    def on_stop(self) -> None:
        """Clean up audio streams, persist session, flush queued SQLite writes, and stop workers."""
        app = self.app
        try:
            Clock.unschedule(app._telemetry_sample_frame)
            Clock.unschedule(app._telemetry_sample_memory)
        except Exception:
            pass
        if hasattr(app, "player_controller") and app.player_controller:
            app.player_controller.stop()
        try:
            flush_db_writes(timeout=3.0)
        except Exception:
            pass
