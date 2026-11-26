"""
Dynamic Multi-Provider Recommendation & Discovery Engine.
Integrates YouTube, Spotify, and JioSaavn data alongside listener behavior,
listening choices, playback habits, time-of-day temporal rhythms, active mood,
and device location/local audio to generate personalized, non-fixed dynamic playlists
and smart song suggestions.
"""

import os
import re
import time
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Any, Union

from services.logger import get_logger
from services.music_provider_router import MusicProviderRouter
from services.jiosaavn_provider import JioSaavnProvider
from services.spotify_provider import SpotifyProvider
from utils.media_utils import fetch_youtube_metadata, parse_complete_media_metadata, is_podcast_item
from models.database import (
    DB_LOCK, get_connection, get_recently_played, get_continue_listening,
    get_on_repeat, get_heavy_rotation, get_forgotten_favorites, get_daily_mix,
    get_all_tracks, get_top_artists, get_top_genres, get_local_library_tracks,
    get_listening_event_stats, get_trending_velocity_map, record_trend_observations, add_track
)
from services.recommendation_scoring import (
    ListenerFeatures,
    TrackFeatures,
    canonical_track_key,
    rank_and_deduplicate_tracks,
)

logger = get_logger("RecommendationEngine")

# Canonical curated Spotify playlist IDs for multi-provider trending charts
SPOTIFY_CHART_PLAYLISTS = {
    "top_hits": "37i9dQZF1DXcBWIGoYBM5M",       # Today's Top Hits
    "viral_global": "37i9dQZF1DX1kCI7MYgnvx",   # Viral 50 Global
    "india_hits": "37i9dQZF1DX0XUfTFmZeCE",     # Hot Hits India
    "chill": "37i9dQZF1DX4WYpdgoIcn6",          # Chill Hits
    "workout": "37i9dQZF1DX76Wlfdnj7AP",        # Beast Mode / Workout
}

class DynamicRecommendationEngine:
    """
    Intelligent context-driven discovery and dynamic recommendation engine.
    Fuses user listening choices, behaviors, time-of-day, active mood, location,
    and multi-provider data (YouTube, Spotify, JioSaavn, and Local Storage).
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.router = MusicProviderRouter()
        self.spotify = SpotifyProvider()
        self.jiosaavn = JioSaavnProvider()
        self._executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="RecEngineWorker")
        
        # Memory caches: key -> (timestamp, data)
        self._cache: Dict[str, Any] = {}
        self._cache_ttl = 900  # 15 minutes TTL
        self._initialized = True

    # =========================================================================
    # 1. TEMPORAL & CONTEXTUAL ANALYSIS (Time of Day & Rhythms)
    # =========================================================================
    @staticmethod
    def get_time_context() -> Dict[str, Any]:
        """
        Calculates time-of-day listening context and appropriate musical themes.
        """
        now = datetime.datetime.now()
        hour = now.hour
        weekday = now.weekday()  # 0=Monday, 4=Friday, 5=Saturday, 6=Sunday
        is_weekend = (weekday in (4, 5, 6))

        if hour < 5:
            return {
                "period": "late_night",
                "kicker": "MIDNIGHT ATMOSPHERE",
                "title": "Late Night Lo-Fi & Ambient",
                "shelf_title": "Late Night Melodies",
                "query": "late night drive slow chill aesthetic songs lofi",
                "tempo": "slow",
            }
        elif 5 <= hour < 10:
            return {
                "period": "morning",
                "kicker": "FRESH START",
                "title": "Morning Acoustic & Coffee",
                "shelf_title": "Morning Energy Boost",
                "query": "morning acoustic coffee fresh wake up pop hits",
                "tempo": "medium",
            }
        elif 10 <= hour < 17:
            return {
                "period": "afternoon",
                "kicker": "WORK & FOCUS FLOW",
                "title": "Deep Focus & Daytime Beats",
                "shelf_title": "Daytime Flow",
                "query": "study focus lofi beats instrumental concentration flow",
                "tempo": "steady",
            }
        elif 17 <= hour < 22:
            title = "Weekend Party & High Energy" if is_weekend else "Golden Hour Vibes & Sunset Chill"
            query = "party dance club bangers viral hits" if is_weekend else "sunset chill acoustic melodies feel good evening"
            return {
                "period": "evening",
                "kicker": "EVENING VIBES",
                "title": title,
                "shelf_title": "Evening Chill & Wind Down",
                "query": query,
                "tempo": "upbeat" if is_weekend else "relaxing",
            }
        else:
            return {
                "period": "night",
                "kicker": "NIGHT DRIVE",
                "title": "Midnight Chill & Deep Melodies",
                "shelf_title": "Night Drive 2026",
                "query": "late night chill slow aesthetic songs",
                "tempo": "mellow",
            }

    # =========================================================================
    # 2. LOCATION & REGIONAL CONTEXT ANALYSIS
    # =========================================================================
    @staticmethod
    def get_location_context() -> Dict[str, Any]:
        """
        Detects user's regional affinity from system timezone and environment.
        """
        tz_str = " ".join(time.tzname).lower()
        env_tz = os.environ.get("TZ", "").lower()
        is_south_asia = any(k in tz_str or k in env_tz for k in ["india", "calcutta", "kolkata", "ist", "asia/kolkata"])

        if is_south_asia:
            return {
                "region": "South Asia / India",
                "is_regional": True,
                "kicker": "TRENDING IN YOUR REGION",
                "title": "Hot Regional Hits & Desi Vibes",
                "query": "trending hindi punjabi hits",
                "alt_query": "top bollywood punjabi viral hits",
            }
        else:
            return {
                "region": "Global",
                "is_regional": False,
                "kicker": "REGIONAL HITS & LOCAL GEMS",
                "title": "Trending Nearby & Local Vault",
                "query": "trending global music viral hits",
                "alt_query": "billboard top global hits",
            }

    # =========================================================================
    # 3. MOOD CONTEXT ARBITRATION
    # =========================================================================
    @staticmethod
    def get_mood_context(mood: str) -> Dict[str, Any]:
        """
        Maps the active Home screen mood chip to rich multi-source query terms.
        """
        clean = (mood or "All").strip()
        mood_table = {
            "Relax": {
                "kicker": "CHILL & UNWIND",
                "title": "Relaxing Acoustic & Lo-Fi",
                "query": "relaxing acoustic chill music lofi beats",
                "spotify_key": "chill",
            },
            "Sleep": {
                "kicker": "BEDTIME ATMOSPHERE",
                "title": "Deep Sleep & Calm Ambient",
                "query": "deep sleep ambient calm piano rain soothing",
                "spotify_key": "chill",
            },
            "Energize": {
                "kicker": "HIGH ENERGY MOTIVATION",
                "title": "Energize & Uplifting Pop",
                "query": "energizing upbeat motivation pop high energy",
                "spotify_key": "top_hits",
            },
            "Sad": {
                "kicker": "HEARTFELT & EMOTIONAL",
                "title": "Melancholic & Acoustic Ballads",
                "query": "sad songs slow melancholic acoustic ballads",
                "spotify_key": "chill",
            },
            "Romance": {
                "kicker": "ROMANTIC MELODIES",
                "title": "Soulful Love Songs & Duets",
                "query": "romantic love songs acoustic hindi english melodies",
                "spotify_key": "chill",
            },
            "Feel Good": {
                "kicker": "SUNNY VIBES",
                "title": "Feel Good & Happy Hits",
                "query": "feel good happy upbeat pop sunny morning",
                "spotify_key": "top_hits",
            },
            "Workout": {
                "kicker": "POWER & ADRENALINE",
                "title": "Workout Gym Phonk & Energy",
                "query": "gym workout phonk motivation electronic cardio",
                "spotify_key": "workout",
            },
            "Party": {
                "kicker": "DANCE & CLUB BANGERS",
                "title": "Party Hits & Club Bangers",
                "query": "party dance hits club bangers edm 2026",
                "spotify_key": "top_hits",
            },
            "Commute": {
                "kicker": "ON THE ROAD",
                "title": "Road Trip & Highway Commute",
                "query": "road trip driving car hits highway commute beats",
                "spotify_key": "top_hits",
            },
            "Focus": {
                "kicker": "DEEP WORK FLOW",
                "title": "Study Beats & Instrumental Focus",
                "query": "lofi study beats instrumental focus concentration",
                "spotify_key": "chill",
            },
        }
        return mood_table.get(clean, {
            "kicker": "PERSONALIZED DISCOVERY",
            "title": "Quick picks",
            "query": "trending global music hits official audio",
            "spotify_key": "top_hits",
        })

    # =========================================================================
    # 4. LISTENER BEHAVIOR & EXPLICIT FEATURE CONTRACTS
    # =========================================================================
    def get_listener_profile(self, context_keywords: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Aggregates listener behavior from SQLite storage (`tracks` + `listening_events` +
        `trend_observations`) and builds an explicit `ListenerFeatures` contract.
        """
        top_artists_rows = get_top_artists(limit=8)
        top_artists = [r["artist"] for r in top_artists_rows if r.get("artist")]
        max_art_w = max([float(r.get("total_plays") or r.get("track_count") or 1) for r in top_artists_rows], default=1.0)
        artist_affinities = {
            str(r["artist"]).strip().lower(): min(1.0, float(r.get("total_plays") or r.get("track_count") or 0) / max_art_w)
            for r in top_artists_rows if r.get("artist")
        }

        top_genre_rows = get_top_genres(limit=8)
        max_gen_w = max([float(r.get("weight") or 1) for r in top_genre_rows], default=1.0)
        genre_affinities = {
            str(r["genre"]).strip().lower(): min(1.0, float(r.get("weight") or 0) / max_gen_w)
            for r in top_genre_rows if r.get("genre")
        }

        recent = get_recently_played(limit=12)
        on_repeat = get_on_repeat(limit=12)
        heavy = get_heavy_rotation(limit=12)
        forgotten = get_forgotten_favorites(limit=12)
        local = get_local_library_tracks(limit=12)

        events_stats = get_listening_event_stats()
        velocity_map = get_trending_velocity_map()
        total_plays = sum(int(s.get("play_count") or 0) for s in events_stats.values())
        total_skips = sum(int(s.get("skip_count") or 0) for s in events_stats.values())
        total_listen = sum(float(s.get("total_listen_seconds") or 0.0) for s in events_stats.values())

        listener_features = ListenerFeatures(
            artist_affinities=artist_affinities,
            genre_affinities=genre_affinities,
            total_plays=total_plays,
            total_skips=total_skips,
            total_listening_seconds=total_listen,
            context_keywords=tuple(context_keywords or ()),
        )

        primary_artist = top_artists[0] if top_artists else ""

        return {
            "top_artists": top_artists,
            "primary_artist": primary_artist,
            "recent": recent,
            "on_repeat": on_repeat,
            "heavy_rotation": heavy,
            "forgotten": forgotten,
            "local_tracks": local,
            "has_history": bool(recent or on_repeat),
            "listener_features": listener_features,
            "events_stats_map": events_stats,
            "velocity_map": velocity_map,
        }

    # =========================================================================
    # 5. MULTI-PROVIDER DATA HARVESTING (Spotify, JioSaavn, YouTube, Local)
    # =========================================================================
    def fetch_spotify_chart(self, chart_key: str = "top_hits", limit: int = 15) -> List[Dict[str, Any]]:
        """Extracts tracks from public curated Spotify playlists with memory caching."""
        cache_key = f"sp_chart_{chart_key}"
        if cache_key in self._cache:
            ts, data = self._cache[cache_key]
            if time.time() - ts < self._cache_ttl and len(data) >= 5:
                return data

        pl_id = SPOTIFY_CHART_PLAYLISTS.get(chart_key, SPOTIFY_CHART_PLAYLISTS["top_hits"])
        try:
            pl_data = self.spotify.get_playlist(pl_id)
            if pl_data and pl_data.get("tracks"):
                clean_tracks = []
                for idx, t in enumerate(pl_data["tracks"]):
                    if not t or is_podcast_item(t):
                        continue
                    clean_tracks.append({
                        "video_id": t.get("video_id", ""),
                        "title": t.get("title", "Unknown Title"),
                        "artist": t.get("artist", "Unknown Artist"),
                        "artwork": t.get("artwork", "album_art.png"),
                        "duration": t.get("duration", 180),
                        "url": t.get("url", ""),
                        "source": "spotify",
                        "media_type": "song",
                        "chart_rank": idx + 1,
                    })
                clean_tracks = clean_tracks[:limit]
                self._cache[cache_key] = (time.time(), clean_tracks)
                record_trend_observations(clean_tracks, default_source="spotify")
                return clean_tracks
        except Exception as e:
            logger.warning("Error fetching Spotify chart %s: %s", chart_key, e)

        return []

    def fetch_jiosaavn_trending(self, query: str = "trending hindi punjabi hits", limit: int = 15) -> List[Dict[str, Any]]:
        """Fetches high-fidelity 320kbps regional and trending tracks from JioSaavn."""
        cache_key = f"js_q_{query}"
        if cache_key in self._cache:
            ts, data = self._cache[cache_key]
            if time.time() - ts < self._cache_ttl and len(data) >= 5:
                return data

        try:
            results = self.jiosaavn.search(query, limit=limit)
            clean_tracks = []
            for idx, t in enumerate(results):
                if not t or is_podcast_item(t):
                    continue
                clean_tracks.append({
                    "video_id": t.get("video_id", ""),
                    "title": t.get("title", "Unknown Title"),
                    "artist": t.get("artist", "Unknown Artist"),
                    "artwork": t.get("artwork", "album_art.png"),
                    "duration": t.get("duration", 180),
                    "url": t.get("url", ""),
                    "stream_url": t.get("stream_url", ""),
                    "bitrate": 320,
                    "source": "jiosaavn",
                    "media_type": "song",
                    "chart_rank": idx + 1,
                })
            self._cache[cache_key] = (time.time(), clean_tracks)
            record_trend_observations(clean_tracks, default_source="jiosaavn")
            return clean_tracks
        except Exception as e:
            logger.warning("Error fetching JioSaavn trending: %s", e)

        return []

    def fetch_youtube_tracks(self, query: str, limit: int = 15) -> List[Dict[str, Any]]:
        """Flat metadata extraction for YouTube search and trending charts."""
        cache_key = f"yt_q_{query}"
        if cache_key in self._cache:
            ts, data = self._cache[cache_key]
            if time.time() - ts < self._cache_ttl and len(data) >= 5:
                return data

        try:
            info = fetch_youtube_metadata(f"ytsearch{limit}:{query}", extract_flat=True)
            entries = info.get("entries", []) if info else []
            clean_tracks = []
            for idx, entry in enumerate(entries):
                if not entry:
                    continue
                meta = parse_complete_media_metadata(entry)
                if not meta or not meta.get("video_id") or is_podcast_item(entry):
                    continue
                clean_tracks.append({
                    "video_id": meta["video_id"],
                    "title": meta["title"],
                    "artist": meta["artist"],
                    "artwork": meta["artwork"] or "album_art.png",
                    "duration": meta["duration"],
                    "url": meta["url"],
                    "view_count": meta.get("view_count", 0),
                    "source": "youtube",
                    "media_type": "song",
                    "chart_rank": idx + 1,
                })
            self._cache[cache_key] = (time.time(), clean_tracks)
            record_trend_observations(clean_tracks, default_source="youtube")
            return clean_tracks
        except Exception as e:
            logger.warning("Error fetching YouTube query '%s': %s", query, e)

        return []

    # =========================================================================
    # 6. DYNAMIC SHELF GENERATOR (Non-Fixed, Context-Driven)
    # =========================================================================
    def build_dynamic_shelves(self, mood: str = "All", limit: int = 15, offline_only: bool = False) -> Dict[str, Dict[str, Any]]:
        """
        Synthesizes 6 context-driven shelves backed by explicit `ListenerFeatures`,
        `TrackFeatures`, multi-timestamp trending velocity, novelty saturation `1 - exp(-dt/tau)`,
        skip suppression, and canonical cross-provider deduplication.
        """
        time_ctx = self.get_time_context()
        loc_ctx = self.get_location_context()
        mood_ctx = self.get_mood_context(mood)
        is_mood_active = bool(mood and mood.strip() != "All")

        ctx_tokens = (mood_ctx["query"] + " " + time_ctx["query"]).split()[:6]
        profile = self.get_listener_profile(context_keywords=ctx_tokens)
        listener: ListenerFeatures = profile["listener_features"]
        events_stats = profile["events_stats_map"]
        velocity_map = profile["velocity_map"]

        is_headless = (os.environ.get("KIVY_HEADLESS") == "1")
        use_network = not (offline_only or is_headless)

        # Pre-fetch multi-provider data under a shared 5.0s wall-clock budget
        yt_mood, js_mood = [], []
        sp_trending, yt_trending = [], []
        js_art, js_reg, time_yt = [], [], []

        if use_network:
            futures = {}
            if is_mood_active:
                futures[self._executor.submit(self.fetch_youtube_tracks, mood_ctx["query"], 8)] = "yt_mood"
                futures[self._executor.submit(self.fetch_jiosaavn_trending, mood_ctx["query"], 8)] = "js_mood"
            futures[self._executor.submit(self.fetch_spotify_chart, "top_hits", 8)] = "sp_trending"
            futures[self._executor.submit(self.fetch_youtube_tracks, "trending music hits global charts official audio", 8)] = "yt_trending"

            top_art = profile.get("primary_artist", "")
            if top_art:
                futures[self._executor.submit(self.fetch_jiosaavn_trending, f"{top_art} songs hits", 8)] = "js_art"
            futures[self._executor.submit(self.fetch_jiosaavn_trending, loc_ctx["query"], 10)] = "js_reg"
            futures[self._executor.submit(self.fetch_youtube_tracks, time_ctx["query"], 10)] = "time_yt"

            try:
                for fut in as_completed(futures, timeout=5.0):
                    key = futures[fut]
                    try:
                        res = fut.result()
                        if key == "yt_mood":
                            yt_mood = res
                        elif key == "js_mood":
                            js_mood = res
                        elif key == "sp_trending":
                            sp_trending = res
                        elif key == "yt_trending":
                            yt_trending = res
                        elif key == "js_art":
                            js_art = res
                        elif key == "js_reg":
                            js_reg = res
                        elif key == "time_yt":
                            time_yt = res
                    except Exception as e:
                        logger.debug("Parallel fetch %s error: %s", key, e)
            except Exception:
                logger.debug("Parallel recommendation harvest hit 5s budget")

        # Refresh velocity_map after parallel chart observations landed
        if use_network:
            velocity_map = get_trending_velocity_map()

        all_lib = get_all_tracks()

        def _rank_shelf(candidates: List[Dict[str, Any]], mode: str) -> List[Dict[str, Any]]:
            ranked = rank_and_deduplicate_tracks(
                candidates,
                listener=listener,
                mode=mode,
                limit=limit,
                velocity_map=velocity_map,
                events_stats_map=events_stats,
            )
            min_target = min(limit, 4)
            if len(ranked) < min_target and all_lib:
                seen_ids = {t.get("video_id") for t in ranked if t.get("video_id")}
                seen_keys = {canonical_track_key(t) for t in ranked}
                fallback_extra = [
                    t for t in all_lib
                    if t.get("video_id") not in seen_ids and canonical_track_key(t) not in seen_keys
                ]
                ranked.extend(
                    rank_and_deduplicate_tracks(
                        fallback_extra,
                        listener=listener,
                        mode=mode,
                        limit=min_target - len(ranked),
                        velocity_map=velocity_map,
                        events_stats_map=events_stats,
                    )
                )
            return ranked[:limit]

        # Shelf 1: Quick Picks / Mood Power Picks (Discovery weighting with novelty 1 - exp(-dt/tau))
        if is_mood_active:
            s1_kicker = f"{mood.upper()} PICKS • START RADIO"
            s1_title = f"{mood} Power Picks"
            s1_candidates = yt_mood + js_mood + profile["forgotten"] + profile["recent"]
        else:
            s1_kicker = f"TAILORED FOR YOU • {time_ctx['kicker']}"
            s1_title = "Quick picks"
            s1_candidates = profile["forgotten"] + profile["recent"] + profile["on_repeat"] + profile["local_tracks"]

        # Shelf 2: Jump Back In & Heavy Rotation (Recall weighting: recency + engagement)
        s2_kicker = "PICK UP WHERE YOU LEFT OFF"
        s2_title = "Jump back in & Heavy rotation"
        s2_candidates = profile["heavy_rotation"] + profile["recent"] + profile["on_repeat"]

        # Shelf 3: Trending Across YouTube, Spotify & JioSaavn (Multi-timestamp velocity weighted)
        s3_kicker = "CHARTS & VIRAL HITS"
        s3_title = "Trending on YouTube & Spotify"
        s3_candidates = sp_trending + yt_trending + profile["heavy_rotation"][:4]

        # Shelf 4: Artists You Love / Behavioral Recommendation
        top_art = profile["primary_artist"]
        if top_art:
            s4_kicker = f"ARTISTS YOU LOVE • {top_art.upper()}"
            s4_title = f"Heavy Rotation & Related to {top_art}"
            art_hist = [t for t in (profile["on_repeat"] + profile["heavy_rotation"]) if t.get("artist") == top_art]
            s4_candidates = art_hist + js_art + profile["heavy_rotation"]
        else:
            s4_kicker = "FROM YOUR LISTENING HISTORY"
            s4_title = "Made for you"
            s4_candidates = profile["heavy_rotation"]

        # Shelf 5: Regional Hits & Local Vault (JioSaavn + Local Audio Files)
        s5_kicker = loc_ctx["kicker"]
        s5_title = loc_ctx["title"]
        s5_candidates = profile["local_tracks"] + js_reg + profile["recent"]

        # Shelf 6: Contextual Time-of-Day Vibe / Daily Mix
        s6_kicker = time_ctx["kicker"]
        s6_title = time_ctx["title"]
        s6_candidates = time_yt + get_daily_mix(limit=12)

        return {
            "quick_picks": {
                "kicker": s1_kicker,
                "title": s1_title,
                "tracks": _rank_shelf(s1_candidates, mode="discovery"),
            },
            "listen_again": {
                "kicker": s2_kicker,
                "title": s2_title,
                "tracks": _rank_shelf(s2_candidates, mode="recall"),
            },
            "trending": {
                "kicker": s3_kicker,
                "title": s3_title,
                "tracks": _rank_shelf(s3_candidates, mode="trending"),
            },
            "featured": {
                "kicker": s4_kicker,
                "title": s4_title,
                "tracks": _rank_shelf(s4_candidates, mode="discovery"),
            },
            "forgotten": {
                "kicker": s5_kicker,
                "title": s5_title,
                "tracks": _rank_shelf(s5_candidates, mode="regional"),
            },
            "daily_mix": {
                "kicker": s6_kicker,
                "title": s6_title,
                "tracks": _rank_shelf(s6_candidates, mode="discovery"),
            },
        }

    # =========================================================================
    # 7. DYNAMIC PLAYLIST ROUTING FOR PLAYLISTSCREEN
    # =========================================================================
    def get_dynamic_playlist(self, playlist_name: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Dynamically generates full tracklists for dynamic category playlists
        requested by PlaylistScreen or shelf 'Play all' buttons.
        """
        clean = (playlist_name or "").strip()
        time_ctx = self.get_time_context()
        loc_ctx = self.get_location_context()

        if clean in ("Top Charts", "Global Top 50", "YouTube Global Top 50"):
            sp = self.fetch_spotify_chart("top_hits", limit=limit // 2)
            yt = self.fetch_youtube_tracks("billboard global top 50 official music", limit=limit // 2)
            return (sp + yt)[:limit]
        elif clean in ("Viral Hits Today", "Trending Hits"):
            sp = self.fetch_spotify_chart("viral_global", limit=limit // 2)
            yt = self.fetch_youtube_tracks("viral hits today trending songs official audio", limit=limit // 2)
            return (sp + yt)[:limit]
        elif clean in ("Hot Hits Regional", "Trending Regional"):
            return self.fetch_jiosaavn_trending(loc_ctx["query"], limit=limit)
        elif clean == "Late Night":
            return self.fetch_youtube_tracks("late night drive slow chill aesthetic songs audio", limit=limit)
        elif clean == "Workout":
            sp = self.fetch_spotify_chart("workout", limit=limit // 2)
            yt = self.fetch_youtube_tracks("workout gym motivation high energy music audio", limit=limit // 2)
            return (sp + yt)[:limit]
        elif clean == "Chillwave":
            return self.fetch_youtube_tracks("chillwave lofi beats relaxing study audio", limit=limit)
        elif clean == "On Repeat":
            return get_on_repeat(limit=limit)
        elif clean == "Heavy Rotation":
            return get_heavy_rotation(limit=limit)
        elif clean == "Forgotten Favorites":
            return get_forgotten_favorites(limit=limit)
        elif clean == "Your Daily Mix":
            return get_daily_mix(limit=limit)

        # Fallback query search
        return self.fetch_youtube_tracks(f"{clean} official music hits audio", limit=limit)
