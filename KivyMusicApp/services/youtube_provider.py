"""
YouTube Music Provider.
Stream extraction, caching, and catalog search via yt-dlp.
"""
import re
from typing import List, Dict, Optional, Any
from services.music_provider_base import BaseMusicProvider
from services.logger import get_logger
from services.youtube_extractor import (
    YtdlpLogBridge,
    SilentLogger,
    YouTubeExtractionError,
    get_youtube_extractor,
    redact_sensitive_text,
)
from utils.media_utils import parse_complete_media_metadata

logger = get_logger("YouTubeProvider")


class YouTubeProvider(BaseMusicProvider):
    """Concrete provider for YouTube / YouTube Music audio extraction via yt-dlp."""

    def __init__(self):
        super().__init__(name="youtube")

    @staticmethod
    def extract_video_id(url_or_id: str) -> str:
        """Extracts YouTube 11-char video ID from URL or bare ID."""
        if not url_or_id:
            return ""
        if len(url_or_id) == 11 and not ("/" in url_or_id or "=" in url_or_id):
            return url_or_id
        if "v=" in url_or_id:
            return url_or_id.split("v=")[-1].split("&")[0]
        if "youtu.be/" in url_or_id:
            return url_or_id.split("youtu.be/")[-1].split("?")[0]
        cleaned = re.sub(r'[^a-zA-Z0-9_-]', '', url_or_id)
        return cleaned[:11] if cleaned else "unknown"

    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Performs resilient flat search on YouTube via hardened YouTubeExtractor."""
        if not query:
            return []

        search_target = f"ytsearch{min(limit, 30)}:{query}"
        tracks: List[Dict[str, Any]] = []

        try:
            result = get_youtube_extractor().extract_metadata(search_target, extract_flat=True)
            entries = result.get("entries", []) if result else []
            for entry in entries:
                if not entry:
                    continue
                meta = parse_complete_media_metadata(entry)
                if meta and meta.get("video_id"):
                    tracks.append(meta)
        except Exception as e:
            logger.error("Search error: %s", redact_sensitive_text(e))

        return tracks

    def get_track_details(self, track_id: str) -> Optional[Dict[str, Any]]:
        """Extracts complete metadata for a YouTube track."""
        vid = self.extract_video_id(track_id)
        if not vid:
            return None
        url = f"https://www.youtube.com/watch?v={vid}"
        try:
            info = get_youtube_extractor().extract_metadata(url, extract_flat=True)
            if info:
                meta = parse_complete_media_metadata(info)
                if meta and meta.get("video_id"):
                    return meta
        except Exception as e:
            logger.error("get_track_details failed for %s: %s", vid, redact_sensitive_text(e))
        return None

    def get_stream_url(
        self,
        track_id_or_url: str,
        quality: str = "320",
        force_refresh: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """Resolves validated direct audio stream URL + expiry via YouTubeExtractor."""
        vid = self.extract_video_id(track_id_or_url)
        url = f"https://www.youtube.com/watch?v={vid}" if vid else track_id_or_url
        try:
            extracted = get_youtube_extractor().extract_stream(url, force_refresh=force_refresh)
            if extracted and extracted.get("url"):
                return {
                    "url": extracted["url"],
                    "bitrate": int(extracted.get("abr", 128) or 128),
                    "format": extracted.get("ext", "m4a"),
                    "source": "youtube",
                    "expires_at": float(extracted.get("expires_at") or 0.0),
                    "client_tier": extracted.get("client_tier", ""),
                }
        except YouTubeExtractionError as e:
            logger.error("get_stream_url error (%s): %s", e.code, e.user_message)
        except Exception as e:
            logger.error("get_stream_url error: %s", redact_sensitive_text(e))
        return None

    def get_playlist(self, playlist_id_or_url: str) -> Optional[Dict[str, Any]]:
        """Extracts playlist items from YouTube via hardened YouTubeExtractor."""
        try:
            info = get_youtube_extractor().extract_metadata(playlist_id_or_url, extract_flat=True)
            if info:
                entries = info.get("entries", [])
                tracks = []
                for e in entries:
                    if not e:
                        continue
                    meta = parse_complete_media_metadata(e)
                    if meta and meta.get("video_id"):
                        tracks.append(meta)
                return {
                    "id": info.get("id", "yt_playlist"),
                    "title": info.get("title", "YouTube Playlist"),
                    "artwork": info.get("thumbnail", "album_art.png"),
                    "tracks": tracks,
                    "source": "youtube",
                }
        except Exception as e:
            logger.error("get_playlist error: %s", redact_sensitive_text(e))
        return None
