from kivy.event import EventDispatcher
from kivy.properties import StringProperty, NumericProperty

class TrackModel(EventDispatcher):
    title = StringProperty("Unknown Title")
    artist = StringProperty("Unknown Artist")
    album_art = StringProperty("album_art.png")
    duration = NumericProperty(100) # seconds
    current_time = NumericProperty(0)
    lyrics = StringProperty("These are some dummy lyrics...\nLine 2\nLine 3\nLine 4\nJust for testing!")

    @property
    def formatted_current_time(self):
        m, s = divmod(int(self.current_time), 60)
        return f"{m:02d}:{s:02d}"
        
    @property
    def formatted_duration(self):
        m, s = divmod(int(self.duration), 60)
        return f"{m:02d}:{s:02d}"
class PlaylistModel(EventDispatcher):
    # A simple list of TrackModels
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracks = [
            TrackModel(title="Song 1", artist="Artist A", duration=180),
            TrackModel(title="Song 2", artist="Artist B", duration=210),
            TrackModel(title="Song 3", artist="Artist C", duration=150),
        ]

