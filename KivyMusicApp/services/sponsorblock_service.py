"""
SponsorBlock API Integration Service.
Queries the community-maintained SponsorBlock API to retrieve non-music, sponsor,
intro, and outro segment timestamps for YouTube music tracks.
Enables automatic segment skipping during playback when enabled in settings.
Completely non-blocking, cached, and cross-platform compatible (Windows and Android).
"""

import json
import ssl
import threading
import urllib.parse
import urllib.request
from typing import Dict, List, Optional, Tuple

class SponsorBlockService:
    """Manages SponsorBlock segment retrieval, memory caching, and skip evaluation."""

    API_URL = "https://sponsor.ajay.app/api/skipSegments"
    CATEGORIES = ["music_offtopic", "sponsor", "intro", "outro", "selfpromo"]

    def __init__(self):
        self._cache: Dict[str, List[Tuple[float, float, str]]] = {}
        self._fetching: set = set()
        self._lock = threading.Lock()

    def fetch_segments_async(self, video_id: str, on_loaded=None):
        """Asynchronously fetches skip segments for a given YouTube video ID."""
        if not video_id or len(video_id) < 5:
            return

        with self._lock:
            if video_id in self._cache or video_id in self._fetching:
                if video_id in self._cache and on_loaded:
                    on_loaded(self._cache[video_id])
                return
            self._fetching.add(video_id)

        def _worker():
            segments = []
            try:
                params = [("videoID", video_id)]
                for cat in self.CATEGORIES:
                    params.append(("category", cat))
                query_str = urllib.parse.urlencode(params)
                full_url = f"{self.API_URL}?{query_str}"

                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE

                req = urllib.request.Request(
                    full_url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) KivyMusicApp/2.0"
                    }
                )
                with urllib.request.urlopen(req, timeout=4, context=ctx) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode("utf-8"))
                        for item in data:
                            seg = item.get("segment", [])
                            cat = item.get("category", "sponsor")
                            if len(seg) == 2:
                                start, end = float(seg[0]), float(seg[1])
                                if end > start:
                                    segments.append((start, end, cat))
            except Exception:
                # 404 or network timeout simply means no skip segments exist for this track
                pass
            finally:
                with self._lock:
                    self._cache[video_id] = segments
                    self._fetching.discard(video_id)
                if on_loaded:
                    on_loaded(segments)

        threading.Thread(target=_worker, daemon=True).start()

    def get_skip_target(self, video_id: str, current_pos: float) -> Optional[float]:
        """
        Checks if current playback position falls within any skip segment.
        Returns the end position of the segment to seek to, or None if no skip needed.
        """
        if not video_id:
            return None
        with self._lock:
            segments = self._cache.get(video_id, [])

        for start, end, cat in segments:
            # If current position is inside segment (with a small 0.2s tolerance)
            if start <= current_pos < (end - 0.5):
                return end
        return None

    def clear_cache(self):
        """Clears cached segment data."""
        with self._lock:
            self._cache.clear()
            self._fetching.clear()
