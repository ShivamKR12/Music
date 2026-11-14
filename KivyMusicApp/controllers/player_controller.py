import os
import random
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from models.track_model import TrackModel
from models.database import is_favorite, toggle_favorite, mark_track_played, update_local_track_path
from services.audio_engine import AudioEngine
from utils.theme_utils import update_theme_from_image

class PlayerController(EventDispatcher):
    active_track = ObjectProperty(None, allownone=True)
    is_playing = BooleanProperty(False)
    is_shuffle = BooleanProperty(False)
    is_repeat = BooleanProperty(False)
    repeat_mode = StringProperty("off")
    is_favorite = BooleanProperty(False)
    is_loading = BooleanProperty(False)
    status_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.playlist_model = None
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
            return
        if self.is_shuffle:
            current = self.active_track or (self.queue[self.queue_index] if self.queue else None)
            rest = [t for t in self.user_ordered_queue if t != current]
            random.shuffle(rest)
            self.queue = ([current] if current else []) + rest
            self.queue_index = 0
        else:
            self.queue = list(self.user_ordered_queue)
            self.queue_index = self.queue.index(self.active_track) if self.active_track in self.queue else 0

    def cycle_repeat_mode(self):
        """Cycles through repeat modes: off -> all -> one -> off."""
        modes = ["off", "all", "one"]
        self.repeat_mode = modes[(modes.index(self.repeat_mode) + 1) % len(modes)]
        self.is_repeat = (self.repeat_mode in ("all", "one"))
        self.audio_engine.repeat_one = (self.repeat_mode == "one")
        return self.repeat_mode

    def toggle_repeat(self):
        """Toggle track repeat mode."""
        self.cycle_repeat_mode()

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
        self.active_track.current_time = 0
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

    def toggle_play(self):
        if not self.active_track:
            return

        if self.is_playing:
            self.audio_engine.pause()
            self.is_playing = False
        else:
            self.play()

    def seek(self, pos: float):
        """Seek to position in seconds."""
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
        MDApp.get_running_app().play_selected_track(self.active_track)

    def prev_track(self):
        prev_t = self.get_prev_track()
        if not prev_t:
            return
        self.set_track(prev_t)
        from kivymd.app import MDApp
        MDApp.get_running_app().play_selected_track(self.active_track)

    def stop(self):
        self.is_playing = False
        self.audio_engine.cleanup_player()

    # AudioEngine Callbacks
    def _on_audio_time_update(self, elapsed, duration):
        if self.active_track:
            self.active_track.current_time = elapsed
            if duration > 0:
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
