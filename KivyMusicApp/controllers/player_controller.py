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
    is_favorite = BooleanProperty(False)
    is_loading = BooleanProperty(False)
    status_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.playlist_model = None
        self.audio_engine = AudioEngine()
        self.audio_engine.on_time_update = self._on_audio_time_update
        self.audio_engine.on_track_end = self._on_audio_track_end
        self.audio_engine.on_artwork_loaded = self._on_audio_artwork_loaded
        self.audio_engine.on_loading = self._on_audio_loading
        self.audio_engine.on_download_progress = self._on_audio_download_progress
        self.audio_engine.on_error = self._on_audio_error

    def set_playlist(self, playlist_model):
        self.playlist_model = playlist_model

    def toggle_shuffle(self):
        """Toggle playlist shuffle mode."""
        self.is_shuffle = not self.is_shuffle

    def toggle_repeat(self):
        """Toggle track repeat mode."""
        self.is_repeat = not self.is_repeat
        self.audio_engine.repeat_one = self.is_repeat

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
        self.active_track = track
        self.active_track.current_time = 0
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

    def next_track(self):
        if not self.playlist_model or not self.playlist_model.tracks or not self.active_track:
            return
        if self.is_shuffle and len(self.playlist_model.tracks) > 1:
            candidates = [t for t in self.playlist_model.tracks if t != self.active_track]
            next_t = random.choice(candidates)
        else:
            idx = self.playlist_model.tracks.index(self.active_track)
            next_idx = (idx + 1) % len(self.playlist_model.tracks)
            next_t = self.playlist_model.tracks[next_idx]

        self.set_track(next_t)
        from kivymd.app import MDApp
        MDApp.get_running_app().play_selected_track(self.active_track)

    def prev_track(self):
        if not self.playlist_model or not self.playlist_model.tracks or not self.active_track:
            return
        idx = self.playlist_model.tracks.index(self.active_track)
        prev_idx = (idx - 1) % len(self.playlist_model.tracks)
        next_t = self.playlist_model.tracks[prev_idx]

        self.set_track(next_t)
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
