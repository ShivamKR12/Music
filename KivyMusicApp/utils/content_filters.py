"""Content-quality filters for recommendations, shelves, search and queues.

AI-generated tracks and tutorial/how-to videos are noise in a music player.
They are filtered by default; the AI filter can be disabled in Settings for
users who explicitly want to see AI-generated music.
"""

from __future__ import annotations

import re
from typing import Any, Iterable, List

_AI_RE = re.compile(
    r"(?i)\b(ai|suno|udio|ai[- ]?song|ai[- ]?music|ai[- ]?cover|"
    r"ai[- ]?generated|generated[- ]?by[- ]?ai|synthetic[- ]?voice)\b"
)

_NON_MUSIC_RE = re.compile(
    r"(?i)\b(tutorial|how[- ]?to|howto|step[- ]?by[- ]?step|"
    r"vlog|unboxing|lecture)\b"
)


def _field(track: Any, key: str) -> str:
    if isinstance(track, dict):
        return str(track.get(key) or "")
    return str(getattr(track, key, "") or "")


def is_ai_generated(track: Any) -> bool:
    """True when title/artist/channel/description advertises AI-generated audio."""
    haystack = " ".join(
        _field(track, key)
        for key in ("title", "artist", "channel", "description", "album")
    )
    return bool(_AI_RE.search(haystack))


def is_non_music_video(track: Any) -> bool:
    """True for tutorial/how-to videos mislabeled as songs."""
    media_type = _field(track, "media_type").lower()
    if media_type == "podcast":
        return False
    haystack = " ".join(
        _field(track, key) for key in ("title", "artist", "channel", "description")
    )
    return bool(_NON_MUSIC_RE.search(haystack))


def filter_tracks(
    tracks: Iterable[Any],
    include_ai: bool = False,
    filter_non_music: bool = True,
) -> List[Any]:
    """Return tracks with tutorials removed and AI songs gated by ``include_ai``."""
    result = []
    for track in tracks or []:
        if filter_non_music and is_non_music_video(track):
            continue
        if not include_ai and is_ai_generated(track):
            continue
        result.append(track)
    return result
