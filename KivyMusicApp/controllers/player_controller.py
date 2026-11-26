import os
import random
import threading
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from models.track_model import TrackModel
from models.database import (
    is_favorite, toggle_favorite, mark_track_played,
    record_track_skip, update_local_track_path
)
from services.android_media_lifecycle import AndroidMediaLifecycleCoordinator
from services.audio_engine import AudioEngine
from services.discord_rpc_service import DiscordRPCService
from services.logger import get_logger
from utils.theme_utils import update_theme_from_image

logger = get_logger("PlayerController")

class PlayerController(EventDispatcher):
    playlist_model = ObjectProperty(None, allownone=True)
    active_track = ObjectProperty(None, allownone=True)
    is_playing = BooleanProperty(False)
    is_shuffle = BooleanProperty(False)
    is_repeat = BooleanProperty(False)
    repeat_mode = StringProperty("off")
    is_favorite = BooleanProperty(False)
    is_loading = BooleanProperty(False)
    is_seeking = BooleanProperty(False)
    buffer_progress = NumericProperty(0.0)
    buffer_time = NumericProperty(0.0)
    status_text = StringProperty("")
    current_time = NumericProperty(0.0)
    duration = NumericProperty(180.0)
    formatted_current_time = StringProperty("00:00")
    formatted_duration = StringProperty("03:00")
    volume = NumericProperty(1.0)
    is_muted = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, "playlist_model") or self.playlist_model is None:
            self.playlist_model = kwargs.get("playlist_model", None)
        self.queue = []
        self.user_ordered_queue = []
        self.queue_index = 0
        self.audio_engine = AudioEngine()
        self.audio_engine.on_time_update = self._on_audio_time_update
        self.audio_engine.on_track_end = self._on_audio_track_end
        self.audio_engine.on_artwork_loaded = self._on_audio_artwork_loaded
        self.audio_engine.on_loading = self._on_audio_loading
        self.audio_engine.on_download_progress = self._on_audio_download_progress
        self.audio_engine.on_buffer_update = self._on_audio_buffer_update
        self.audio_engine.on_buffer_metrics = self._on_audio_buffer_metrics
        self.audio_engine.on_error = self._on_audio_error
        self.audio_engine.on_track_loaded = self._on_audio_track_loaded
        self.audio_engine.on_sponsorblock_skipped = self._on_sponsorblock_skipped
        self.audio_engine.on_crossfade_trigger = self._on_crossfade_trigger
        self.audio_engine.on_crossfade_track_advanced = self._on_crossfade_track_advanced

        self.discord_rpc = DiscordRPCService()
        self.media_lifecycle = AndroidMediaLifecycleCoordinator(self)
        self._pre_mute_volume = 1.0
        self._manual_stopped = True
        self._consecutive_error_skips = 0

    def set_playlist(self, playlist_model):
        self.playlist_model = playlist_model
        self.rebuild_queue()

    def set_custom_queue(self, tracks: list, start_track=None):
        """Sets an explicit ordered playback queue (e.g. from an active playlist or offline scan)."""
        if not tracks:
            return
        self.user_ordered_queue = list(tracks)
        if self.is_shuffle and start_track and start_track in tracks:
            rest = [t for t in tracks if t != start_track]
            random.shuffle(rest)
            self.queue = [start_track] + rest
            self.queue_index = 0
        else:
            self.queue = list(tracks)
            self.queue_index = self.queue.index(start_track) if (start_track and start_track in self.queue) else 0
        if start_track and start_track in self.queue:
            self.active_track = start_track

    def rebuild_queue(self):
        """Rebuilds internal ordered and shuffled playback queues."""
        tracks = list(self.playlist_model.tracks) if self.playlist_model and hasattr(self.playlist_model, 'tracks') else []
        self.user_ordered_queue = list(tracks)
        if self.is_shuffle and self.active_track in tracks:
            rest = [t for t in tracks if t != self.active_track]
            random.shuffle(rest)
            self.queue = [self.active_track] + rest
            self.queue_index = 0
        else:
            self.queue = list(tracks)
            self.queue_index = self.queue.index(self.active_track) if self.active_track in self.queue else 0

    def toggle_shuffle(self):
        """Toggle playlist shuffle mode preserving non-repeating queue order."""
        self.is_shuffle = not self.is_shuffle
        if not self.queue:
            self.rebuild_queue()
        elif self.is_shuffle:
            current = self.active_track or (self.queue[self.queue_index] if self.queue else None)
            rest = [t for t in self.user_ordered_queue if t != current]
            random.shuffle(rest)
            self.queue = ([current] if current else []) + rest
            self.queue_index = 0
        else:
            self.queue = list(self.user_ordered_queue)
            self.queue_index = self.queue.index(self.active_track) if self.active_track in self.queue else 0

        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if app and hasattr(app, "show_toast"):
            msg = "Shuffle ON: Tracks randomized" if self.is_shuffle else "Shuffle OFF: Playing sequentially"
            app.show_toast(msg)

    def cycle_repeat_mode(self):
        """Cycles through repeat modes: off -> all -> one -> off."""
        modes = ["off", "all", "one"]
        self.repeat_mode = modes[(modes.index(self.repeat_mode) + 1) % len(modes)]
        self.is_repeat = (self.repeat_mode in ("all", "one"))
        self.audio_engine.repeat_one = (self.repeat_mode == "one")

        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if app and hasattr(app, "show_toast"):
            if self.repeat_mode == "one":
                msg = "Repeat: Current Track"
            elif self.repeat_mode == "all":
                msg = "Repeat: All Tracks in Queue"
            else:
                msg = "Repeat: OFF"
            app.show_toast(msg)

        return self.repeat_mode

    def toggle_repeat(self):
        """Toggle track repeat mode."""
        self.cycle_repeat_mode()

    def set_volume(self, val: float):
        """Sets master volume level in range [0.0, 1.0]."""
        self.volume = max(0.0, min(1.0, float(val)))
        if self.volume > 0.0:
            self.is_muted = False
        self.audio_engine.set_volume(self.volume)

    def toggle_mute(self):
        """Toggles audio mute state."""
        self.is_muted = not self.is_muted
        if self.is_muted:
            self._pre_mute_volume = self.volume if self.volume > 0 else 1.0
            self.audio_engine.set_muted(True)
        else:
            self.audio_engine.set_muted(False)
            if self.volume == 0:
                self.set_volume(self._pre_mute_volume)

    def adjust_volume(self, delta: float):
        """Adjusts master volume by delta (+0.05 / -0.05)."""
        new_vol = max(0.0, min(1.0, self.volume + delta))
        self.set_volume(new_vol)

    def toggle_favorite(self):
        """Toggle active track favorite status in SQLite database optimistically."""
        if not self.active_track:
            return
        vid = getattr(self.active_track, "video_id", "")
        target_status = not self.is_favorite
        # 1. Optimistic UI update in the current frame (<1ms latency)
        self.is_favorite = target_status
        self.active_track.is_favorite = target_status

        if vid:
            # 2. Asynchronous disk persistence; safely reconciles or rolls back on error
            def _async_db():
                try:
                    new_status = toggle_favorite(vid)
                    if new_status != target_status:
                        def _sync_back(dt):
                            self.is_favorite = new_status
                            if self.active_track:
                                self.active_track.is_favorite = new_status
                        Clock.schedule_once(_sync_back, 0)
                except Exception:
                    def _revert_err(dt):
                        self.is_favorite = not target_status
                        if self.active_track:
                            self.active_track.is_favorite = not target_status
                    Clock.schedule_once(_revert_err, 0)

            threading.Thread(target=_async_db, daemon=True).start()

    def set_track(self, track: TrackModel):
        if self.active_track != track:
            self.audio_engine.cleanup_player()
        self.active_track = track
        self.current_time = 0.0
        self.formatted_current_time = "00:00"
        dur = float(getattr(track, "duration", 0) or 180.0)
        self.duration = dur
        dsec = max(0, int(dur))
        dm, ds = divmod(dsec, 60)
        self.formatted_duration = f"{dm:02d}:{ds:02d}"
        is_dl = getattr(track, "is_downloaded", False) or bool(getattr(track, "local_path", "") and os.path.exists(getattr(track, "local_path", "")))
        self.buffer_progress = 1.0 if is_dl else 0.0
        self.buffer_time = dur if is_dl else 0.0
        if self.active_track:
            self.active_track.current_time = 0.0
        if track in self.queue:
            self.queue_index = self.queue.index(track)
        else:
            self.queue.append(track)
            self.user_ordered_queue.append(track)
            self.queue_index = len(self.queue) - 1
        vid = getattr(track, "video_id", "")
        self.is_favorite = getattr(track, "is_favorite", False)
        if vid:
            # Asynchronously verify database favorite status & record play count without blocking the UI thread
            def _async_track_init(t_vid, target_track):
                try:
                    db_fav = is_favorite(t_vid)
                    mark_track_played(t_vid)
                    if db_fav != getattr(target_track, "is_favorite", False):
                        def _sync_fav(dt):
                            if self.active_track == target_track:
                                self.is_favorite = db_fav
                            target_track.is_favorite = db_fav
                        Clock.schedule_once(_sync_fav, 0)
                except Exception:
                    pass
            threading.Thread(target=_async_track_init, args=(vid, track), daemon=True).start()
        else:
            self.active_track.is_favorite = self.is_favorite

    def play(self):
        """Explicitly starts or resumes playback without blocking the main UI thread."""
        if not self.active_track:
            return
        if not self.media_lifecycle.request_audio_focus():
            logger.warning("OS declined audio focus; holding playback cleanly")
            self.is_playing = False
            return
        self._manual_stopped = False
        if not getattr(self, "_advancing_from_error", False):
            self._consecutive_error_skips = 0
        self._advancing_from_error = False
        if self.audio_engine.paused and self.audio_engine.player:
            self.audio_engine.unpause()
            self.is_playing = True
            self.media_lifecycle.sync_playback_state(
                self.active_track, True, self.current_time, self.duration, force=True
            )
            if self.discord_rpc and self.active_track:
                t_title, t_artist, t_cur, t_dur = self.active_track.title, self.active_track.artist, self.current_time, self.duration
                Clock.schedule_once(lambda dt: self.discord_rpc.update_track(t_title, t_artist, t_cur, t_dur, True), 0)
        else:
            track_meta = self.active_track.to_dict() if hasattr(self.active_track, "to_dict") else {
                "video_id": getattr(self.active_track, "video_id", ""),
                "title": self.active_track.title,
                "artist": self.active_track.artist,
                "duration": self.active_track.duration,
                "artwork": self.active_track.album_art,
                "local_path": getattr(self.active_track, "local_path", ""),
                "url": getattr(self.active_track, "url", ""),
                "source": getattr(self.active_track, "source", "youtube"),
            }
            # Resolve remote streams asynchronously off the Kivy UI thread
            started = self.audio_engine.resolve_and_play_track(track_meta)
            self.is_playing = bool(started)
            self.media_lifecycle.sync_playback_state(
                self.active_track, self.is_playing, 0.0, self.duration, force=True
            )
            if self.discord_rpc and self.active_track:
                t_title, t_artist, t_dur = self.active_track.title, self.active_track.artist, self.duration
                Clock.schedule_once(lambda dt: self.discord_rpc.update_track(t_title, t_artist, 0.0, t_dur, True), 0)

    def toggle_play(self):
        if not self.active_track:
            return

        if self.is_playing:
            self.audio_engine.pause()
            self.is_playing = False
            self.media_lifecycle.sync_playback_state(
                self.active_track, False, self.current_time, self.duration, force=True
            )
            self.media_lifecycle.persist_snapshot(wait=False)
            if self.discord_rpc and self.active_track:
                t_title, t_artist, t_cur, t_dur = self.active_track.title, self.active_track.artist, self.current_time, self.duration
                Clock.schedule_once(lambda dt: self.discord_rpc.update_track(t_title, t_artist, t_cur, t_dur, False), 0)
        else:
            self.play()

    def pause(self):
        """Explicitly pauses playback of the active track if currently playing."""
        if self.is_playing:
            self.toggle_play()

    def seek(self, pos: float):
        """Seek to position in seconds."""
        self.current_time = float(pos)
        sec = max(0, int(pos or 0))
        m, s = divmod(sec, 60)
        self.formatted_current_time = f"{m:02d}:{s:02d}"
        if self.active_track:
            self.active_track.current_time = pos
        self.audio_engine.seek(pos)
        self.media_lifecycle.sync_playback_state(
            self.active_track, self.is_playing, self.current_time, self.duration, force=True
        )

    def get_next_track(self):
        """Calculates next track based on queue and repeat mode without random repeating."""
        if not self.queue:
            if self.playlist_model and hasattr(self.playlist_model, 'tracks') and self.playlist_model.tracks:
                self.rebuild_queue()
            else:
                return None
        if not self.queue:
            return None
        if self.repeat_mode == "one":
            return self.active_track or self.queue[self.queue_index]
        next_idx = self.queue_index + 1
        if next_idx >= len(self.queue):
            if self.repeat_mode in ("all", "off"):
                next_idx = 0
            else:
                return None
        return self.queue[next_idx]

    def get_prev_track(self):
        """Calculates previous track based on queue order."""
        if not self.queue:
            if self.playlist_model and hasattr(self.playlist_model, 'tracks') and self.playlist_model.tracks:
                self.rebuild_queue()
            else:
                return None
        if not self.queue:
            return None
        prev_idx = self.queue_index - 1
        if prev_idx < 0:
            prev_idx = (len(self.queue) - 1) if self.repeat_mode == "all" else 0
        return self.queue[prev_idx]

    def next_track(self):
        # Record genuine early-skip behavioral telemetry if user skipped an actively playing track early
        if (
            self.is_playing
            and self.active_track
            and not getattr(self, "_advancing_from_error", False)
            and float(self.current_time or 0.0) >= 0.5
        ):
            vid = getattr(self.active_track, "video_id", "")
            dur = float(self.duration or getattr(self.active_track, "duration", 0) or 0.0)
            played = float(self.current_time or 0.0)
            if vid and played < 30.0 and (dur <= 0 or played < dur * 0.35):
                threading.Thread(
                    target=lambda v=vid, l=played, d=dur: record_track_skip(v, l, d),
                    daemon=True,
                ).start()
        next_t = self.get_next_track()
        if not next_t:
            self.is_playing = False
            return
        self.set_track(next_t)
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if app and hasattr(app, "play_selected_track"):
            app.play_selected_track(self.active_track)

    def prev_track(self):
        prev_t = self.get_prev_track()
        if not prev_t:
            return
        self.set_track(prev_t)
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if app and hasattr(app, "play_selected_track"):
            app.play_selected_track(self.active_track)

    def persist_session_snapshot(self, wait: bool = False):
        return self.media_lifecycle.persist_snapshot(wait=wait)

    def restore_session_snapshot(self):
        return self.media_lifecycle.restore_saved_session()

    def stop(self):
        self._manual_stopped = True
        self._consecutive_error_skips = 0
        self.is_playing = False
        self.is_loading = False
        self.media_lifecycle.persist_snapshot(wait=False)
        self.media_lifecycle.release()
        if self.discord_rpc:
            self.discord_rpc.clear()
        self.audio_engine.cleanup_player(cancel_workers=True)

    def fade_out_and_stop(self, duration: float = 0.25, on_complete=None):
        """Gradually fades out playback volume over duration, then cleanly halts audio engine."""
        self.is_playing = False
        if self.discord_rpc:
            self.discord_rpc.clear()
        if hasattr(self.audio_engine, "fade_out") and self.audio_engine.player:
            def _done():
                self.audio_engine.cleanup_player()
                if on_complete:
                    on_complete()
            self.audio_engine.fade_out(duration=duration, on_complete=_done)
        else:
            self.audio_engine.cleanup_player()
            if on_complete:
                on_complete()

    def set_equalizer(self, bands: list, reverb: bool = False):
        """Passes 10-band equalizer settings to the underlying AudioEngine."""
        if hasattr(self, "audio_engine") and self.audio_engine:
            self.audio_engine.set_equalizer(bands, reverb)

    def set_crossfade_duration(self, seconds: float):
        """Sets the DJ-style crossfade duration on the audio engine."""
        if hasattr(self, "audio_engine") and self.audio_engine:
            self.audio_engine.crossfade_duration = max(0.0, float(seconds))

    def _on_sponsorblock_skipped(self, start_pos: float, end_pos: float):
        """Callback when SponsorBlock automatically skips a non-music segment."""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if app and hasattr(app, "show_toast"):
            Clock.schedule_once(
                lambda dt: app.show_toast(f"Skipped non-music segment ({start_pos:.0f}s - {end_pos:.0f}s)"),
                0
            )

    def _on_crossfade_trigger(self):
        """Triggered ahead of track conclusion: stages Deck B cleanly for equal-power crossfade."""
        if self.repeat_mode == "one":
            return
        next_t = self.get_next_track()
        if not next_t or next_t == self.active_track:
            return
        next_dict = next_t.to_dict() if hasattr(next_t, "to_dict") else {
            "video_id": getattr(next_t, "video_id", ""),
            "title": getattr(next_t, "title", ""),
            "artist": getattr(next_t, "artist", ""),
            "duration": getattr(next_t, "duration", 0),
            "artwork": getattr(next_t, "album_art", ""),
            "local_path": getattr(next_t, "local_path", ""),
            "url": getattr(next_t, "url", ""),
            "source": getattr(next_t, "source", "youtube"),
        }
        self.audio_engine.stage_next_deck(next_dict)

    def _on_crossfade_track_advanced(self, next_info: dict):
        """Advance active_track and queue index seamlessly after Deck B promotion."""
        next_t = self.get_next_track()
        if not next_t:
            return
        self.active_track = next_t
        if next_t in self.queue:
            self.queue_index = self.queue.index(next_t)
        dur = float(getattr(next_t, "duration", 0) or (next_info or {}).get("duration") or 180.0)
        self.duration = dur
        dsec = max(0, int(dur))
        dm, ds = divmod(dsec, 60)
        self.formatted_duration = f"{dm:02d}:{ds:02d}"
        vid = getattr(next_t, "video_id", "")
        self.is_favorite = is_favorite(vid) if vid else getattr(next_t, "is_favorite", False)
        if vid:
            threading.Thread(target=lambda: mark_track_played(vid), daemon=True).start()
        if self.discord_rpc:
            self.discord_rpc.update_track(next_t.title, next_t.artist, 0.0, self.duration, True)

    # AudioEngine Callbacks
    def _on_audio_time_update(self, elapsed, duration):
        if float(elapsed or 0.0) >= 2.0 and self._consecutive_error_skips:
            self._consecutive_error_skips = 0
        if not self.is_seeking:
            self.current_time = float(elapsed)
            sec = max(0, int(elapsed or 0))
            if getattr(self, "_last_disp_sec", -1) != sec:
                self._last_disp_sec = sec
                m, s = divmod(sec, 60)
                self.formatted_current_time = f"{m:02d}:{s:02d}"
            if duration > 0:
                self.duration = float(duration)
                dsec = max(0, int(duration or 0))
                if getattr(self, "_last_disp_dur_sec", -1) != dsec:
                    self._last_disp_dur_sec = dsec
                    dm, ds = divmod(dsec, 60)
                    self.formatted_duration = f"{dm:02d}:{ds:02d}"
        if self.active_track and not self.is_seeking:
            self.active_track.current_time = elapsed
            if duration > 0 and self.active_track.duration != duration:
                self.active_track.duration = duration
            self.media_lifecycle.sync_playback_state(
                self.active_track, self.is_playing, self.current_time, self.duration, force=False
            )

    def _on_audio_track_end(self):
        if self.is_repeat:
            if self.active_track:
                self.active_track.current_time = 0
            self.toggle_play()
        else:
            self.next_track()

    def _on_audio_artwork_loaded(self, art_path):
        if self.active_track and art_path and os.path.exists(art_path):
            self.active_track.album_art = art_path
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            if not app or getattr(app, "extract_artwork_colors", True):
                update_theme_from_image(art_path)

    def _on_audio_loading(self, is_loading):
        self.is_loading = is_loading
        if self.active_track:
            self.active_track.is_loading = is_loading

    def _on_audio_download_progress(self, percent_str):
        self.status_text = f"Downloading: {percent_str}"
        if self.active_track:
            self.active_track.download_progress = percent_str

    def _on_audio_buffer_update(self, progress: float):
        self.buffer_progress = max(0.0, min(1.0, float(progress or 0.0)))
        if self.duration > 0:
            self.buffer_time = self.buffer_progress * self.duration

    def _on_audio_buffer_metrics(self, metrics):
        self.buffer_progress = max(0.0, min(1.0, float(metrics.download_progress or 0.0)))
        if metrics.playable_buffer_seconds > 0:
            self.buffer_time = float(metrics.playable_buffer_seconds)
        elif self.duration > 0:
            self.buffer_time = self.buffer_progress * self.duration

    def _on_audio_error(self, err_msg):
        from services.youtube_extractor import redact_sensitive_text
        clean_err = redact_sensitive_text(err_msg) or "Playback error"
        self.status_text = f"Error: {clean_err}"
        self.is_playing = False
        self.is_loading = False
        if self.active_track:
            self.active_track.is_loading = False
        logger.error("Audio error: %s", clean_err)

        try:
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            if app and hasattr(app, "show_toast"):
                Clock.schedule_once(lambda dt, m=clean_err: app.show_toast(m), 0)
        except Exception:
            pass

        # Fail-safe queue protection: skip dead/blocked track up to 3 consecutive items without infinite looping
        if (
            not getattr(self, "_manual_stopped", True)
            and len(self.queue) > 1
            and self.repeat_mode != "one"
        ):
            max_skips = min(3, len(self.queue) - 1)
            if getattr(self, "_consecutive_error_skips", 0) < max_skips:
                self._consecutive_error_skips = getattr(self, "_consecutive_error_skips", 0) + 1
                logger.warning(
                    "Fail-safe queue protection advancing past unplayable track (%d/%d)",
                    self._consecutive_error_skips, max_skips,
                )
                Clock.schedule_once(lambda dt: self._safe_advance_after_error(), 0.25)
            else:
                logger.warning("Halted queue auto-skip after %d consecutive extraction failures.", max_skips)

    def _safe_advance_after_error(self):
        if getattr(self, "_manual_stopped", True) or len(self.queue) <= 1:
            return
        self._advancing_from_error = True
        self.next_track()
        try:
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            if not (app and hasattr(app, "play_selected_track")):
                self.play()
        except Exception:
            pass
        self._advancing_from_error = False

    def _on_audio_track_loaded(self, path, info):
        """Mark offline persistence strictly when a verified non-.part file completed on disk."""
        is_complete_file = bool(path and not str(path).endswith(".part") and os.path.exists(path))
        if not is_complete_file:
            return
        self.buffer_progress = 1.0
        self.buffer_time = self.duration
        if self.active_track:
            self.active_track.local_path = path
            self.active_track.is_downloaded = True
            art = info.get("artwork") if info else None
            if art and os.path.exists(art):
                self.active_track.album_art = art
            vid = getattr(self.active_track, "video_id", "")
            if vid:
                dur = info.get("duration", 0) if info else getattr(self.active_track, "duration", 0)
                try:
                    update_local_track_path(vid, path, dur)
                except Exception:
                    pass
