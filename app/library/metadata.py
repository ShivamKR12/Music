# library/metadata.py

class Song:
    def __init__(
        self,
        title,
        artist="Unknown",
        album="Unknown",
        duration=0,
        source="local",
        file_path=None,
        artwork_path=None,
        song_id=None
    ):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.source = source
        self.file_path = file_path
        self.artwork_path = artwork_path
        self.id = song_id
