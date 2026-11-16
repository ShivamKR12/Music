"""
Base Music Provider Interface.
Defines the standard contract for music catalog search, metadata extraction,
and stream URL resolution across diverse providers (YouTube, Spotify, JioSaavn).
"""
import abc
from typing import List, Dict, Optional, Any

class BaseMusicProvider(abc.ABC):
    """Abstract interface implemented by all concrete music streaming and metadata providers."""

    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Searches the provider for tracks matching query.
        Returns a list of track metadata dictionaries.
        """
        pass

    @abc.abstractmethod
    def get_track_details(self, track_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetches detailed metadata for a single track.
        """
        pass

    @abc.abstractmethod
    def get_stream_url(self, track_id_or_url: str, quality: str = "320") -> Optional[Dict[str, Any]]:
        """
        Resolves a playable direct HTTP audio stream URL or yt-dlp stream descriptor.
        Returns dict with: {"url": str, "bitrate": int, "format": str, "source": str}
        """
        pass

    @abc.abstractmethod
    def get_playlist(self, playlist_id_or_url: str) -> Optional[Dict[str, Any]]:
        """
        Extracts playlist metadata and its tracklist.
        Returns dict with: {"id": str, "title": str, "artwork": str, "tracks": List[dict]}
        """
        pass
