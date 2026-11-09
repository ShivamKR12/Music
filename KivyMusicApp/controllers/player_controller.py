import random
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, BooleanProperty
from models.track_model import TrackModel

class PlayerController(EventDispatcher):
    active_track = ObjectProperty(None, allownone=True)
    is_playing = BooleanProperty(False)
    is_shuffle = BooleanProperty(False)
    is_repeat = BooleanProperty(False)
    is_favorite = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.play_event = None

    def set_playlist(self, playlist_model):
        self.playlist_model = playlist_model

    def toggle_shuffle(self):
        """Toggle playlist shuffle mode."""
        self.is_shuffle = not self.is_shuffle

    def toggle_repeat(self):
        """Toggle track repeat mode."""
        self.is_repeat = not self.is_repeat

    def toggle_favorite(self):
        """Toggle active track favorite status."""
        self.is_favorite = not self.is_favorite

    def set_track(self, track: TrackModel):
        self.active_track = track
        self.active_track.current_time = 0
        self.is_playing = False
        if self.play_event:
            self.play_event.cancel()

    def next_track(self):
        if not self.playlist_model or not self.playlist_model.tracks or not self.active_track:
            return
        if self.is_shuffle and len(self.playlist_model.tracks) > 1:
            candidates = [t for t in self.playlist_model.tracks if t != self.active_track]
            next_track = random.choice(candidates)
        else:
            idx = self.playlist_model.tracks.index(self.active_track)
            next_idx = (idx + 1) % len(self.playlist_model.tracks)
            next_track = self.playlist_model.tracks[next_idx]
            
        self.set_track(next_track)
        from kivymd.app import MDApp
        MDApp.get_running_app().play_selected_track(self.active_track)

    def prev_track(self):
        if not self.playlist_model or not self.playlist_model.tracks or not self.active_track:
            return
        idx = self.playlist_model.tracks.index(self.active_track)
        prev_idx = (idx - 1) % len(self.playlist_model.tracks)
        self.set_track(self.playlist_model.tracks[prev_idx])
        from kivymd.app import MDApp
        MDApp.get_running_app().play_selected_track(self.active_track)

    def toggle_play(self):
        if not self.active_track:
            return

        self.is_playing = not self.is_playing
        
        if self.is_playing:
            self.play_event = Clock.schedule_interval(self._update_time, 1)
        else:
            if self.play_event:
                self.play_event.cancel()

    def _update_time(self, dt):
        if self.active_track:
            if self.active_track.current_time < self.active_track.duration:
                self.active_track.current_time += 1
            else:
                if self.is_repeat:
                    self.active_track.current_time = 0
                else:
                    self.next_track()
