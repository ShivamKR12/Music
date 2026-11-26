"""
Explicit Data Contracts & Tested Mathematical Ranking Functions for Recommendations
(Priority 4 Subsystem).

Feature Provenance (Designed & Implemented):
- TrackFeatures:
  * Metadata (`video_id`, `title`, `artist`, `genre`, `duration_seconds`): from SQLite `tracks`,
    YouTube/JioSaavn/Spotify metadata, or local ID3 tags (`mutagen`).
  * `popularity`: normalized chart/view signal in [0, 1] when chart rank or real view counts exist.
  * `trending_velocity`: normalized [0, 1] velocity computed strictly from >= 2 timestamped
    observations stored in `trend_observations` (never guessed from a single view count).
  * `play_count`, `skip_count`, `total_listen_seconds`, `seconds_since_last_play`: from SQLite
    `tracks` + `listening_events`.
  * Acoustic descriptors (`energy`, `valence`, `bpm`): explicitly Optional[float] = None and NEVER
    fabricated when unavailable; context matching uses verified metadata/query tags honestly.
- ListenerFeatures:
  * Derived strictly from real SQLite listening history (`tracks`, `listening_events`, Favorites).
"""

from __future__ import annotations

import datetime
import math
import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


DEFAULT_NOVELTY_TAU_SEC = 86400.0   # 24 hours
DEFAULT_RECENT_TAU_SEC = 14400.0    # 4 hours


@dataclass
class TrackFeatures:
    """Typed track feature contract for recommendation ranking."""
    video_id: str
    title: str
    artist: str
    source: str = "youtube"
    genre: str = ""
    duration_seconds: float = 0.0
    popularity: float = 0.0
    trending_velocity: float = 0.0
    play_count: int = 0
    skip_count: int = 0
    total_listen_seconds: float = 0.0
    seconds_since_last_play: Optional[float] = None
    is_favorite: bool = False
    is_local: bool = False
    tags_text: str = ""
    # Explicitly None until an audio feature extractor supplies real acoustic values
    energy: Optional[float] = None
    valence: Optional[float] = None
    bpm: Optional[float] = None


@dataclass
class ListenerFeatures:
    """Typed listener preference contract derived strictly from persisted listening events."""
    artist_affinities: Dict[str, float] = field(default_factory=dict)
    genre_affinities: Dict[str, float] = field(default_factory=dict)
    total_plays: int = 0
    total_skips: int = 0
    total_listening_seconds: float = 0.0
    context_keywords: Tuple[str, ...] = ()


@dataclass
class RecommendationScoreBreakdown:
    """Interpretable component scores and total score for a single ranked track."""
    total_score: float
    artist_affinity: float
    genre_affinity: float
    trending_velocity: float
    novelty: float
    engagement_quality: float
    context_match: float
    skip_penalty: float


# =============================================================================
# Core Pure Mathematical Functions (Unit-Testable with Boundary Laws)
# =============================================================================
def compute_recency_novelty(
    seconds_since_last_play: Optional[float],
    tau_seconds: float = DEFAULT_NOVELTY_TAU_SEC,
) -> float:
    """
    Monotonic novelty saturation curve H(dt) in [0.0, 1.0]:
        H(dt) = 1 - exp(-dt / tau)
    - Unplayed tracks (seconds_since_last_play is None) -> 1.0 (maximum discovery novelty).
    - At dt = 0 (just played right now) -> 0.0 (suppresses immediate repeat echo).
    - Strictly increases with dt >= 0 and asymptotically approaches 1.0.
    """
    if seconds_since_last_play is None:
        return 1.0
    tau = max(1.0, float(tau_seconds))
    dt = max(0.0, float(seconds_since_last_play))
    return max(0.0, min(1.0, 1.0 - math.exp(-dt / tau)))


def compute_recent_recall(
    seconds_since_last_play: Optional[float],
    tau_seconds: float = DEFAULT_RECENT_TAU_SEC,
) -> float:
    """
    Exponential recency decay F(dt) in [0.0, 1.0] for explicit 'Jump back in / Recently played'
    recall shelves (inverse of novelty):
        F(dt) = exp(-dt / tau)
    """
    if seconds_since_last_play is None:
        return 0.0
    tau = max(1.0, float(tau_seconds))
    dt = max(0.0, float(seconds_since_last_play))
    return max(0.0, min(1.0, math.exp(-dt / tau)))


def compute_skip_penalty(
    play_count: int,
    skip_count: int,
) -> float:
    """
    Bayesian-smoothed skip ratio in [0.0, 1.0].
    Strictly increases as `skip_count` grows relative to total interactions.
    """
    plays = max(0, int(play_count or 0))
    skips = max(0, int(skip_count or 0))
    if skips == 0:
        return 0.0
    denom = float(plays + skips + 2.0)  # Laplace-smoothed prior avoids harsh 1/1 penalty on single accidental skip
    return max(0.0, min(1.0, skips / denom))


def compute_engagement_quality(
    play_count: int,
    skip_count: int,
    total_listen_seconds: float,
    duration_seconds: float,
    is_favorite: bool = False,
) -> float:
    """
    Combines completion affinity, favorite preference, and skip suppression in [0.0, 1.0].
    """
    plays = max(0, int(play_count or 0))
    skip_pen = compute_skip_penalty(plays, skip_count)
    dur = max(0.0, float(duration_seconds or 0.0))
    listen = max(0.0, float(total_listen_seconds or 0.0))

    if plays > 0 and dur > 10.0 and listen > 0.0:
        avg_ratio = min(1.0, (listen / float(plays)) / dur)
    elif plays > 0:
        avg_ratio = min(1.0, 0.35 + 0.15 * min(4, plays))
    else:
        avg_ratio = 0.25  # Neutral baseline prior for unplayed discovery candidates

    fav_bonus = 0.25 if is_favorite else 0.0
    raw = avg_ratio * (1.0 - 0.75 * skip_pen) + fav_bonus - 0.30 * skip_pen
    return max(0.0, min(1.0, raw))


def compute_trending_velocity(
    observations: Sequence[Tuple[float, float]],
    min_dt_seconds: float = 60.0,
) -> float:
    """
    Compute normalized multi-timestamp trending velocity in [0.0, 1.0].
    Accepts observations as (epoch_timestamp_sec, metric_value) pairs where metric_value is
    monotonic popularity (e.g. view_count or inverted chart rank score).
    STRICT INVARIANT:
    - Fewer than 2 observations, or observation span < min_dt_seconds, ALWAYS returns 0.0
      so static single-snapshot view counts never pose as trending velocity.
    - Negative/falling or flat trends clamp cleanly to 0.0.
    """
    if not observations or len(observations) < 2:
        return 0.0

    ordered = sorted((float(ts), float(val)) for ts, val in observations if ts is not None and val is not None)
    t0, v0 = ordered[0]
    t1, v1 = ordered[-1]
    dt_sec = t1 - t0
    if dt_sec < min_dt_seconds:
        return 0.0

    delta_v = v1 - v0
    if delta_v <= 0.0:
        return 0.0

    # Relative growth per hour normalized with smooth saturation (tanh)
    dt_hours = dt_sec / 3600.0
    baseline = max(1.0, abs(v0))
    rel_growth_per_hour = (delta_v / baseline) / max(0.016, dt_hours)
    return max(0.0, min(1.0, math.tanh(rel_growth_per_hour)))


def parse_timestamp_age_seconds(
    ts_value: Optional[str],
    now_utc: Optional[datetime.datetime] = None,
) -> Optional[float]:
    """Parse SQLite CURRENT_TIMESTAMP ('YYYY-MM-DD HH:MM:SS' UTC) or ISO string into age in seconds."""
    if not ts_value or not isinstance(ts_value, str):
        return None
    s = ts_value.strip()
    if not s:
        return None
    try:
        dt = datetime.datetime.fromisoformat(s.replace("Z", ""))
        ref = now_utc or datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        if dt.tzinfo is not None:
            dt = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        return max(0.0, (ref - dt).total_seconds())
    except Exception:
        return None


def compute_context_match(
    track: TrackFeatures,
    context_keywords: Sequence[str],
) -> float:
    """Measure overlap between verified track metadata/title/genre tags and active context keywords."""
    if not context_keywords:
        return 0.0
    haystack = " ".join([
        track.title or "",
        track.artist or "",
        track.genre or "",
        track.tags_text or "",
    ]).lower()
    clean_kw = [str(k).strip().lower() for k in context_keywords if k and len(str(k).strip()) >= 3]
    if not clean_kw:
        return 0.0
    hits = sum(1 for kw in clean_kw if kw in haystack)
    return max(0.0, min(1.0, hits / max(1.0, min(4.0, float(len(clean_kw))))))


# =============================================================================
# Feature Builders, Scoring Modes, and Canonical Deduplication
# =============================================================================
def track_dict_to_features(
    raw: Dict[str, Any],
    velocity_map: Optional[Dict[str, float]] = None,
    events_stats_map: Optional[Dict[str, Dict[str, Any]]] = None,
    now_utc: Optional[datetime.datetime] = None,
) -> TrackFeatures:
    """Build explicit TrackFeatures contract from heterogeneous track dict + SQLite telemetry."""
    vid = str(raw.get("video_id") or "")
    ev_stats = (events_stats_map or {}).get(vid, {})

    play_count = max(int(raw.get("play_count") or 0), int(ev_stats.get("play_count") or 0))
    skip_count = int(ev_stats.get("skip_count") or raw.get("skip_count") or 0)
    listen_sec = float(ev_stats.get("total_listen_seconds") or raw.get("total_listen_seconds") or 0.0)

    age_sec = parse_timestamp_age_seconds(raw.get("last_played") or ev_stats.get("last_played"), now_utc=now_utc)

    views = float(raw.get("view_count") or 0.0)
    chart_rank = float(raw.get("chart_rank") or 0.0)
    if chart_rank > 0:
        popularity = max(0.0, min(1.0, 1.0 - ((chart_rank - 1.0) / 50.0)))
    elif views > 0:
        popularity = max(0.0, min(1.0, math.log10(max(1.0, views)) / 9.0))
    else:
        popularity = 0.0

    # Multi-timestamp trending velocity ONLY (strictly 0.0 without >=2 timestamps)
    velocity = float((velocity_map or {}).get(vid, raw.get("trending_velocity") or 0.0))

    return TrackFeatures(
        video_id=vid,
        title=str(raw.get("title") or "Unknown Title"),
        artist=str(raw.get("artist") or "Unknown Artist"),
        source=str(raw.get("source") or "youtube"),
        genre=str(raw.get("genre") or ""),
        duration_seconds=float(raw.get("duration") or 0.0),
        popularity=popularity,
        trending_velocity=max(0.0, min(1.0, velocity)),
        play_count=play_count,
        skip_count=skip_count,
        total_listen_seconds=listen_sec,
        seconds_since_last_play=age_sec,
        is_favorite=bool(raw.get("is_favorite")),
        is_local=bool(raw.get("local_path")),
        tags_text=" ".join(filter(None, [str(raw.get("album") or ""), str(raw.get("description") or "")[:180]])),
    )


def score_track(
    track: TrackFeatures,
    listener: ListenerFeatures,
    mode: str = "discovery",
) -> RecommendationScoreBreakdown:
    """
    Score a track under explicit shelf weighting modes:
    - 'discovery': prioritizes novelty (1 - exp(-dt/tau)), artist/genre affinity, and context match.
    - 'trending':  prioritizes multi-timestamp trending_velocity & popularity with novelty & anti-skip.
    - 'recall':    prioritizes recent recall & high engagement quality for Jump Back In / Heavy Rotation.
    - 'regional':  prioritizes local library / regional affinity + freshness.
    """
    art_key = (track.artist or "").strip().lower()
    artist_aff = 0.0
    if art_key and listener.artist_affinities:
        if art_key in listener.artist_affinities:
            artist_aff = listener.artist_affinities[art_key]
        else:
            # Handle multi-artist strings (e.g. "Artist A, Artist B")
            for k, val in listener.artist_affinities.items():
                if k and len(k) >= 3 and k in art_key:
                    artist_aff = max(artist_aff, val * 0.85)

    g_key = (track.genre or "").strip().lower()
    genre_aff = float(listener.genre_affinities.get(g_key, 0.0)) if g_key else 0.0

    novelty = compute_recency_novelty(track.seconds_since_last_play)
    recall = compute_recent_recall(track.seconds_since_last_play)
    skip_pen = compute_skip_penalty(track.play_count, track.skip_count)
    engagement = compute_engagement_quality(
        track.play_count,
        track.skip_count,
        track.total_listen_seconds,
        track.duration_seconds,
        is_favorite=track.is_favorite,
    )
    ctx_match = compute_context_match(track, listener.context_keywords)

    # Blend multi-timestamp velocity strictly ahead of static popularity
    trend_signal = 0.70 * track.trending_velocity + 0.30 * track.popularity

    if mode == "trending":
        total = (
            0.40 * trend_signal
            + 0.25 * novelty
            + 0.20 * artist_aff
            + 0.15 * ctx_match
            - 0.35 * skip_pen
        )
    elif mode == "recall":
        total = (
            0.35 * engagement
            + 0.30 * recall
            + 0.25 * artist_aff
            + 0.10 * genre_aff
            - 0.40 * skip_pen
        )
    elif mode == "regional":
        local_bonus = 0.25 if track.is_local else 0.0
        total = (
            local_bonus
            + 0.25 * novelty
            + 0.25 * artist_aff
            + 0.15 * trend_signal
            + 0.10 * ctx_match
            - 0.35 * skip_pen
        )
    else:  # 'discovery' / quick_picks / daily_mix
        total = (
            0.30 * novelty
            + 0.25 * artist_aff
            + 0.15 * engagement
            + 0.15 * ctx_match
            + 0.15 * (0.6 * trend_signal + 0.4 * genre_aff)
            - 0.40 * skip_pen
        )

    return RecommendationScoreBreakdown(
        total_score=round(total, 6),
        artist_affinity=round(artist_aff, 4),
        genre_affinity=round(genre_aff, 4),
        trending_velocity=round(track.trending_velocity, 4),
        novelty=round(novelty, 4),
        engagement_quality=round(engagement, 4),
        context_match=round(ctx_match, 4),
        skip_penalty=round(skip_pen, 4),
    )


def canonical_track_key(track_dict: Dict[str, Any]) -> str:
    """
    Canonical deduplication key uniting identical songs across Spotify, JioSaavn,
    YouTube, and local filesystem copies.
    """
    title = re.sub(r"\([^)]*\)|\[[^\]]*\]", "", str(track_dict.get("title") or "")).lower()
    title_norm = re.sub(r"[^a-z0-9]", "", title)
    artist = re.sub(r"[^a-z0-9]", "", str(track_dict.get("artist") or "").lower().split(",")[0])
    if title_norm and artist:
        return f"ta:{title_norm}:{artist}"
    vid = str(track_dict.get("video_id") or "").strip()
    if vid:
        return f"id:{vid}"
    return f"t:{title_norm}"


def rank_and_deduplicate_tracks(
    candidates: Iterable[Dict[str, Any]],
    listener: ListenerFeatures,
    mode: str = "discovery",
    limit: int = 15,
    velocity_map: Optional[Dict[str, float]] = None,
    events_stats_map: Optional[Dict[str, Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """
    Score, deduplicate canonically, and rank candidate track dicts deterministically.
    Preserves all original keys on each returned track dict and attaches `_rec_score`.
    """
    seen_ids = set()
    seen_keys = set()
    scored_items: List[Tuple[float, int, Dict[str, Any]]] = []

    for idx, item in enumerate(candidates):
        if not item or not isinstance(item, dict):
            continue
        vid = str(item.get("video_id") or "").strip()
        if vid and vid in seen_ids:
            continue
        ckey = canonical_track_key(item)
        if ckey in seen_keys:
            continue
        if vid:
            seen_ids.add(vid)
        seen_keys.add(ckey)

        feats = track_dict_to_features(
            item,
            velocity_map=velocity_map,
            events_stats_map=events_stats_map,
        )
        breakdown = score_track(feats, listener, mode=mode)
        enriched = dict(item)
        enriched["_rec_score"] = breakdown.total_score
        scored_items.append((breakdown.total_score, idx, enriched))

    scored_items.sort(key=lambda pair: (-pair[0], pair[1]))
    return [pair[2] for pair in scored_items[:max(1, int(limit))]]
