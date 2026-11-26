"""
JioSaavn Music Provider.
Direct unauthenticated search, metadata extraction, and 320kbps CD-quality
direct AAC/MP4 streaming via JioSaavn CDN and pure-Python DES-ECB URL decryption.
Compatible with Windows Desktop, Linux, macOS, and Android.
"""
import os
import re
import html
import base64
import threading
import requests
from typing import List, Dict, Optional, Any
from services.music_provider_base import BaseMusicProvider
from services.logger import get_logger
from utils.des import des, ECB, PAD_PKCS5

logger = get_logger("JioSaavnProvider")

JIOSAAVN_API_BASE = "https://www.jiosaavn.com/api.php"
DES_CIPHER_KEY = b"38346591"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

class JioSaavnProvider(BaseMusicProvider):
    """Concrete provider for JioSaavn regional and high-fidelity 320kbps audio."""

    def __init__(self):
        super().__init__(name="jiosaavn")
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self._des_local = threading.local()

    def _get_des_cipher(self):
        """Return a thread-local DES-ECB cipher instance (pyDes mutates per-instance state)."""
        cipher = getattr(self._des_local, "cipher", None)
        if cipher is None:
            cipher = des(DES_CIPHER_KEY, ECB, padmode=PAD_PKCS5)
            self._des_local.cipher = cipher
        return cipher

    def _decrypt_media_url(self, encrypted_url: str, quality: str = "320") -> Optional[str]:
        """Decrypts JioSaavn's DES-ECB encrypted media string to direct AAC/MP4 CDN stream."""
        if not encrypted_url:
            return None
        try:
            raw_bytes = base64.b64decode(encrypted_url.strip())
            decrypted = self._get_des_cipher().decrypt(raw_bytes, padmode=PAD_PKCS5).decode("utf-8")
            # Upgrade audio bitrate quality suffix if applicable
            target_suffix = f"_{quality}.mp4" if quality in ("320", "160", "96") else "_320.mp4"
            for sfx in ["_96.mp4", "_160.mp4", "_320.mp4", ".mp4"]:
                if sfx in decrypted:
                    return decrypted.replace(sfx, target_suffix)
            return decrypted
        except Exception as e:
            logger.warning("DES decryption error: %s", e)
            return None

    def _clean_text(self, text: Any) -> str:
        """Unescapes HTML entities and normalizes string formatting."""
        if not text:
            return ""
        return html.unescape(str(text)).strip()

    def _upgrade_artwork(self, image_url: str) -> str:
        """Upscales low-res 50x50 or 150x150 thumbnails to 500x500 high-res artwork."""
        if not image_url:
            return "album_art.png"
        clean = image_url.replace("http://", "https://")
        return re.sub(r'-(?:50x50|150x150)\.jpg', '-500x500.jpg', clean)

    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Searches JioSaavn for tracks matching query."""
        if not query:
            return []
        params = {
            "__call": "search.getResults",
            "_format": "json",
            "p": "1",
            "n": str(min(limit, 50)),
            "_marker": "0",
            "ctx": "web6dot0",
            "q": query
        }
        tracks: List[Dict[str, Any]] = []
        try:
            resp = self.session.get(JIOSAAVN_API_BASE, params=params, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                for item in results:
                    track_id = item.get("id") or item.get("song_id")
                    if not track_id:
                        continue
                    
                    title = self._clean_text(item.get("song") or item.get("title"))
                    artists = self._clean_text(item.get("singers") or item.get("primary_artists") or item.get("music"))
                    duration = int(item.get("duration", 0) or 0)
                    artwork = self._upgrade_artwork(item.get("image", ""))
                    
                    enc_url = item.get("encrypted_media_url")
                    stream_url = self._decrypt_media_url(enc_url, quality="320") if enc_url else ""
                    
                    tracks.append({
                        "video_id": f"js_{track_id}",
                        "source_id": track_id,
                        "title": title,
                        "artist": artists or "JioSaavn Artist",
                        "duration": duration,
                        "artwork": artwork,
                        "url": stream_url or f"https://www.jiosaavn.com/song/{track_id}",
                        "source": "jiosaavn",
                        "bitrate": 320,
                        "stream_url": stream_url,
                        "album": self._clean_text(item.get("album", "")),
                        "year": item.get("year", ""),
                    })
        except Exception as e:
            logger.error("Search exception: %s", e)

        # Fallback to autocomplete if full search returned zero results
        if not tracks:
            tracks = self._autocomplete_search(query, limit=limit)

        return tracks

    def _autocomplete_search(self, query: str, limit: int = 15) -> List[Dict[str, Any]]:
        """Fallback search using autocomplete endpoint."""
        params = {
            "__call": "autocomplete.get",
            "_format": "json",
            "_marker": "0",
            "ctx": "web6dot0",
            "query": query
        }
        tracks = []
        try:
            resp = self.session.get(JIOSAAVN_API_BASE, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                song_list = data.get("songs", {}).get("data", [])
                for item in song_list[:limit]:
                    track_id = item.get("id")
                    if not track_id:
                        continue
                    title = self._clean_text(item.get("title"))
                    artist = self._clean_text(item.get("description") or item.get("singers"))
                    artwork = self._upgrade_artwork(item.get("image", ""))
                    tracks.append({
                        "video_id": f"js_{track_id}",
                        "source_id": track_id,
                        "title": title,
                        "artist": artist or "JioSaavn Artist",
                        "duration": 180,
                        "artwork": artwork,
                        "url": f"https://www.jiosaavn.com/song/{track_id}",
                        "source": "jiosaavn",
                        "bitrate": 320,
                        "stream_url": "",
                        "album": self._clean_text(item.get("album", "")),
                        "year": "",
                    })
        except Exception as e:
            logger.warning("Autocomplete search failed: %s", e)
        return tracks

    def get_track_details(self, track_id: str) -> Optional[Dict[str, Any]]:
        """Fetches detailed track metadata including decrypted 320kbps CDN stream."""
        clean_id = track_id.replace("js_", "")
        params = {
            "__call": "song.getDetails",
            "cc": "in",
            "_marker": "0?_marker=0",
            "_format": "json",
            "pids": clean_id
        }
        try:
            resp = self.session.get(JIOSAAVN_API_BASE, params=params, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                item = data.get(clean_id) or (list(data.values())[0] if data and isinstance(data, dict) else None)
                if not item or not isinstance(item, dict):
                    return None
                
                title = self._clean_text(item.get("song") or item.get("title"))
                artist = self._clean_text(item.get("singers") or item.get("primary_artists"))
                duration = int(item.get("duration", 0) or 0)
                artwork = self._upgrade_artwork(item.get("image", ""))
                
                enc_url = item.get("encrypted_media_url")
                stream_320 = self._decrypt_media_url(enc_url, quality="320")
                
                return {
                    "video_id": f"js_{clean_id}",
                    "source_id": clean_id,
                    "title": title,
                    "artist": artist or "JioSaavn Artist",
                    "duration": duration,
                    "artwork": artwork,
                    "url": stream_320 or item.get("perma_url", ""),
                    "source": "jiosaavn",
                    "bitrate": 320,
                    "stream_url": stream_320,
                    "lyrics": self._clean_text(item.get("lyrics_snippet", "")),
                    "album": self._clean_text(item.get("album", "")),
                    "year": item.get("year", ""),
                }
        except Exception as e:
            logger.error("get_track_details failed for %s: %s", track_id, e)
        return None

    def get_stream_url(self, track_id_or_url: str, quality: str = "320") -> Optional[Dict[str, Any]]:
        """Resolves direct HTTP CDN stream link for audio playback."""
        # Check if already a direct CDN url
        if track_id_or_url.startswith("http") and "saavncdn.com" in track_id_or_url:
            return {
                "url": track_id_or_url,
                "bitrate": int(quality) if quality.isdigit() else 320,
                "format": "mp4",
                "source": "jiosaavn"
            }
        details = self.get_track_details(track_id_or_url)
        if details and details.get("stream_url"):
            return {
                "url": details["stream_url"],
                "bitrate": 320,
                "format": "mp4",
                "source": "jiosaavn"
            }
        return None

    def get_playlist(self, playlist_id_or_url: str) -> Optional[Dict[str, Any]]:
        """Extracts playlist details and all song tracks from JioSaavn."""
        list_id = playlist_id_or_url
        if "jiosaavn.com/featured/" in playlist_id_or_url or "jiosaavn.com/shows/" in playlist_id_or_url:
            m = re.search(r'/([^/]+)/([a-zA-Z0-9_-]+)$', playlist_id_or_url)
            if m:
                list_id = m.group(2)

        params = {
            "__call": "playlist.getDetails",
            "_format": "json",
            "cc": "in",
            "_marker": "0?_marker=0",
            "listid": list_id
        }
        try:
            resp = self.session.get(JIOSAAVN_API_BASE, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                title = self._clean_text(data.get("listname") or data.get("title"))
                artwork = self._upgrade_artwork(data.get("image", ""))
                raw_songs = data.get("songs", [])
                
                parsed_tracks = []
                for s in raw_songs:
                    sid = s.get("id")
                    if not sid:
                        continue
                    enc = s.get("encrypted_media_url")
                    stream = self._decrypt_media_url(enc, quality="320") if enc else ""
                    parsed_tracks.append({
                        "video_id": f"js_{sid}",
                        "source_id": sid,
                        "title": self._clean_text(s.get("song")),
                        "artist": self._clean_text(s.get("singers") or s.get("primary_artists")),
                        "duration": int(s.get("duration", 0) or 0),
                        "artwork": self._upgrade_artwork(s.get("image", "")),
                        "url": stream or f"https://www.jiosaavn.com/song/{sid}",
                        "source": "jiosaavn",
                        "bitrate": 320,
                        "stream_url": stream,
                    })
                return {
                    "id": f"js_pl_{list_id}",
                    "title": title or "JioSaavn Playlist",
                    "artwork": artwork,
                    "tracks": parsed_tracks,
                    "source": "jiosaavn"
                }
        except Exception as e:
            logger.error("get_playlist failed: %s", e)
        return None
