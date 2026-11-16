"""
Music Provider Router & Stream Arbitration Engine.
Unifies YouTube, Spotify, and JioSaavn into a seamless multi-source pipeline.
Handles query routing, parallel multi-source search, intelligent stream matching,
and 1-click Spotify playlist import into local SQLite storage.
"""
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Any, Union

from services.music_provider_base import BaseMusicProvider
from services.youtube_provider import YouTubeProvider
from services.jiosaavn_provider import JioSaavnProvider
from services.spotify_provider import SpotifyProvider
from models.database import (
    DB_LOCK, get_db_connection, add_track, add_playlist,
    add_track_to_playlist, get_all_playlists
)

class MusicProviderRouter:
    """Central router and arbitrator for all music providers."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.youtube = YouTubeProvider()
        self.jiosaavn = JioSaavnProvider()
        self.spotify = SpotifyProvider()
        self._executor = ThreadPoolExecutor(max_workers=4)
        self._initialized = True

    def search(self, query: str, provider: str = "all", limit: int = 20) -> List[Dict[str, Any]]:
        """
        Executes unified search across requested providers.
        provider: 'all' | 'jiosaavn' | 'youtube' | 'spotify'
        """
        clean_q = query.strip()
        if not clean_q:
            return []

        # 1. URL-based direct routing
        if "open.spotify.com/" in clean_q or clean_q.startswith("spotify:"):
            return self.spotify.search(clean_q, limit=limit)
        if "youtube.com/" in clean_q or "youtu.be/" in clean_q:
            return self.youtube.search(clean_q, limit=limit)

        # 2. Single provider routing
        if provider == "jiosaavn":
            return self.jiosaavn.search(clean_q, limit=limit)
        if provider == "youtube":
            return self.youtube.search(clean_q, limit=limit)
        if provider == "spotify":
            return self.spotify.search(clean_q, limit=limit)

        # 3. Parallel multi-source fan-out ('all')
        futures = {
            self._executor.submit(self.jiosaavn.search, clean_q, max(5, limit // 2)): "jiosaavn",
            self._executor.submit(self.youtube.search, clean_q, max(5, limit // 2)): "youtube",
        }
        combined: List[Dict[str, Any]] = []
        js_results: List[Dict[str, Any]] = []
        yt_results: List[Dict[str, Any]] = []

        for future in as_completed(futures):
            src = futures[future]
            try:
                res = future.result()
                if src == "jiosaavn":
                    js_results = res
                else:
                    yt_results = res
            except Exception as e:
                print(f"[MusicProviderRouter] Search failed for {src}: {e}")

        # Interleave JioSaavn (320kbps HD) and YouTube results smoothly
        max_len = max(len(js_results), len(yt_results))
        for i in range(max_len):
            if i < len(js_results):
                combined.append(js_results[i])
            if i < len(yt_results):
                combined.append(yt_results[i])

        return combined[:limit]

    def resolve_stream(self, track: Union[dict, Any]) -> Dict[str, Any]:
        """
        Resolves the highest fidelity audio stream for any given track.
        Directs JioSaavn tracks to direct 320kbps CDN, matches Spotify tracks to JioSaavn/YouTube.
        """
        track_dict = track.to_dict() if hasattr(track, "to_dict") else dict(track)
        source = track_dict.get("source", "youtube")
        vid = track_dict.get("video_id", "")
        source_id = track_dict.get("source_id", "") or vid
        title = track_dict.get("title", "")
        artist = track_dict.get("artist", "")
        stream_url = track_dict.get("stream_url", "")

        # 1. JioSaavn: Direct 320kbps CD-Quality Stream
        if source == "jiosaavn" or vid.startswith("js_"):
            if stream_url and "saavncdn.com" in stream_url:
                return {
                    "url": stream_url,
                    "source": "jiosaavn",
                    "bitrate": 320,
                    "is_direct_http": True,
                    "format": "mp4"
                }
            clean_id = source_id.replace("js_", "")
            details = self.jiosaavn.get_track_details(clean_id)
            if details and details.get("stream_url"):
                return {
                    "url": details["stream_url"],
                    "source": "jiosaavn",
                    "bitrate": 320,
                    "is_direct_http": True,
                    "format": "mp4"
                }

        # 2. Spotify: High-Fidelity Audio Matching Engine
        if source == "spotify" or vid.startswith("sp_"):
            # Attempt A: Match against JioSaavn for 320kbps HD audio
            search_query = f"{title} {artist}".strip()
            if search_query:
                js_matches = self.jiosaavn.search(search_query, limit=2)
                if js_matches:
                    best = js_matches[0]
                    # Simple title resemblance verification
                    clean_match_title = re.sub(r'[^a-zA-Z0-9]', '', best.get('title', '')).lower()
                    clean_orig_title = re.sub(r'[^a-zA-Z0-9]', '', title).lower()
                    if clean_orig_title in clean_match_title or clean_match_title in clean_orig_title:
                        if best.get("stream_url"):
                            return {
                                "url": best["stream_url"],
                                "source": "jiosaavn_matched",
                                "bitrate": 320,
                                "is_direct_http": True,
                                "format": "mp4"
                            }

            # Attempt B: Match against YouTube via yt-dlp
            yt_matches = self.youtube.search(f"{title} {artist}", limit=1)
            if yt_matches:
                yt_vid = yt_matches[0].get("video_id")
                return {
                    "url": f"https://www.youtube.com/watch?v={yt_vid}",
                    "source": "youtube_matched",
                    "bitrate": 128,
                    "is_direct_http": False,
                    "matched_video_id": yt_vid
                }

        # 3. Standard YouTube Fallback
        clean_yt_id = vid.replace("yt_", "")
        return {
            "url": f"https://www.youtube.com/watch?v={clean_yt_id}",
            "source": "youtube",
            "bitrate": 128,
            "is_direct_http": False,
            "video_id": clean_yt_id
        }

    def import_spotify_playlist(self, playlist_url_or_id: str) -> Dict[str, Any]:
        """
        Extracts public Spotify playlist/album and imports all tracks into local SQLite database.
        Returns result summary: {"success": bool, "title": str, "count": int, "artwork": str}
        """
        pl_data = self.spotify.get_playlist(playlist_url_or_id)
        if not pl_data or not pl_data.get("tracks"):
            return {"success": False, "error": "Could not extract Spotify playlist or playlist is empty."}

        title = pl_data.get("title", "Imported Spotify Playlist")
        artwork = pl_data.get("artwork", "album_art.png")
        tracks = pl_data.get("tracks", [])

        # 1. Create or ensure unique playlist in SQLite
        clean_pl_name = f"[Spotify] {title}"
        add_playlist(clean_pl_name)

        # 2. Persist tracks and bind to playlist
        imported_count = 0
        for tr in tracks:
            vid = tr.get("video_id")
            if not vid:
                continue
            add_track(
                video_id=vid,
                title=tr.get("title", "Unknown"),
                artist=tr.get("artist", "Unknown"),
                url=tr.get("url", ""),
                duration=tr.get("duration", 180),
                artwork=tr.get("artwork", artwork),
                local_path=""
            )
            add_track_to_playlist(clean_pl_name, vid, track_meta=tr)
            imported_count += 1

        return {
            "success": True,
            "title": clean_pl_name,
            "count": imported_count,
            "artwork": artwork,
            "tracks": tracks
        }
