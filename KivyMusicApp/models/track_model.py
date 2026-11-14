import os
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from models.database import get_all_tracks, add_track, is_favorite, init_db

class TrackModel(EventDispatcher):
    video_id = StringProperty("")
    title = StringProperty("Unknown Title")
    artist = StringProperty("Unknown Artist")
    url = StringProperty("")
    album_art = StringProperty("album_art.png")
    local_path = StringProperty("")
    duration = NumericProperty(180) # seconds
    current_time = NumericProperty(0)
    lyrics = StringProperty("")
    is_favorite = BooleanProperty(False)
    is_downloaded = BooleanProperty(False)
    is_loading = BooleanProperty(False)
    download_progress = StringProperty("")

    @property
    def formatted_current_time(self):
        m, s = divmod(int(self.current_time), 60)
        return f"{m:02d}:{s:02d}"

    @property
    def formatted_duration(self):
        m, s = divmod(int(self.duration), 60)
        return f"{m:02d}:{s:02d}"

    @classmethod
    def from_dict(cls, data: dict):
        """Build TrackModel instance from database or dictionary, auto-resolving cached files."""
        vid = data.get("video_id") or data.get("id") or ""

        # Check cache directory for local audio and artwork
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache")
        cached_mp3 = os.path.join(cache_dir, f"{vid}.mp3") if vid else ""
        cached_art = os.path.join(cache_dir, f"{vid}.jpg") if vid else ""

        local_path = data.get("local_path", "")
        if not local_path or not os.path.exists(local_path):
            if cached_mp3 and os.path.exists(cached_mp3):
                local_path = cached_mp3

        art = data.get("artwork") or data.get("album_art") or ""
        if not art or not os.path.exists(art) or art == "album_art.png":
            if cached_art and os.path.exists(cached_art):
                art = cached_art
            elif vid:
                try:
                    from utils.media_utils import get_thumbnail_path
                    art = get_thumbnail_path(vid, cache_dir)
                except Exception:
                    art = "album_art.png"
            elif not art or not os.path.exists(art):
                art = "album_art.png"

        return cls(
            video_id=vid,
            title=data.get("title", "Unknown Title"),
            artist=data.get("artist", "Unknown Artist"),
            url=data.get("url", f"https://www.youtube.com/watch?v={vid}" if vid else ""),
            album_art=art,
            local_path=local_path,
            duration=int(data.get("duration", 180)),
            is_favorite=is_favorite(vid) if vid else False,
            is_downloaded=bool(local_path and os.path.exists(local_path)),
        )

DEFAULT_TRACKS_SEED = [
    {
        "video_id": "zxbDTgRivGI",
        "title": "Angreji Beat",
        "artist": "Yo Yo Honey Singh, Gippy Grewal",
        "url": "https://www.youtube.com/watch?v=zxbDTgRivGI",
        "duration": 210,
        "artwork": "album_art.png"
    },
    {
        "video_id": "AEt0xGoLxNk",
        "title": "Dope Shope",
        "artist": "Yo Yo Honey Singh, Deep Money",
        "url": "https://www.youtube.com/watch?v=AEt0xGoLxNk",
        "duration": 189,
        "artwork": "album_art2.png"
    },
    {
        "video_id": "0tnbKiLiPt0",
        "title": "Brown Rang",
        "artist": "Yo Yo Honey Singh",
        "url": "https://www.youtube.com/watch?v=0tnbKiLiPt0",
        "duration": 179,
        "artwork": "album_art.png"
    },
]

class PlaylistModel(EventDispatcher):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracks = []
        self.load_from_db()

    def load_from_db(self):
        """Load tracks from SQLite database, ensuring default seed tracks exist."""
        init_db()
        db_tracks = get_all_tracks()
        existing_vids = {t["video_id"] for t in db_tracks} if db_tracks else set()
        seeded_any = False
        for item in DEFAULT_TRACKS_SEED:
            if item["video_id"] not in existing_vids:
                add_track(
                    video_id=item["video_id"],
                    title=item["title"],
                    artist=item["artist"],
                    url=item["url"],
                    duration=item["duration"],
                    artwork=item["artwork"]
                )
                seeded_any = True

        if seeded_any or not db_tracks:
            db_tracks = get_all_tracks()

        self.tracks = [TrackModel.from_dict(t) for t in db_tracks]

    def add_track(self, track: TrackModel):
        """Append track if not already in playlist."""
        if track not in self.tracks:
            self.tracks.append(track)
            add_track(
                video_id=track.video_id,
                title=track.title,
                artist=track.artist,
                url=track.url,
                duration=track.duration,
                artwork=track.album_art,
                local_path=track.local_path
            )

    def find_track(self, video_id: str):
        """Find a track in playlist by video_id."""
        for t in self.tracks:
            if t.video_id == video_id:
                return t
        return None

    def get_track_by_video_id(self, video_id: str):
        """Alias for find_track."""
        return self.find_track(video_id)
