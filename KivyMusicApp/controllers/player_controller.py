import os
import random
import threading
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from models.track_model import TrackModel
from models.database import is_favorite, toggle_favorite, mark_track_played, update_local_track_path
from services.audio_engine import AudioEngine
from services.discord_rpc_service import DiscordRPCService
from utils.theme_utils import update_theme_from_image

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
        self.audio_engine.on_error = self._on_audio_error
        self.audio_engine.on_track_loaded = self._on_audio_track_loaded
        self.audio_engine.on_sponsorblock_skipped = self._on_sponsorblock_skipped
        self.audio_engine.on_crossfade_trigger = self._on_crossfade_trigger

        self.discord_rpc = DiscordRPCService()
        self._pre_mute_volume = 1.0

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
        """Toggle active track favorite status in SQLite database."""
        if not self.active_track:
            return
        vid = getattr(self.active_track, "video_id", "")
        if vid:
            new_status = toggle_favorite(vid)
            self.is_favorite = new_status
            self.active_track.is_favorite = new_status
        else:
            self.is_favorite = not self.is_favorite
            self.active_track.is_favorite = self.is_favorite

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
        if self.active_track:
            self.active_track.current_time = 0.0
        if track in self.queue:
            self.queue_index = self.queue.index(track)
        else:
            self.queue.append(track)
            self.user_ordered_queue.append(track)
            self.queue_index = len(self.queue) - 1
        vid = getattr(track, "video_id", "")
        if vid:
            self.is_favorite = is_favorite(vid)
            self.active_track.is_favorite = self.is_favorite
            mark_track_played(vid)
        else:
            self.is_favorite = getattr(track, "is_favorite", False)
            self.active_track.is_favorite = self.is_favorite

    def play(self):
        """Explicitly starts or resumes playback of the active track."""
        if not self.active_track:
            return
        if self.audio_engine.paused and self.audio_engine.player:
            self.audio_engine.unpause()
            self.is_playing = True
            if self.discord_rpc and self.active_track:
                self.discord_rpc.update_track(
                    self.active_track.title,
                    self.active_track.artist,
                    self.current_time,
                    self.duration,
                    True
                )
        else:
            target_src = getattr(self.active_track, "local_path", "") or getattr(self.active_track, "url", "")
            track_meta = {
                "id": getattr(self.active_track, "video_id", ""),
                "title": self.active_track.title,
                "artist": self.active_track.artist,
                "duration": self.active_track.duration,
                "artwork": self.active_track.album_art
            }
            # If target_src is empty or doesn't exist, check local bundled art/demo
            if not target_src and hasattr(self.active_track, "video_id") and self.active_track.video_id:
                target_src = f"https://www.youtube.com/watch?v={self.active_track.video_id}"

            started = self.audio_engine.start_play(target_src, track_meta)
            self.is_playing = bool(started)
            if self.discord_rpc and self.active_track:
                self.discord_rpc.update_track(
                    self.active_track.title,
                    self.active_track.artist,
                    0.0,
                    self.duration,
                    True
                )

    def toggle_play(self):
        if not self.active_track:
            return

        if self.is_playing:
            self.audio_engine.pause()
            self.is_playing = False
            if self.discord_rpc and self.active_track:
                self.discord_rpc.update_track(
                    self.active_track.title,
                    self.active_track.artist,
                    self.current_time,
                    self.duration,
                    False
                )
        else:
            self.play()

    def seek(self, pos: float):
        """Seek to position in seconds."""
        self.current_time = float(pos)
        sec = max(0, int(pos or 0))
        m, s = divmod(sec, 60)
        self.formatted_current_time = f"{m:02d}:{s:02d}"
        if self.active_track:
            self.active_track.current_time = pos
        self.audio_engine.seek(pos)

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

    def stop(self):
        self.is_playing = False
        if self.discord_rpc:
            self.discord_rpc.clear()
        self.audio_engine.cleanup_player()

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
        """Triggered when track reaches crossfade window before ending."""
        # Pre-cache next track if in queue
        next_t = self.get_next_track()
        if next_t and hasattr(next_t, "video_id") and next_t.video_id:
            vid = next_t.video_id
            from services.audio_engine import get_cache_dir
            cp = os.path.join(get_cache_dir(), f"{vid}.mp3")
            if not os.path.exists(cp):
                from utils.media_utils import fetch_youtube_metadata
                threading.Thread(
                    target=lambda: fetch_youtube_metadata(f"https://www.youtube.com/watch?v={vid}", extract_flat=True),
                    daemon=True
                ).start()

    # AudioEngine Callbacks
    def _on_audio_time_update(self, elapsed, duration):
        if not self.is_seeking:
            self.current_time = float(elapsed)
            sec = max(0, int(elapsed or 0))
            m, s = divmod(sec, 60)
            self.formatted_current_time = f"{m:02d}:{s:02d}"
            if duration > 0:
                self.duration = float(duration)
                dsec = max(0, int(duration or 0))
                dm, ds = divmod(dsec, 60)
                self.formatted_duration = f"{dm:02d}:{ds:02d}"
        if self.active_track and not self.is_seeking:
            self.active_track.current_time = elapsed
            if duration > 0 and self.active_track.duration != duration:
                self.active_track.duration = duration

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

    def _on_audio_error(self, err_msg):
        self.status_text = f"Error: {err_msg}"
        print(f"[PlayerController] Audio error: {err_msg}")

    def _on_audio_track_loaded(self, path, info):
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
