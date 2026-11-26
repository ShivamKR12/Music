"""Catalog, Home Shelves, Recommendations, Library, Artist/Album/Podcasts & Offline Coordinator."""

from __future__ import annotations

import os
import re
import threading
import time
from datetime import datetime
from typing import Any

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform
from kivymd.uix.bottomsheet import (
    MDBottomSheet,
    MDBottomSheetDragHandle,
    MDBottomSheetDragHandleButton,
    MDBottomSheetDragHandleTitle,
)
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemHeadlineText,
    MDListItemLeadingAvatar,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
    MDListItemTrailingIcon,
)
from kivymd.uix.scrollview import MDScrollView

from app_core.service_container import resolve_symbol
from models import database as db_mod
from models.track_model import TrackModel
from services.logger import app_logger
from utils import media_utils
from views.components import ArtistAlbumCard


class CatalogCoordinator:
    """Manages Home shelves, mood filters, library tabs, albums, artists, podcasts, favorites & local scan."""

    def __init__(self, app: Any):
        self.app = app

    @staticmethod
    def get_greeting() -> str:
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Good morning"
        if 12 <= hour < 17:
            return "Good afternoon"
        return "Good evening"

    @staticmethod
    def _track_card_data(t: TrackModel) -> dict:
        return {
            "title": t.title,
            "artist": t.artist,
            "artwork": t.album_art,
            "track_obj": t,
            "text": t.title,
        }

    def on_artwork_downloaded(self, track, art_path: str) -> None:
        track.album_art = art_path
        Clock.unschedule(self.debounced_refresh_views)
        Clock.schedule_once(self.debounced_refresh_views, 0.4)

    def debounced_refresh_views(self, dt=None) -> None:
        app = self.app
        app.populate_home_screen_data()
        if hasattr(app, "root") and app.root and hasattr(app.root, "ids") and "screen_manager" in app.root.ids:
            try:
                sm = app.root.ids.screen_manager
                if sm.has_screen("library"):
                    lib_screen = sm.get_screen("library")
                    if "library_list" in lib_screen.ids:
                        lib_screen.ids.library_list.data = [
                            {"title": t.title, "artist": t.artist, "artwork": t.album_art, "track_obj": t}
                            for t in app.playlist_model.tracks[:20]
                        ]
                if sm.has_screen("player") and sm.current == "player":
                    app.ensure_player_carousel(force_refresh=True)
            except Exception:
                pass

    def get_track_object_from_row(self, r: dict):
        app = self.app
        if hasattr(app, "playlist_model") and app.playlist_model.tracks:
            vid = r.get("video_id")
            path = r.get("local_path")
            title = r.get("title")
            for t in app.playlist_model.tracks:
                if (vid and t.video_id == vid) or (path and t.local_path == path) or (title and t.title == title):
                    return t
        from models.track_model import Track

        return Track(
            title=r.get("title") or "Unknown Title",
            artist=r.get("artist") or "Unknown Artist",
            url=r.get("url") or "",
            local_path=r.get("local_path") or "",
            video_id=r.get("video_id") or "",
            album_art=r.get("artwork") or "album_art.png",
            duration=r.get("duration") or 180,
            is_downloaded=bool(r.get("local_path")),
        )

    def load_recently_played_data(self) -> None:
        app = self.app
        if not hasattr(app, "root") or not app.root or not hasattr(app.root, "ids") or "screen_manager" not in app.root.ids:
            Clock.schedule_once(lambda dt: app.start_warmup_pipeline(), 0.05)
            return
        sm = app.root.ids.screen_manager
        if not sm.has_screen("recently_played"):
            return
        try:
            recent_screen = sm.get_screen("recently_played")
            if "recent_list" not in recent_screen.ids:
                return
            get_recent_pl = resolve_symbol("get_recently_played", db_mod.get_recently_played)
            get_recent_add = resolve_symbol("get_recently_added", db_mod.get_recently_added)
            rows = get_recent_pl(limit=50)
            if not rows:
                rows = get_recent_add(limit=30)
            data = []
            if rows:
                for r in rows:
                    data.append({
                        "title": r.get("title") or "Unknown Title",
                        "artist": r.get("artist") or "Unknown Artist",
                        "artwork": r.get("artwork") or "album_art.png",
                        "track_obj": app.get_track_object_from_row(r),
                    })
            elif hasattr(app, "playlist_model") and app.playlist_model.tracks:
                for t in app.playlist_model.tracks:
                    data.append({
                        "title": t.title,
                        "artist": t.artist,
                        "artwork": t.album_art if t.album_art else "album_art.png",
                        "track_obj": t,
                    })
            recent_screen.ids.recent_list.data = data
        except Exception as e:
            app_logger.error(f"Error loading recently played data: {e}")

    def load_analytics_data(self) -> None:
        app = self.app
        if not hasattr(app, "root") or not app.root or not hasattr(app.root, "ids") or "screen_manager" not in app.root.ids:
            Clock.schedule_once(lambda dt: app.start_warmup_pipeline(), 0.05)
            return
        sm = app.root.ids.screen_manager
        if not sm.has_screen("analytics"):
            return
        try:
            screen = sm.get_screen("analytics")
            summary = db_mod.get_library_analytics_summary()

            screen.total_tracks_text = f"{summary['total_tracks']} Tracks"
            screen.total_artists_text = f"{summary['total_artists']} Artists"

            total_sec = summary["total_seconds"]
            screen.total_playtime_text = f"{int(total_sec // 3600)}h {int((total_sec % 3600) // 60)}m"

            top_row = summary.get("top_track")
            screen.most_played_text = (
                f"{top_row.get('title', 'None')} • {top_row.get('artist', '')}" if top_row else "No Tracks Yet"
            )

            top_artists = summary.get("top_artists") or []
            if top_artists:
                total_top = sum(a["c"] for a in top_artists) or 1
                pcts = [a["c"] / total_top for a in top_artists]
                screen.segment_1_name = top_artists[0]["artist"]
                screen.segment_1_pct = f"{int(pcts[0] * 100)}%"
                end_1 = int(pcts[0] * 360)
                screen.segment_1_end = max(10, end_1)

                if len(top_artists) > 1:
                    screen.segment_2_name = top_artists[1]["artist"]
                    screen.segment_2_pct = f"{int(pcts[1] * 100)}%"
                    screen.segment_2_end = max(end_1 + 10, end_1 + int(pcts[1] * 360))
                else:
                    screen.segment_2_name = ""
                    screen.segment_2_pct = ""
                    screen.segment_2_end = 360

                if len(top_artists) > 2:
                    screen.segment_3_name = top_artists[2]["artist"]
                    screen.segment_3_pct = f"{int(pcts[2] * 100)}%"
                    screen.segment_3_end = 360
                else:
                    screen.segment_3_name = ""
                    screen.segment_3_pct = ""
                    screen.segment_3_end = 360

            dow_counts = summary.get("dow_counts") or {}
            days = ["1", "2", "3", "4", "5", "6", "0"]
            counts = [dow_counts.get(d, 0) for d in days]
            max_c = max(counts) if max(counts) > 0 else 0
            if max_c == 0:
                screen.bar_mon_h = 0.4
                screen.bar_tue_h = 0.75
                screen.bar_wed_h = 0.5
                screen.bar_thu_h = 0.85
                screen.bar_fri_h = 0.95
                screen.bar_sat_h = 1.0
                screen.bar_sun_h = 0.65
            else:
                heights = [max(0.1, c / max_c) for c in counts]
                (
                    screen.bar_mon_h,
                    screen.bar_tue_h,
                    screen.bar_wed_h,
                    screen.bar_thu_h,
                    screen.bar_fri_h,
                    screen.bar_sat_h,
                    screen.bar_sun_h,
                ) = heights
        except Exception as e:
            app_logger.error(f"Error loading analytics data: {e}")

    def populate_home_screen_data(self) -> None:
        app = self.app
        if not hasattr(app, "root") or not app.root or not hasattr(app.root, "ids") or "screen_manager" not in app.root.ids:
            Clock.schedule_once(lambda dt: app.start_warmup_pipeline(), 0.05)
            return
        try:
            home = app.root.ids.screen_manager.get_screen("home")
            tracks = [t for t in app.playlist_model.tracks if t.media_type != "podcast" and not media_utils.is_podcast_item(t.to_dict())]
            if not tracks:
                return

            app.home_greeting = app.get_greeting()

            from services.recommendation_engine import DynamicRecommendationEngine

            rec_engine = DynamicRecommendationEngine()
            time_ctx = rec_engine.get_time_context()
            loc_ctx = rec_engine.get_location_context()
            is_mood_active = bool(app.home_mood and app.home_mood.strip() != "All")

            if "quick_picks_kicker" in home.ids:
                home.ids.quick_picks_kicker.text = (
                    f"{app.home_mood.upper()} PICKS • START RADIO" if is_mood_active else f"TAILORED FOR YOU • {time_ctx['kicker']}"
                )
            if "quick_picks_title" in home.ids:
                home.ids.quick_picks_title.text = f"{app.home_mood} Power Picks" if is_mood_active else "Quick picks"
            if "listen_again_kicker" in home.ids:
                home.ids.listen_again_kicker.text = "PICK UP WHERE YOU LEFT OFF"
            if "listen_again_title" in home.ids:
                home.ids.listen_again_title.text = "Listen again"
            if "trending_kicker" in home.ids:
                home.ids.trending_kicker.text = "CHARTS & VIRAL HITS"
            if "trending_title" in home.ids:
                home.ids.trending_title.text = "Trending now"
            if "featured_kicker" in home.ids:
                top_art_rows = db_mod.get_top_artists(limit=1)
                top_art = top_art_rows[0]["artist"] if top_art_rows else ""
                home.ids.featured_kicker.text = f"ARTISTS YOU LOVE • {top_art.upper()}" if top_art else "FROM YOUR LISTENING HISTORY"
            if "featured_title" in home.ids:
                top_art_rows = db_mod.get_top_artists(limit=1)
                top_art = top_art_rows[0]["artist"] if top_art_rows else ""
                home.ids.featured_title.text = f"Heavy Rotation & Related to {top_art}" if top_art else "Made for you"
            if "forgotten_favorites_kicker" in home.ids:
                home.ids.forgotten_favorites_kicker.text = loc_ctx["kicker"]
            if "forgotten_favorites_title" in home.ids:
                home.ids.forgotten_favorites_title.text = "Forgotten favorites"
            if "daily_mix_kicker" in home.ids:
                home.ids.daily_mix_kicker.text = time_ctx["kicker"]
            if "daily_mix_title" in home.ids:
                home.ids.daily_mix_title.text = time_ctx["title"]

            def _row_track(row):
                try:
                    if isinstance(row, dict):
                        if row.get("media_type") == "podcast" or media_utils.is_podcast_item(row):
                            return None
                        vid = row.get("video_id", "")
                        t = app.playlist_model.find_track(vid) if vid else None
                        if t and (t.media_type == "podcast" or media_utils.is_podcast_item(t.to_dict())):
                            return None
                        cand = t or TrackModel.from_dict(row)
                        if cand.media_type == "podcast" or media_utils.is_podcast_item(cand.to_dict()):
                            return None
                        return cand
                    vid = row[3] if len(row) > 3 else None
                    t = app.playlist_model.find_track(vid) if vid else None
                    if t and (t.media_type == "podcast" or media_utils.is_podcast_item(t.to_dict())):
                        return None
                    return t
                except Exception:
                    return None

            def _set_rv_data(rv_id, new_data):
                if rv_id in home.ids:
                    rv = home.ids[rv_id]
                    if getattr(rv, "data", None) != new_data:
                        rv.data = new_data

            shelf_limit = 15
            get_cont = resolve_symbol("get_continue_listening", db_mod.get_continue_listening)
            get_rec_pl = resolve_symbol("get_recently_played", db_mod.get_recently_played)
            get_pl_tr = resolve_symbol("get_playlist_tracks", db_mod.get_playlist_tracks)
            get_rep = resolve_symbol("get_on_repeat", db_mod.get_on_repeat)
            get_hvy = resolve_symbol("get_heavy_rotation", db_mod.get_heavy_rotation)

            quick_picks_tracks = []
            try:
                for row in get_cont(limit=8):
                    t = _row_track(row)
                    if t and t not in quick_picks_tracks:
                        quick_picks_tracks.append(t)
            except Exception:
                pass
            for t in tracks:
                if t not in quick_picks_tracks:
                    quick_picks_tracks.append(t)
            quick_picks_tracks = quick_picks_tracks[:shelf_limit]
            _set_rv_data("quick_picks_list", [self._track_card_data(t) for t in quick_picks_tracks])

            listen_again_tracks = []
            try:
                for row in get_rec_pl(limit=shelf_limit):
                    t = _row_track(row)
                    if t and t not in listen_again_tracks:
                        listen_again_tracks.append(t)
            except Exception:
                pass
            _set_rv_data("listen_again_list", [self._track_card_data(t) for t in listen_again_tracks])

            mood_playlists_data = [
                {"name": "Chillwave", "subtitle": "Relax & Study Lo-Fi", "artwork": "album_art.png"},
                {"name": "Late Night", "subtitle": "Midnight Ambient & Drive", "artwork": "album_art.png"},
                {"name": "Workout", "subtitle": "Gym Phonk & Energy", "artwork": "album_art.png"},
                {"name": "Feel Good", "subtitle": "Sunny & Happy Hits", "artwork": "album_art.png"},
                {"name": "Focus", "subtitle": "Deep Instrumental Flow", "artwork": "album_art.png"},
                {"name": "Romance", "subtitle": "Soulful Love Melodies", "artwork": "album_art.png"},
                {"name": "Party", "subtitle": "Club Bangers & EDM", "artwork": "album_art.png"},
                {"name": "Top Charts", "subtitle": "Global Billboard Hits", "artwork": "album_art.png"},
            ]
            try:
                covers = db_mod.get_playlist_covers()
                for p in mood_playlists_data:
                    cov = covers.get(p["name"])
                    if cov:
                        p["artwork"] = cov
                    elif tracks:
                        p["artwork"] = tracks[abs(hash(p["name"])) % len(tracks)].album_art
            except Exception:
                pass
            _set_rv_data("mood_playlists_list", mood_playlists_data)

            trending_tracks = []
            try:
                for row in get_pl_tr("Top Charts"):
                    t = _row_track(row)
                    if t and t not in trending_tracks:
                        trending_tracks.append(t)
            except Exception:
                pass
            if not trending_tracks:
                trending_tracks = tracks[::-1][:shelf_limit]
            _set_rv_data("trending_list", [self._track_card_data(t) for t in trending_tracks[:shelf_limit]])

            featured_tracks = []
            try:
                for row in get_rep(limit=shelf_limit):
                    t = _row_track(row)
                    if t and t not in featured_tracks:
                        featured_tracks.append(t)
            except Exception:
                pass
            if not featured_tracks:
                try:
                    for row in get_hvy(limit=shelf_limit):
                        t = _row_track(row)
                        if t and t not in featured_tracks:
                            featured_tracks.append(t)
                except Exception:
                    pass
            if not featured_tracks:
                featured_tracks = tracks[::2] + tracks[1::2]
            _set_rv_data("featured_list", [self._track_card_data(t) for t in featured_tracks[:shelf_limit]])

            pod_items = []
            try:
                cached_pods = db_mod.load_cache_payload("podcasts_cache")
                if not cached_pods:
                    cached_pods = db_mod.get_all_podcasts()
                if cached_pods and isinstance(cached_pods, list):
                    for row in cached_pods:
                        if isinstance(row, dict) and (row.get("media_type") == "podcast" or media_utils.is_podcast_item(row)):
                            t = TrackModel.from_dict(row)
                            pod_items.append({
                                "title": t.title,
                                "artist": t.channel or t.artist or "Podcast",
                                "artwork": t.album_art or "album_art.png",
                                "track_obj": t,
                                "text": t.title,
                            })
                if not pod_items:
                    for t in app.playlist_model.tracks:
                        if t.media_type == "podcast" or media_utils.is_podcast_item(t.to_dict()):
                            pod_items.append({
                                "title": t.title,
                                "artist": t.channel or t.artist or "Podcast",
                                "artwork": t.album_art or "album_art.png",
                                "track_obj": t,
                                "text": t.title,
                            })
            except Exception:
                pass
            _set_rv_data("home_podcasts_list", pod_items[:shelf_limit])

            forgotten_tracks = []
            try:
                for row in db_mod.get_forgotten_favorites(limit=shelf_limit):
                    t = _row_track(row)
                    if t and t not in forgotten_tracks:
                        forgotten_tracks.append(t)
            except Exception:
                pass
            if not forgotten_tracks:
                forgotten_tracks = tracks[::-1][:shelf_limit]
            _set_rv_data("forgotten_favorites_list", [self._track_card_data(t) for t in forgotten_tracks[:shelf_limit]])

            daily_mix_tracks = []
            try:
                for row in db_mod.get_daily_mix(limit=shelf_limit):
                    t = _row_track(row)
                    if t and t not in daily_mix_tracks:
                        daily_mix_tracks.append(t)
            except Exception:
                pass
            if not daily_mix_tracks:
                daily_mix_tracks = (tracks[1::2] + tracks[::2])[:shelf_limit]
            _set_rv_data("daily_mix_list", [self._track_card_data(t) for t in daily_mix_tracks[:shelf_limit]])

            if os.environ.get("KIVY_HEADLESS") != "1":
                threading.Thread(target=app._bg_fetch_dynamic_recommendations, args=(app.home_mood,), daemon=True).start()
        except Exception as e:
            app_logger.warning(f"populate_home_screen_data encountered non-fatal error: {e}")

    def bg_fetch_dynamic_recommendations(self, mood: str = "All") -> None:
        app = self.app
        try:
            from services.recommendation_engine import DynamicRecommendationEngine

            shelves = DynamicRecommendationEngine().build_dynamic_shelves(mood=mood, limit=15, offline_only=False)
            Clock.schedule_once(lambda dt: app._apply_dynamic_shelves(shelves), 0)
        except Exception as e:
            app_logger.warning(f"_bg_fetch_dynamic_recommendations error: {e}")

    def apply_dynamic_shelves(self, shelves: dict) -> None:
        app = self.app
        if not hasattr(app, "root") or not app.root or not hasattr(app.root, "ids") or "screen_manager" not in app.root.ids:
            return
        try:
            home = app.root.ids.screen_manager.get_screen("home")

            def _resolve_track_obj(item):
                if isinstance(item, TrackModel):
                    return item
                if isinstance(item, dict):
                    vid = item.get("video_id")
                    cand = app.playlist_model.find_track(vid) if vid else None
                    return cand or TrackModel.from_dict(item)
                return None

            def _card_data(item):
                track_obj = _resolve_track_obj(item)
                title = track_obj.title if track_obj else item.get("title", "")
                artist = track_obj.artist if track_obj else item.get("artist", "")
                art = track_obj.album_art if track_obj else (item.get("artwork") or "album_art.png")
                return {"title": title, "artist": artist, "artwork": art, "track_obj": track_obj, "text": title}

            shelf_mapping = [
                ("quick_picks", "quick_picks_kicker", "quick_picks_title", "quick_picks_list"),
                ("listen_again", "listen_again_kicker", "listen_again_title", "listen_again_list"),
                ("trending", "trending_kicker", "trending_title", "trending_list"),
                ("featured", "featured_kicker", "featured_title", "featured_list"),
                ("forgotten", "forgotten_favorites_kicker", "forgotten_favorites_title", "forgotten_favorites_list"),
                ("daily_mix", "daily_mix_kicker", "daily_mix_title", "daily_mix_list"),
            ]

            all_new_tracks = []
            for shelf_key, kicker_id, title_id, list_id in shelf_mapping:
                shelf_info = shelves.get(shelf_key, {})
                if kicker_id in home.ids and shelf_info.get("kicker"):
                    home.ids[kicker_id].text = shelf_info["kicker"]
                if title_id in home.ids and shelf_info.get("title"):
                    home.ids[title_id].text = shelf_info["title"]
                if list_id in home.ids and "tracks" in shelf_info and shelf_info["tracks"]:
                    home.ids[list_id].data = [_card_data(t) for t in shelf_info["tracks"]]
                    for t in shelf_info["tracks"]:
                        obj = _resolve_track_obj(t)
                        if obj:
                            all_new_tracks.append(obj)

            if all_new_tracks:
                ensure_dl = resolve_symbol("ensure_artworks_downloaded", media_utils.ensure_artworks_downloaded)
                ensure_dl(all_new_tracks, on_track_updated=app.on_artwork_downloaded)
        except Exception as e:
            app_logger.warning(f"_apply_dynamic_shelves error: {e}")

    def fetch_trending_tracks(self) -> None:
        app = self.app
        try:
            yt_meta = resolve_symbol("fetch_youtube_metadata", media_utils.fetch_youtube_metadata)
            info = yt_meta("ytsearch20:trending music hits global charts official audio", extract_flat=True)
            entries = info.get("entries", []) if info else []
            db_mod.add_playlist("Top Charts")
            for entry in entries:
                if not entry:
                    continue
                meta = media_utils.parse_complete_media_metadata(entry)
                if not meta or not meta.get("video_id"):
                    continue
                if meta.get("media_type") == "podcast" or media_utils.is_podcast_item(entry):
                    continue
                video_id = meta["video_id"]
                thumb = media_utils.get_thumbnail_path(video_id)
                db_mod.add_track(
                    video_id=video_id,
                    title=meta["title"],
                    artist=meta["artist"],
                    url=meta["url"],
                    duration=meta["duration"],
                    artwork=thumb or meta["artwork"],
                    album=meta.get("album", ""),
                    genre=meta.get("genre", ""),
                    description=meta.get("description", ""),
                    view_count=meta.get("view_count", 0),
                    like_count=meta.get("like_count", 0),
                    channel=meta.get("channel", ""),
                    channel_id=meta.get("channel_id", ""),
                    release_date=meta.get("release_date", ""),
                    chapters=meta.get("chapters", ""),
                    track_number=meta.get("track_number", 0),
                    media_type="song",
                )
                db_mod.add_track_to_playlist("Top Charts", video_id)
            app_logger.info(f"[THREAD SUCCESS] MusicApp._fetch_trending_tracks completed with {len(entries)} items")
            Clock.schedule_once(lambda dt: app._on_trending_fetched(), 0)
        except Exception as e:
            app_logger.error(f"[THREAD FAILED] MusicApp._fetch_trending_tracks error: {e}")

    def on_trending_fetched(self) -> None:
        app = self.app
        app.playlist_model.load_from_db()
        app.player_controller.rebuild_queue()
        app.refresh_library_data()
        app.populate_home_screen_data()
        app.ensure_player_carousel(force_refresh=True)
        ensure_dl = resolve_symbol("ensure_artworks_downloaded", media_utils.ensure_artworks_downloaded)
        ensure_dl(app.playlist_model.tracks, on_track_updated=app.on_artwork_downloaded)

    def select_mood_filter(self, chip_instance, mood: str) -> None:
        app = self.app
        if not (hasattr(app, "root") and app.root):
            return
        try:
            home = app.root.ids.screen_manager.get_screen("home")
            if "mood_box" in home.ids:
                for c in home.ids.mood_box.children:
                    c.active = (c == chip_instance)
            app.home_mood = mood

            from services.recommendation_engine import DynamicRecommendationEngine

            rec_engine = DynamicRecommendationEngine()
            if mood == "All":
                app.populate_home_screen_data()
            else:
                app.show_toast(f"Curating {mood} mix...")
                instant_shelves = rec_engine.build_dynamic_shelves(mood=mood, limit=15, offline_only=True)
                app._apply_dynamic_shelves(instant_shelves)
                if os.environ.get("KIVY_HEADLESS") != "1":
                    threading.Thread(target=app._bg_fetch_dynamic_recommendations, args=(mood,), daemon=True).start()
        except Exception as e:
            app_logger.debug(f"select_mood_filter error: {e}")

    def async_mood_search(self, mood: str) -> None:
        app = self.app
        try:
            from services.music_provider_router import MusicProviderRouter

            entries = MusicProviderRouter().search(f"{mood} music mix", provider="youtube", limit=12)
            Clock.schedule_once(lambda dt: app._on_mood_results(entries, mood), 0)
        except Exception:
            Clock.schedule_once(lambda dt: app.show_toast(f"{mood} picks unavailable"), 0)

    def on_mood_results(self, entries: list, mood: str) -> None:
        app = self.app
        try:
            home = app.root.ids.screen_manager.get_screen("home")
            rv_data, tracks = [], []
            for entry in entries:
                vid = entry.get("video_id") or entry.get("id", "")
                if not vid:
                    continue
                track_obj = TrackModel(
                    video_id=vid,
                    title=entry.get("title", "Unknown Title"),
                    artist=entry.get("artist") or entry.get("uploader") or "Unknown Artist",
                    url=entry.get("url", f"https://www.youtube.com/watch?v={vid}"),
                    duration=int(entry.get("duration", 0) or 180),
                    album_art=entry.get("artwork") or media_utils.get_thumbnail_path(vid),
                    source=entry.get("source", "youtube"),
                )
                tracks.append(track_obj)
                rv_data.append(self._track_card_data(track_obj))
            if "quick_picks_title" in home.ids:
                home.ids.quick_picks_title.text = f"{mood} picks"
            if "quick_picks_list" in home.ids:
                home.ids.quick_picks_list.data = rv_data
            if tracks:
                ensure_dl = resolve_symbol("ensure_artworks_downloaded", media_utils.ensure_artworks_downloaded)
                ensure_dl(tracks, on_track_updated=lambda t: None)
        except Exception as e:
            app_logger.debug(f"_on_mood_results error: {e}")

    def play_home_shelf(self, shelf_id: str) -> None:
        app = self.app
        try:
            home = app.root.ids.screen_manager.get_screen("home")
            if shelf_id not in home.ids:
                return
            tracks = [d["track_obj"] for d in home.ids[shelf_id].data if d.get("track_obj")]
            if not tracks:
                return
            app.active_playlist_tracks = tracks
            app.play_selected_track(tracks[0])
        except Exception as e:
            app_logger.debug(f"play_home_shelf({shelf_id}) error: {e}")

    def play_home_quick_picks(self) -> None:
        self.play_home_shelf("quick_picks_list")

    def select_library_filter(self, chip_instance, filter_name: str) -> None:
        app = self.app
        if hasattr(app, "root") and app.root:
            lib = app.root.ids.screen_manager.get_screen("library")
            if "library_chips_box" in lib.ids:
                for c in lib.ids.library_chips_box.children:
                    c.active = (c == chip_instance)
            if filter_name in ("Library", "Playlists", "Songs"):
                app.library_filter = filter_name
                if filter_name == "Playlists":
                    app._populate_playlists_grid()
                elif filter_name == "Songs":
                    app._sync_library_songs()
            elif filter_name == "Albums":
                app.open_album()
            elif filter_name == "Artists":
                app.open_artist()
            elif filter_name == "Downloaded":
                app.show_downloaded()

    def refresh_library_data(self) -> None:
        app = self.app
        if not hasattr(app, "root") or not app.root:
            return
        try:
            sm = app.root.ids.screen_manager
            if not sm.has_screen("library"):
                return
            lib = sm.get_screen("library")
            get_pl = resolve_symbol("get_playlist_tracks", db_mod.get_playlist_tracks)
            get_hvy = resolve_symbol("get_heavy_rotation", db_mod.get_heavy_rotation)
            get_rec_add = resolve_symbol("get_recently_added", db_mod.get_recently_added)

            fav_tracks = [TrackModel.from_dict(r) for r in get_pl("Favorites")]
            app._update_library_tile(lib, "favorites_fan", [t.album_art for t in fav_tracks])
            if "favorites_count_text" in lib.ids:
                lib.ids.favorites_count_text.text = (
                    f"{len(fav_tracks)} songs" if fav_tracks else "Tap the heart on any song to save it here"
                )

            artists = {}
            for t in (app.playlist_model.tracks if getattr(app, "playlist_model", None) else []):
                name = (t.artist or "Unknown Artist").strip()
                if name and name not in artists:
                    artists[name] = t.album_art or ""
            app._update_library_tile(lib, "artists_fan", list(artists.values()))
            if "artists_count_text" in lib.ids:
                lib.ids.artists_count_text.text = f"{len(artists)} artist{'s' if len(artists) != 1 else ''}"

            mp_tracks = [TrackModel.from_dict(r) for r in get_hvy(limit=3)]
            app._update_library_tile(lib, "most_played_fan", [t.album_art for t in mp_tracks])
            if "most_played_count_text" in lib.ids:
                lib.ids.most_played_count_text.text = f"{len(mp_tracks)} tracks"

            dl_tracks = [TrackModel.from_dict(r) for r in get_pl("Offline Songs")]
            app._update_library_tile(lib, "downloaded_fan", [t.album_art for t in dl_tracks])
            if "downloaded_count_text" in lib.ids:
                lib.ids.downloaded_count_text.text = f"{len(dl_tracks)} songs" if dl_tracks else "Import local audio"

            if "recently_added_list" in lib.ids:
                ra = [TrackModel.from_dict(r) for r in get_rec_add(limit=10)]
                lib.ids.recently_added_list.data = [
                    {"title": t.title, "artist": t.artist, "artwork": t.album_art, "track_obj": t}
                    for t in ra
                ]
            app._sync_library_songs()
        except Exception as e:
            app_logger.error(f"[refresh_library_data error]: {e}")

    @staticmethod
    def update_library_tile(lib, fan_id: str, artworks: list) -> None:
        try:
            if fan_id in lib.ids:
                lib.ids[fan_id].artworks = [a for a in (artworks or []) if a][:3]
        except Exception as e:
            app_logger.error(f"[_update_library_tile error]: {e}")

    @staticmethod
    def is_user_library_playlist(name: str) -> bool:
        if not name or not isinstance(name, str):
            return False
        clean = name.strip()
        system_names = {
            "Podcasts", "Chillwave", "Late Night", "Workout", "Top Charts",
            "Viral Hits Today", "YouTube Global Top 50", "Global Top 50",
            "Your Daily Mix", "On Repeat", "Heavy Rotation", "Forgotten Favorites",
            "Favorites", "Offline Songs", "Relax", "Sleep", "Energize", "Sad",
            "Romance", "Feel Good", "Party", "Commute", "Focus", "Community Picks",
            "Radio Stations", "Trending Hits", "Hot Hits Regional", "Trending Regional",
            "Top Hits", "Todays Top Hits", "Today's Top Hits",
        }
        if clean in system_names:
            return False
        if clean.lower().startswith(("dynamic_pl_", "stress playlist", "[spotify]", "test playlist")):
            return False
        if any(c in clean for c in ("'", '"', "--", ";")):
            return False
        return True

    def populate_playlists_grid(self) -> None:
        app = self.app
        if not hasattr(app, "root") or not app.root:
            return
        try:
            sm = app.root.ids.screen_manager
            if not sm.has_screen("library"):
                return
            lib = sm.get_screen("library")
            grid = lib.ids.get("playlists_grid")
            if grid is None:
                return
            covers = db_mod.get_playlist_covers()
            data = [{"is_create": True, "name": "Create", "track_count": 0, "artwork": "album_art.png"}]
            for p in db_mod.get_all_playlists():
                p_name = p["name"]
                if not app.is_user_library_playlist(p_name):
                    continue
                data.append({
                    "is_create": False,
                    "name": p_name,
                    "track_count": p.get("track_count", 0) or 0,
                    "artwork": covers.get(p_name, ""),
                })
            grid.data = data
        except Exception as e:
            app_logger.error(f"[_populate_playlists_grid error]: {e}")

    def sync_library_songs(self) -> None:
        app = self.app
        if not hasattr(app, "root") or not app.root:
            return
        try:
            sm = app.root.ids.screen_manager
            if sm.has_screen("library"):
                lib = sm.get_screen("library")
                if "library_list" in lib.ids:
                    lib.ids.library_list.data = [
                        {"title": t.title, "artist": t.artist, "artwork": t.album_art, "track_obj": t}
                        for t in app.playlist_model.tracks[:20]
                    ]
        except Exception:
            pass

    def open_album(self, album_name="New Releases", artist_name="Various Artists", artwork="album_art.png", tracks=None) -> None:
        app = self.app
        app.active_album_name = album_name or "New Releases"
        app.active_album_artist = artist_name or "Various Artists"
        app.active_album_art = artwork or "album_art.png"
        app.switch_screen("album")

        if tracks:
            app.active_album_tracks = list(tracks)
            app.active_album_info = f"{len(tracks)} tracks • Album"
            app._render_album_tracks()
        else:
            matching = [
                t for t in app.playlist_model.tracks
                if (album_name.lower() in (t.title or "").lower() or artist_name.lower() in (t.artist or "").lower())
            ]
            if matching:
                app.active_album_tracks = matching
                app.active_album_info = f"{len(matching)} tracks • Album"
            else:
                app.active_album_tracks = []
                app.active_album_info = "Loading album tracks from YouTube..."
            app._render_album_tracks()
            app._fetch_album_tracks_async(app.active_album_name, app.active_album_artist)

    def render_album_tracks(self) -> None:
        app = self.app

        def _do_render(dt):
            if hasattr(app, "root") and app.root:
                try:
                    screen = app.root.ids.screen_manager.get_screen("album")
                    if "album_tracks_list" in screen.ids:
                        screen.ids.album_tracks_list.data = [
                            {"title": t.title, "artist": t.artist, "artwork": t.album_art or "album_art.png", "track_obj": t}
                            for t in app.active_album_tracks
                        ]
                except Exception as e:
                    app_logger.error(f"[_render_album_tracks error]: {e}")

        Clock.schedule_once(_do_render, 0)

    def fetch_album_tracks_async(self, album_name: str, artist_name: str) -> None:
        app = self.app
        app.album_loading = True
        yt_meta = resolve_symbol("fetch_youtube_metadata", media_utils.fetch_youtube_metadata)
        ensure_dl = resolve_symbol("ensure_artworks_downloaded", media_utils.ensure_artworks_downloaded)

        def _bg():
            try:
                query = f"ytsearch10:{album_name} {artist_name} full audio"
                info = yt_meta(query, extract_flat=True)
                entries = info.get("entries", []) if info else []
                new_tracks = []
                for entry in entries:
                    vid = entry.get("id")
                    if vid:
                        t_title = entry.get("title", "Unknown Title")
                        t_artist = entry.get("uploader") or entry.get("channel") or artist_name
                        t_url = entry.get("url", f"https://www.youtube.com/watch?v={vid}")
                        t_dur = int(entry.get("duration") or 0)
                        t_thumb = media_utils.get_thumbnail_path(vid)
                        db_mod.add_track(video_id=vid, title=t_title, artist=t_artist, url=t_url, duration=t_dur, artwork=t_thumb)
                        new_tracks.append(TrackModel(video_id=vid, title=t_title, artist=t_artist, url=t_url, duration=t_dur, album_art=t_thumb))
                if new_tracks:
                    def _apply(dt):
                        app.album_loading = False
                        if app.active_album_name != album_name:
                            return
                        app.active_album_tracks = new_tracks
                        app.active_album_info = f"{len(new_tracks)} tracks • Album"
                        if new_tracks[0].album_art and (not app.active_album_art or app.active_album_art == "album_art.png"):
                            app.active_album_art = new_tracks[0].album_art
                        app._render_album_tracks()
                        ensure_dl(new_tracks, on_track_updated=app.on_artwork_downloaded)

                    Clock.schedule_once(_apply, 0)
            except Exception as e:
                app_logger.error(f"[_fetch_album_tracks_async error]: {e}")
                Clock.schedule_once(lambda dt: setattr(app, "album_loading", False), 0)

        threading.Thread(target=_bg, daemon=True).start()

    def play_active_album(self, shuffle: bool = False) -> None:
        app = self.app
        tracks = getattr(app, "active_album_tracks", [])
        if not tracks:
            app.show_toast("No tracks available for this album yet.")
            return
        t_list = list(tracks)
        if shuffle:
            import random
            random.shuffle(t_list)
        first = t_list[0]
        app.player_controller.set_custom_queue(t_list, start_track=first)
        app.play_selected_track(first)

    def open_artist(self, artist_name=None) -> None:
        app = self.app
        if not artist_name:
            if hasattr(app, "player_controller") and app.player_controller.active_track and app.player_controller.active_track.artist:
                artist_name = app.player_controller.active_track.artist
            elif hasattr(app, "playlist_model") and app.playlist_model.tracks:
                artist_name = app.playlist_model.tracks[0].artist or "MC Square"
            else:
                artist_name = "MC Square"

        primary_artist = re.split(r",| feat\.?| ft\.?| & ", artist_name, flags=re.IGNORECASE)[0].strip() or artist_name
        all_tracks = []
        seen_ids = set()
        for source_list in (getattr(app, "offline_tracks", []), app.playlist_model.tracks if hasattr(app, "playlist_model") else []):
            for t in source_list:
                if t.video_id not in seen_ids:
                    seen_ids.add(t.video_id)
                    all_tracks.append(t)

        matching = [t for t in all_tracks if primary_artist.lower() in (t.artist or "").lower()]
        app.active_artist_name = primary_artist
        app.active_artist_art = matching[0].album_art if (matching and matching[0].album_art) else "album_art.png"
        app.active_artist_info = f"{len(matching)} Tracks • Library" if matching else "Fetching real artist discography from YouTube..."
        app.active_artist_tracks = matching

        app.switch_screen("artist")
        if hasattr(app, "root") and app.root:
            try:
                screen = app.root.ids.screen_manager.get_screen("artist")
                if "artist_tracks_list" in screen.ids:
                    screen.ids.artist_tracks_list.data = [
                        {"title": t.title, "artist": t.artist, "artwork": t.album_art if t.album_art else "album_art.png", "track_obj": t}
                        for t in matching
                    ]
                if "artist_albums_box" in screen.ids:
                    screen.ids.artist_albums_box.clear_widgets()
            except Exception as e:
                app_logger.error(f"[open_artist initial render error]: {e}")

        app._fetch_artist_data_async(primary_artist)

    def fetch_artist_data_async(self, primary_artist: str) -> None:
        app = self.app
        yt_meta = resolve_symbol("fetch_youtube_metadata", media_utils.fetch_youtube_metadata)
        ensure_dl = resolve_symbol("ensure_artworks_downloaded", media_utils.ensure_artworks_downloaded)

        def _bg():
            try:
                info = yt_meta(f"ytsearch12:{primary_artist} official songs audio", extract_flat=True)
                entries = info.get("entries", []) if info else []
                new_track_objs = []
                for entry in entries:
                    vid = entry.get("id")
                    if vid:
                        t_title = entry.get("title", "Unknown Title")
                        t_artist = entry.get("uploader") or entry.get("channel") or primary_artist
                        t_url = entry.get("url", f"https://www.youtube.com/watch?v={vid}")
                        t_dur = int(entry.get("duration") or 0)
                        t_thumb = media_utils.get_thumbnail_path(vid)
                        db_mod.add_track(video_id=vid, title=t_title, artist=t_artist, url=t_url, duration=t_dur, artwork=t_thumb)
                        new_track_objs.append(TrackModel(video_id=vid, title=t_title, artist=t_artist, url=t_url, duration=t_dur, album_art=t_thumb))

                alb_info = yt_meta(f"ytsearch6:{primary_artist} full album playlist audio", extract_flat=True)
                alb_entries = alb_info.get("entries", []) if alb_info else []
                albums_data = []
                for a_entry in alb_entries:
                    a_title = a_entry.get("title", "")
                    a_vid = a_entry.get("id")
                    if a_title and a_vid:
                        cleaned_title = re.sub(r"\[.*?\]|\(.*?\)|full album|official", "", a_title, flags=re.IGNORECASE).strip() or a_title[:30]
                        albums_data.append({
                            "title": cleaned_title,
                            "subtitle": "Album • Official",
                            "artwork": media_utils.get_thumbnail_path(a_vid),
                            "artist": primary_artist,
                        })

                if not albums_data and new_track_objs:
                    albums_data.append({
                        "title": f"Top Hits: {primary_artist}",
                        "subtitle": f"{len(new_track_objs)} Tracks • Collection",
                        "artwork": new_track_objs[0].album_art,
                        "artist": primary_artist,
                    })

                def _apply_artist_results(dt):
                    if app.active_artist_name != primary_artist:
                        return
                    combined = list(app.active_artist_tracks)
                    existing_vids = {t.video_id for t in combined}
                    for t in new_track_objs:
                        if t.video_id not in existing_vids:
                            existing_vids.add(t.video_id)
                            combined.append(t)
                    app.active_artist_tracks = combined
                    app.active_artist_info = f"{len(combined)} Tracks • Verified Discography"
                    if combined and (not app.active_artist_art or app.active_artist_art == "album_art.png"):
                        app.active_artist_art = combined[0].album_art or "album_art.png"

                    if hasattr(app, "root") and app.root:
                        try:
                            screen = app.root.ids.screen_manager.get_screen("artist")
                            if "artist_tracks_list" in screen.ids:
                                screen.ids.artist_tracks_list.data = [
                                    {"title": t.title, "artist": t.artist, "artwork": t.album_art if t.album_art else "album_art.png", "track_obj": t}
                                    for t in combined
                                ]
                            if "artist_albums_box" in screen.ids:
                                screen.ids.artist_albums_box.clear_widgets()
                                for alb in albums_data:
                                    screen.ids.artist_albums_box.add_widget(
                                        ArtistAlbumCard(
                                            title=alb["title"],
                                            subtitle=alb["subtitle"],
                                            artwork=alb["artwork"] or "album_art.png",
                                            artist=alb["artist"],
                                        )
                                    )
                        except Exception as e:
                            app_logger.error(f"[_apply_artist_results error]: {e}")
                    ensure_dl(combined, on_track_updated=app.on_artwork_downloaded)

                Clock.schedule_once(_apply_artist_results, 0)
            except Exception as e:
                app_logger.error(f"[_fetch_artist_data_async error]: {e}")

        threading.Thread(target=_bg, daemon=True).start()

    def play_active_artist(self, shuffle: bool = False) -> None:
        app = self.app
        tracks = getattr(app, "active_artist_tracks", [])
        if not tracks:
            app.show_toast("No tracks to play for this artist.")
            return
        t_list = list(tracks)
        if shuffle:
            import random
            random.shuffle(t_list)
        first = t_list[0]
        app.player_controller.set_custom_queue(t_list, start_track=first)
        app.play_selected_track(first)

    def show_artist(self, artist_name: str = "") -> None:
        self.open_artist(artist_name)

    def open_podcasts(self) -> None:
        self.app.switch_screen("podcasts")

    def load_podcasts_data(self) -> None:
        app = self.app
        try:
            cached_data = db_mod.load_cache_payload("podcasts_cache")
            if not cached_data:
                cached_data = db_mod.get_all_podcasts()
            if cached_data and isinstance(cached_data, list) and len(cached_data) > 0:
                p_tracks = [
                    TrackModel.from_dict(d)
                    for d in cached_data
                    if (isinstance(d, dict) and d.get("media_type") == "podcast")
                    or media_utils.is_podcast_item(d if isinstance(d, dict) else d.to_dict())
                ]
                if p_tracks:
                    app.podcast_featured_track = p_tracks[0]
                    app.podcast_featured_title = p_tracks[0].title
                    app.podcast_featured_desc = f"{p_tracks[0].artist} • Full Episode"
                    app.podcast_featured_art = p_tracks[0].album_art or "album_art.png"
                    app.podcast_tracks = p_tracks[1:]
                    app._render_podcasts_list()
        except Exception as e:
            app_logger.warning(f"[load_podcasts_data cache read error]: {e}")

        app.podcasts_loading = True
        yt_meta = resolve_symbol("fetch_youtube_metadata", media_utils.fetch_youtube_metadata)
        ensure_dl = resolve_symbol("ensure_artworks_downloaded", media_utils.ensure_artworks_downloaded)

        def _bg_podcasts():
            try:
                info = yt_meta("ytsearch12:popular podcast full episode audio", extract_flat=True)
                entries = info.get("entries", []) if info else []
                new_p_tracks = []
                db_mod.add_playlist("Podcasts")
                for entry in entries:
                    if not entry:
                        continue
                    meta = media_utils.parse_complete_media_metadata(entry)
                    if not meta or not meta.get("video_id"):
                        continue
                    vid = meta["video_id"]
                    t_thumb = media_utils.get_thumbnail_path(vid)
                    meta["media_type"] = "podcast"
                    db_mod.add_track(
                        video_id=vid,
                        title=meta["title"],
                        artist=meta["artist"],
                        url=meta["url"],
                        duration=meta["duration"],
                        artwork=t_thumb or meta["artwork"],
                        album=meta.get("album", ""),
                        genre=meta.get("genre", ""),
                        description=meta.get("description", ""),
                        view_count=meta.get("view_count", 0),
                        like_count=meta.get("like_count", 0),
                        channel=meta.get("channel", ""),
                        channel_id=meta.get("channel_id", ""),
                        release_date=meta.get("release_date", ""),
                        chapters=meta.get("chapters", ""),
                        track_number=meta.get("track_number", 0),
                        media_type="podcast",
                    )
                    db_mod.add_track_to_playlist("Podcasts", vid)
                    tm = TrackModel.from_dict(meta)
                    tm.album_art = t_thumb or meta["artwork"]
                    tm.media_type = "podcast"
                    new_p_tracks.append(tm)
                if new_p_tracks:
                    db_mod.save_cache_payload("podcasts_cache", [t.to_dict() for t in new_p_tracks])

                    def _apply_podcasts(dt):
                        app.podcasts_loading = False
                        app.podcast_featured_track = new_p_tracks[0]
                        app.podcast_featured_title = new_p_tracks[0].title
                        app.podcast_featured_desc = f"{new_p_tracks[0].artist} • Full Episode"
                        app.podcast_featured_art = new_p_tracks[0].album_art or "album_art.png"
                        app.podcast_tracks = new_p_tracks[1:]
                        app._render_podcasts_list()
                        ensure_dl(new_p_tracks, on_track_updated=app.on_artwork_downloaded)

                    Clock.schedule_once(_apply_podcasts, 0)
                else:
                    Clock.schedule_once(lambda dt: setattr(app, "podcasts_loading", False), 0)
            except Exception as e:
                app_logger.error(f"[_bg_podcasts error]: {e}")
                Clock.schedule_once(lambda dt: setattr(app, "podcasts_loading", False), 0)

        threading.Thread(target=_bg_podcasts, daemon=True).start()

    def render_podcasts_list(self) -> None:
        app = self.app

        def _do_render(dt):
            if hasattr(app, "root") and app.root:
                try:
                    screen = app.root.ids.screen_manager.get_screen("podcasts")
                    if "podcasts_list" in screen.ids:
                        screen.ids.podcasts_list.data = [
                            {"title": t.title, "artist": t.artist, "artwork": t.album_art or "album_art.png", "track_obj": t}
                            for t in app.podcast_tracks
                        ]
                except Exception as e:
                    app_logger.error(f"[_render_podcasts_list error]: {e}")

        Clock.schedule_once(_do_render, 0)

    def play_featured_podcast(self) -> None:
        app = self.app
        if app.podcast_featured_track:
            app.play_selected_track(app.podcast_featured_track)
        elif app.podcast_tracks:
            app.play_selected_track(app.podcast_tracks[0])
        elif hasattr(app, "playlist_model") and app.playlist_model.tracks:
            app.play_selected_track(app.playlist_model.tracks[0])
        else:
            app.show_toast("No podcast available to play yet.")

    def show_favorites(self) -> None:
        self.app.sync_favorites_screen()
        self.app.switch_screen("favorites")

    def play_favorites(self, shuffle: bool = False) -> None:
        app = self.app
        tracks = getattr(app, "favorites_tracks", [])
        if not tracks:
            app.show_toast("No favorite songs yet.")
            return
        t_list = list(tracks)
        if shuffle:
            import random
            random.shuffle(t_list)
        first = t_list[0]
        app.player_controller.set_custom_queue(t_list, start_track=first)
        app.play_selected_track(first)

    def sync_favorites_screen(self) -> None:
        app = self.app
        if not hasattr(app, "root") or not app.root:
            return
        try:
            fav_screen = app.root.ids.screen_manager.get_screen("favorites")
            if "favorites_track_list" not in fav_screen.ids:
                return
            container = fav_screen.ids.favorites_track_list
            fav_tracks = db_mod.get_playlist_tracks("Favorites")
            container.clear_widgets()
            track_objs = []
            for t_dict in fav_tracks or []:
                track_obj = TrackModel.from_dict(t_dict)
                track_objs.append(track_obj)
                container.add_widget(
                    MDListItem(
                        MDListItemLeadingAvatar(
                            source=track_obj.album_art if track_obj.album_art else "album_art.png",
                            radius=[dp(8)] * 4,
                        ),
                        MDListItemHeadlineText(text=track_obj.title),
                        MDListItemSupportingText(text=f"{track_obj.artist} • {track_obj.formatted_duration}"),
                        MDListItemTrailingIcon(
                            icon="heart",
                            theme_icon_color="Custom",
                            icon_color=app.theme_cls.primaryColor,
                        ),
                        on_release=lambda instance, t=track_obj: app.play_selected_track(t),
                    )
                )

            app.favorites_tracks = track_objs
            app.favorites_top_art = track_objs[0].album_art if (track_objs and track_objs[0].album_art) else "album_art2.png"
            tot_sec = sum(getattr(t, "duration", 0) for t in track_objs)
            app.favorites_info = f"Auto-synced • {len(track_objs)} tracks • {tot_sec // 60} min"
            if track_objs:
                ensure_dl = resolve_symbol("ensure_artworks_downloaded", media_utils.ensure_artworks_downloaded)
                ensure_dl(track_objs)
        except Exception as e:
            app_logger.error("Error syncing favorites screen: %s", e)

    def show_downloaded(self) -> None:
        tracks = db_mod.get_playlist_tracks("Offline Songs")
        if not tracks:
            self.app.scan_and_load_offline_songs(auto_play=False, show_screen=True)
        else:
            self.app.open_playlist("Offline Songs")

    def show_local_audio_options(self) -> None:
        app = self.app
        sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text="Local & Offline Audio"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: sheet.set_state("close")),
            ),
            size_hint_y=None,
            height="320dp",
            opening_time=0.2,
            closing_time=0.15,
        )
        scroll = MDScrollView(size_hint_y=None, height="240dp")
        dlist = MDList()
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="playlist-music"),
                MDListItemHeadlineText(text="Open Offline Songs Playlist"),
                MDListItemSupportingText(text="View and play all device music files"),
                on_release=lambda x: (sheet.set_state("close"), app.show_downloaded()),
            )
        )
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="folder-sync"),
                MDListItemHeadlineText(text="Scan Device for Music"),
                MDListItemSupportingText(text="Scan Music, Downloads, and storage folders"),
                on_release=lambda x: (sheet.set_state("close"), app.scan_and_load_offline_songs(show_screen=True)),
            )
        )
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="file-music-outline"),
                MDListItemHeadlineText(text="Select Specific File..."),
                MDListItemSupportingText(text="Pick an MP3, FLAC, or WAV file"),
                on_release=lambda x: (sheet.set_state("close"), app.file_manager_open()),
            )
        )
        scroll.add_widget(dlist)
        sheet.add_widget(scroll)
        Window.add_widget(sheet)
        sheet.width = Window.width
        sheet.x = 0
        sheet.set_state("open")

    def ensure_storage_permissions(self, callback=None) -> None:
        from services.android_media_lifecycle import (
            required_notification_permissions_for_sdk,
            required_storage_permissions_for_sdk,
        )

        if platform != "android":
            if callback:
                Clock.schedule_once(lambda dt: callback(True), 0)
            return

        def _do_check(dt=None):
            try:
                from jnius import autoclass
                from android.permissions import request_permissions, check_permission

                sdk_int = int(autoclass("android.os.Build$VERSION").SDK_INT)
                storage_perms = required_storage_permissions_for_sdk(sdk_int)
                notif_perms = required_notification_permissions_for_sdk(sdk_int)
                needed = []
                for p in storage_perms + notif_perms:
                    try:
                        if not check_permission(p):
                            needed.append(p)
                    except Exception:
                        needed.append(p)

                if not needed:
                    if callback:
                        Clock.schedule_once(lambda dt: callback(True), 0)
                    return

                def _on_permissions(permissions, grant_results):
                    res_map = dict(zip(permissions, grant_results))
                    app_logger.info("Android SDK %d permissions result: %s", sdk_int, res_map)
                    granted = any(bool(res_map.get(sp, False)) for sp in storage_perms)
                    if callback:
                        Clock.schedule_once(lambda dt: callback(granted), 0)

                request_permissions(needed, _on_permissions)
            except Exception as e:
                app_logger.warning("ensure_storage_permissions error: %s", e)
                if callback:
                    Clock.schedule_once(lambda dt: callback(True), 0)

        Clock.schedule_once(_do_check, 0)

    def scan_and_load_offline_songs(self, auto_play: bool = False, show_screen: bool = True) -> None:
        app = self.app

        def _execute_scan(granted=True):
            if not granted:
                app.show_toast("Storage permission needed to find offline songs")
                return
            if show_screen:
                app.show_toast("Scanning device for offline songs...")

            def _worker():
                try:
                    db_mod.clean_and_resync_offline_tracks(cache_dir=app.cache_dir)
                    db_tracks = db_mod.get_playlist_tracks("Offline Songs")
                    loaded_tracks = []
                    for meta in db_tracks:
                        vid = meta["video_id"]
                        t = app.playlist_model.get_track_by_video_id(vid)
                        if not t:
                            t = TrackModel.from_dict(meta)
                            app.playlist_model.add_track(t)
                        else:
                            t.title = meta.get("title", t.title)
                            t.artist = meta.get("artist", t.artist)
                            t.album_art = meta.get("artwork", t.album_art)
                            t.local_path = meta.get("local_path", t.local_path)
                            t.is_downloaded = True
                        loaded_tracks.append(t)
                        time.sleep(0.002)

                    def _finish(dt):
                        app.populate_home_screen_data()
                        if show_screen:
                            app.show_toast(f"Found {len(loaded_tracks)} offline songs!")
                            app.open_playlist("Offline Songs")
                        elif getattr(app, "active_playlist_name", "") == "Offline Songs":
                            app.sync_active_playlist_screen()
                        if auto_play and loaded_tracks:
                            app.player_controller.set_custom_queue(loaded_tracks, start_track=loaded_tracks[0])
                            app.play_selected_track(loaded_tracks[0])

                    Clock.schedule_once(_finish, 0)
                except Exception as e:
                    app_logger.error("scan_and_load_offline_songs error: %s", e)

            threading.Thread(target=_worker, daemon=True).start()

        app.ensure_storage_permissions(_execute_scan)
