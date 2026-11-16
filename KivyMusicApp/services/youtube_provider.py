"""
YouTube Music Provider.
Stream extraction, caching, and catalog search via yt-dlp.
"""
import os
import re
from typing import List, Dict, Optional, Any
from services.music_provider_base import BaseMusicProvider
from yt_dlp import YoutubeDL

class SilentLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

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
        """Performs fast flat search on YouTube using yt-dlp."""
        if not query:
            return []
        
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'skip_download': True,
            'noplaylist': True,
            'logger': SilentLogger(),
            'default_search': 'ytsearch',
            'socket_timeout': 10,
        }
        search_target = f"ytsearch{min(limit, 30)}:{query}"
        tracks: List[Dict[str, Any]] = []

        try:
            with YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(search_target, download=False)
                entries = result.get('entries', []) if result else []
                for entry in entries:
                    if not entry:
                        continue
                    vid = entry.get('id')
                    if not vid or len(vid) != 11:
                        continue
                    title = entry.get('title') or "Unknown Title"
                    artist = entry.get('uploader') or entry.get('channel') or "YouTube Artist"
                    duration = int(entry.get('duration', 0) or 0)
                    thumb = entry.get('thumbnail') or ""
                    tracks.append({
                        "video_id": vid,
                        "source_id": vid,
                        "title": title,
                        "artist": artist,
                        "duration": duration,
                        "artwork": thumb or "album_art.png",
                        "url": f"https://www.youtube.com/watch?v={vid}",
                        "source": "youtube",
                        "bitrate": 128,
                        "stream_url": "",
                    })
        except Exception as e:
            print(f"[YouTubeProvider] search error: {e}")

        return tracks

    def get_track_details(self, track_id: str) -> Optional[Dict[str, Any]]:
        """Extracts complete metadata for a YouTube track."""
        vid = self.extract_video_id(track_id)
        if not vid:
            return None
        url = f"https://www.youtube.com/watch?v={vid}"
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'skip_download': True,
            'logger': SilentLogger(),
            'socket_timeout': 10,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    return {
                        "video_id": vid,
                        "source_id": vid,
                        "title": info.get('title', "Unknown"),
                        "artist": info.get('uploader', "YouTube Artist"),
                        "duration": int(info.get('duration', 0) or 0),
                        "artwork": info.get('thumbnail', "album_art.png"),
                        "url": url,
                        "source": "youtube",
                        "bitrate": 128,
                    }
        except Exception as e:
            print(f"[YouTubeProvider] get_track_details failed for {vid}: {e}")
        return None

    def get_stream_url(self, track_id_or_url: str, quality: str = "320") -> Optional[Dict[str, Any]]:
        """Resolves raw direct audio stream URL via yt-dlp."""
        vid = self.extract_video_id(track_id_or_url)
        url = f"https://www.youtube.com/watch?v={vid}" if vid else track_id_or_url
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'skip_download': True,
            'logger': SilentLogger(),
            'socket_timeout': 10,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info and info.get('url'):
                    return {
                        "url": info['url'],
                        "bitrate": int(info.get('abr', 128) or 128),
                        "format": info.get('ext', 'm4a'),
                        "source": "youtube"
                    }
        except Exception as e:
            print(f"[YouTubeProvider] get_stream_url error: {e}")
        return None

    def get_playlist(self, playlist_id_or_url: str) -> Optional[Dict[str, Any]]:
        """Extracts playlist items from YouTube."""
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'skip_download': True,
            'logger': SilentLogger(),
            'socket_timeout': 12,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist_id_or_url, download=False)
                if info:
                    entries = info.get('entries', [])
                    tracks = []
                    for e in entries:
                        if not e: continue
                        vid = e.get('id')
                        if not vid: continue
                        tracks.append({
                            "video_id": vid,
                            "source_id": vid,
                            "title": e.get('title', "Unknown"),
                            "artist": e.get('uploader', "YouTube Artist"),
                            "duration": int(e.get('duration', 0) or 0),
                            "artwork": e.get('thumbnail', "album_art.png"),
                            "url": f"https://www.youtube.com/watch?v={vid}",
                            "source": "youtube",
                            "bitrate": 128,
                        })
                    return {
                        "id": info.get('id', 'yt_playlist'),
                        "title": info.get('title', 'YouTube Playlist'),
                        "artwork": info.get('thumbnail', 'album_art.png'),
                        "tracks": tracks,
                        "source": "youtube"
                    }
        except Exception as e:
            print(f"[YouTubeProvider] get_playlist error: {e}")
        return None
