"""
Spotify Music & Metadata Provider.
Zero-auth public playlist & track extraction using Spotify embed & oEmbed endpoints.
Enables 1-click import of public Spotify playlists and metadata resolution.
Stream resolution is matched to direct 320kbps JioSaavn audio or YouTube streams.
"""
import re
import html
import json
import requests
from typing import List, Dict, Optional, Any
from services.music_provider_base import BaseMusicProvider
from services.logger import get_logger

logger = get_logger("SpotifyProvider")

SPOTIFY_OEMBED_URL = "https://open.spotify.com/oembed"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

class SpotifyProvider(BaseMusicProvider):
    """Concrete provider for Spotify public playlists, albums, and track metadata."""

    def __init__(self):
        super().__init__(name="spotify")
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    @staticmethod
    def extract_spotify_id(url_or_id: str, expected_type: str = "playlist") -> str:
        """Extracts the 22-character Spotify base62 ID from URL or URI."""
        if not url_or_id:
            return ""
        # URI format: spotify:playlist:37i9dQZF1DXcBWIGoYBM5M
        if f"spotify:{expected_type}:" in url_or_id:
            return url_or_id.split(f"spotify:{expected_type}:")[-1].split("?")[0].strip()
        # Web URL format: https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=...
        m = re.search(r'/(?:playlist|track|album)/([a-zA-Z0-9]{22})', url_or_id)
        if m:
            return m.group(1)
        # Direct alphanumeric ID check
        clean = url_or_id.strip()
        if len(clean) == 22 and clean.isalnum():
            return clean
        return clean

    def _extract_next_data(self, html_text: str) -> Optional[dict]:
        """Parses __NEXT_DATA__ embedded JSON blob from Spotify embed HTML."""
        try:
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html_text, re.DOTALL)
            if m:
                return json.loads(m.group(1))
        except Exception as e:
            logger.warning("JSON parse error: %s", e)
        return None

    def get_playlist(self, playlist_id_or_url: str) -> Optional[Dict[str, Any]]:
        """Extracts playlist or album details and tracklist without authentication."""
        is_album = "/album/" in playlist_id_or_url or "spotify:album:" in playlist_id_or_url
        kind = "album" if is_album else "playlist"
        sp_id = self.extract_spotify_id(playlist_id_or_url, expected_type=kind)
        if not sp_id:
            return None

        embed_url = f"https://open.spotify.com/embed/{kind}/{sp_id}"
        try:
            resp = self.session.get(embed_url, timeout=10)
            if resp.status_code != 200:
                logger.warning("Embed returned status %s for %s", resp.status_code, embed_url)
                return None

            data = self._extract_next_data(resp.text)
            if not data:
                return None

            props = data.get("props", {}).get("pageProps", {})
            state = props.get("state", {}).get("data", {})
            entity = state.get("entity", {})
            if not entity:
                return None

            title = html.unescape(entity.get("title") or entity.get("name") or "Spotify Playlist")
            raw_art = entity.get("coverArt", {}).get("sources", [])
            artwork = raw_art[-1].get("url") if raw_art else "album_art.png"

            track_list = entity.get("trackList", [])
            parsed_tracks: List[Dict[str, Any]] = []

            for idx, tr in enumerate(track_list):
                t_title = html.unescape(tr.get("title") or "Unknown")
                t_artist = html.unescape(tr.get("subtitle") or "")
                dur_ms = int(tr.get("duration", 0) or 0)
                dur_sec = max(30, dur_ms // 1000) if dur_ms > 0 else 180
                uri = tr.get("uri") or f"spotify:track:{idx}"
                t_id = uri.split(":")[-1]

                parsed_tracks.append({
                    "video_id": f"sp_{t_id}",
                    "source_id": t_id,
                    "title": t_title,
                    "artist": t_artist,
                    "duration": dur_sec,
                    "artwork": artwork,
                    "url": f"https://open.spotify.com/track/{t_id}",
                    "source": "spotify",
                    "bitrate": 320,
                    "stream_url": "",
                    "isrc": tr.get("isrc", ""),
                })

            return {
                "id": f"sp_{kind}_{sp_id}",
                "source_id": sp_id,
                "title": title,
                "artwork": artwork,
                "tracks": parsed_tracks,
                "source": "spotify",
                "kind": kind
            }
        except Exception as e:
            logger.error("get_playlist failed for %s: %s", playlist_id_or_url, e)
        return None

    def get_track_details(self, track_id: str) -> Optional[Dict[str, Any]]:
        """Extracts individual track details via Spotify oEmbed and embed fallback."""
        clean_id = self.extract_spotify_id(track_id, expected_type="track")
        if not clean_id:
            return None

        oembed_url = f"{SPOTIFY_OEMBED_URL}?url=https://open.spotify.com/track/{clean_id}"
        try:
            resp = self.session.get(oembed_url, timeout=6)
            if resp.status_code == 200:
                d = resp.json()
                title = d.get("title", "Spotify Track")
                artwork = d.get("thumbnail_url", "album_art.png")
                # Parse title which often has format "Track Title - Artist" or "Track Title"
                artist = "Spotify Artist"
                if " - " in title:
                    parts = title.split(" - ", 1)
                    title, artist = parts[0], parts[1]

                return {
                    "video_id": f"sp_{clean_id}",
                    "source_id": clean_id,
                    "title": title,
                    "artist": artist,
                    "duration": 180,
                    "artwork": artwork,
                    "url": f"https://open.spotify.com/track/{clean_id}",
                    "source": "spotify",
                    "bitrate": 320,
                    "stream_url": "",
                }
        except Exception as e:
            logger.warning("get_track_details oEmbed error: %s", e)

        # Fallback to embed page
        embed_url = f"https://open.spotify.com/embed/track/{clean_id}"
        try:
            resp = self.session.get(embed_url, timeout=8)
            if resp.status_code == 200:
                data = self._extract_next_data(resp.text)
                if data:
                    props = data.get("props", {}).get("pageProps", {})
                    state = props.get("state", {}).get("data", {})
                    entity = state.get("entity", {})
                    title = html.unescape(entity.get("title") or entity.get("name") or "Spotify Track")
                    artist = html.unescape(entity.get("subtitle") or "Spotify Artist")
                    dur_ms = int(entity.get("duration", 0) or 0)
                    raw_art = entity.get("coverArt", {}).get("sources", [])
                    artwork = raw_art[-1].get("url") if raw_art else "album_art.png"

                    return {
                        "video_id": f"sp_{clean_id}",
                        "source_id": clean_id,
                        "title": title,
                        "artist": artist,
                        "duration": max(30, dur_ms // 1000) if dur_ms else 180,
                        "artwork": artwork,
                        "url": f"https://open.spotify.com/track/{clean_id}",
                        "source": "spotify",
                        "bitrate": 320,
                        "stream_url": "",
                    }
        except Exception as e:
            logger.warning("get_track_details embed error: %s", e)

        return None

    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Public Spotify search simulation using public playlist and track index queries.
        For direct user search queries, the MusicProviderRouter combines JioSaavn & YouTube.
        """
        # If user pasted a Spotify URL into search bar, resolve it directly!
        if "open.spotify.com/" in query or query.startswith("spotify:"):
            if "/playlist/" in query or "spotify:playlist:" in query or "/album/" in query or "spotify:album:" in query:
                pl = self.get_playlist(query)
                return pl.get("tracks", []) if pl else []
            if "/track/" in query or "spotify:track:" in query:
                td = self.get_track_details(query)
                return [td] if td else []
        return []

    def get_stream_url(self, track_id_or_url: str, quality: str = "320") -> Optional[Dict[str, Any]]:
        """Spotify audio streams are resolved via the MusicProviderRouter matcher."""
        return None
