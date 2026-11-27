"""Multi-Source Search, History, Autocomplete Suggestions & Direct URL Extraction Coordinator."""

from __future__ import annotations

import threading
from typing import Any

from kivy.clock import Clock

from app_core.service_container import resolve_symbol
from models import database as db_mod
from models.track_model import TrackModel
from services.logger import app_logger
from utils import media_utils


class SearchCoordinator:
    """Manages unified multi-source search, history persistence, URL resolvers & result rendering."""

    def __init__(self, app: Any):
        self.app = app

    def clear_search_input(self) -> None:
        app = self.app
        try:
            if hasattr(app, "root") and app.root:
                sm = app.root.ids.get("screen_manager")
                if sm and sm.has_screen("search"):
                    screen = sm.get_screen("search")
                    if "search_input" in screen.ids:
                        screen.ids.search_input.text = ""
            app.clear_search_results()
        except Exception as e:
            app_logger.debug(f"clear_search_input error: {e}")

    def set_search_provider(self, provider: str) -> None:
        app = self.app
        app.active_search_provider = provider
        msg = f"Search Source: {provider.upper()}" if provider != "all" else "Search Source: All Providers"
        app.show_toast(msg)
        try:
            search_screen = app.root.ids.screen_manager.get_screen("search")
            if "search_input" in search_screen.ids:
                q = search_screen.ids.search_input.text.strip()
                if q:
                    app.perform_search(q)
        except Exception:
            pass

    def load_search_history_from_db(self) -> None:
        app = self.app
        try:
            if hasattr(app, "root") and app.root:
                search_screen = app.root.ids.screen_manager.get_screen("search")
                if "search_history_list" in search_screen.ids:
                    get_hist = resolve_symbol("get_search_history", db_mod.get_search_history)
                    history = get_hist()
                    if history:
                        search_screen.ids.search_history_list.data = [{"text": q} for q in history]
        except Exception:
            pass

    def clear_search_history(self) -> None:
        app = self.app
        db_mod.clear_search_history_async()
        try:
            if hasattr(app, "root") and app.root:
                search_screen = app.root.ids.screen_manager.get_screen("search")
                if "search_history_list" in search_screen.ids:
                    search_screen.ids.search_history_list.data = []
        except Exception:
            pass

    def clear_search_results(self) -> None:
        app = self.app
        app.search_state = "empty"
        app.search_loading = False
        try:
            if hasattr(app, "root") and app.root:
                search_screen = app.root.ids.screen_manager.get_screen("search")
                if "search_input" in search_screen.ids:
                    search_screen.ids.search_input.text = ""
                if "search_results_list" in search_screen.ids:
                    search_screen.ids.search_results_list.data = []
                app.load_search_history_from_db()
        except Exception:
            pass

    def on_search_text_change(self, text: str) -> None:
        app = self.app
        query = (text or "").strip()
        if not query:
            if app.search_state != "empty":
                app.search_state = "empty"
            return
        if app.search_state == "results":
            app.search_state = "suggestions"

        if app.search_state != "results":
            app.search_state = "suggestions"
            q_lower = query.lower()
            matches = []
            try:
                get_hist = resolve_symbol("get_search_history", db_mod.get_search_history)
                for h in get_hist(limit=15):
                    if q_lower in h.lower() and h not in matches:
                        matches.append(h)
            except Exception:
                pass
            for t in getattr(app.playlist_model, "tracks", []):
                t_title = t.title or ""
                t_artist = t.artist or ""
                if q_lower in t_title.lower() and t_title not in matches:
                    matches.append(t_title)
                if q_lower in t_artist.lower() and t_artist not in matches:
                    matches.append(t_artist)
                if len(matches) >= 8:
                    break
            try:
                if hasattr(app, "root") and app.root:
                    search_screen = app.root.ids.screen_manager.get_screen("search")
                    if "search_suggestions_list" in search_screen.ids:
                        search_screen.ids.search_suggestions_list.data = [{"text": m, "query": m} for m in matches[:8]]
            except Exception:
                pass

    def perform_search(self, query: str) -> None:
        app = self.app
        if not query or not str(query).strip():
            return
        q = str(query).strip()
        app.search_state = "results"
        app.search_loading = True
        db_mod.add_search_history_async(q)
        try:
            search_screen = app.root.ids.screen_manager.get_screen("search")
            if "search_input" in search_screen.ids:
                search_screen.ids.search_input.text = q
            if "search_history_list" in search_screen.ids:
                rv = search_screen.ids.search_history_list
                if q.lower() not in [item["text"].lower() for item in rv.data]:
                    rv.data.insert(0, {"text": q})
        except Exception:
            pass

        if "open.spotify.com/" in q or q.startswith("spotify:"):
            try:
                search_screen = app.root.ids.screen_manager.get_screen("search")
                if "search_status_label" in search_screen.ids:
                    search_screen.ids.search_status_label.text = "Extracting Spotify metadata & tracks..."
            except Exception:
                pass
            app_logger.info(f"[THREAD START] MusicApp._async_spotify_extractor for URL: {q}")
            threading.Thread(target=app._async_spotify_extractor, args=(q,), daemon=True).start()
            return

        if "youtube.com/" in q or "youtu.be/" in q or (len(q) == 11 and " " not in q and q.isalnum()):
            try:
                search_screen = app.root.ids.screen_manager.get_screen("search")
                if "search_status_label" in search_screen.ids:
                    search_screen.ids.search_status_label.text = "Extracting video metadata..."
            except Exception:
                pass
            app_logger.info(f"[THREAD START] MusicApp._async_url_extractor for URL: {q}")
            threading.Thread(target=app._async_url_extractor, args=(q,), daemon=True).start()
            return

        local_matches = [
            t for t in app.playlist_model.tracks
            if q.lower() in t.title.lower() or q.lower() in t.artist.lower()
        ]
        try:
            search_screen = app.root.ids.screen_manager.get_screen("search")
            if local_matches:
                if "search_status_label" in search_screen.ids:
                    search_screen.ids.search_status_label.text = f"Local matches ({len(local_matches)})... Searching online..."
                if "search_results_list" in search_screen.ids:
                    search_screen.ids.search_results_list.data = [
                        {
                            "title": t.title,
                            "artist": f"{t.artist} • {t.formatted_duration}",
                            "artwork": t.album_art,
                            "source_icon": "headphones" if getattr(t, "source", "") == "jiosaavn" else ("spotify" if getattr(t, "source", "") == "spotify" else "youtube"),
                            "source_icon_color": [0.11, 0.72, 0.33, 1.0] if getattr(t, "source", "") == "spotify" else ([0.90, 0.22, 0.21, 1.0] if getattr(t, "source", "") == "youtube" else [0.35, 0.45, 0.90, 1.0]),
                            "track_obj": t,
                        }
                        for t in local_matches
                    ]
            elif "search_status_label" in search_screen.ids:
                search_screen.ids.search_status_label.text = f"Searching online for '{q}'..."
            if "search_scroll" in search_screen.ids:
                search_screen.ids.search_scroll.scroll_y = 1.0
        except Exception:
            pass

        app_logger.info(f"[THREAD START] MusicApp._async_yt_search for: {q}")
        threading.Thread(target=app._async_yt_search, args=(q,), daemon=True).start()

    def async_url_extractor(self, url: str) -> None:
        app = self.app
        try:
            video_id = media_utils.extract_video_id(url)
            full_url = url if ("youtube.com" in url or "youtu.be" in url) else f"https://www.youtube.com/watch?v={video_id}"
            yt_meta = resolve_symbol("fetch_youtube_metadata", media_utils.fetch_youtube_metadata)
            info = yt_meta(full_url)
            meta = media_utils.parse_complete_media_metadata(info)
            if not meta or not meta.get("video_id"):
                meta = {
                    "video_id": video_id,
                    "title": info.get("title", "Unknown Title"),
                    "artist": info.get("uploader") or info.get("channel") or "Unknown Artist",
                    "url": full_url,
                    "duration": int(info.get("duration", 0) or 0),
                    "media_type": "podcast" if media_utils.is_podcast_item(info) else "song",
                }
            thumb = media_utils.get_thumbnail_path(video_id)
            meta["artwork"] = thumb or meta.get("artwork", "")

            db_mod.add_track(
                video_id=meta["video_id"],
                title=meta["title"],
                artist=meta["artist"],
                url=meta["url"],
                duration=meta["duration"],
                artwork=meta["artwork"],
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
                media_type=meta.get("media_type", "song"),
            )
            app_logger.info(f"[THREAD SUCCESS] _async_url_extractor completed for {video_id}: {meta['title']}")
            Clock.schedule_once(lambda dt: app._on_url_extracted(meta), 0)
        except Exception as e:
            app_logger.error(f"[THREAD FAILED] _async_url_extractor error: {e}")
            Clock.schedule_once(lambda dt: app._on_search_error(f"Link extraction failed: {e}"), 0)

    def on_url_extracted(self, meta: dict) -> None:
        app = self.app
        is_pod = (meta.get("media_type") == "podcast")
        track_obj = TrackModel.from_dict(meta)
        if not is_pod:
            app.playlist_model.load_from_db()
            app.player_controller.rebuild_queue()
            existing = app.playlist_model.find_track(meta["video_id"])
            if existing:
                track_obj = existing
            else:
                app.playlist_model.add_track(track_obj)
        else:
            db_mod.add_playlist("Podcasts")
            db_mod.add_track_to_playlist("Podcasts", meta["video_id"])

        try:
            search_screen = app.root.ids.screen_manager.get_screen("search")
            if "search_status_label" in search_screen.ids:
                search_screen.ids.search_status_label.text = f"Ready: {track_obj.title}"
            if "search_results_list" in search_screen.ids:
                search_screen.ids.search_results_list.data = [
                    {
                        "title": track_obj.title,
                        "artist": f"{track_obj.artist} • {track_obj.formatted_duration}",
                        "artwork": track_obj.album_art,
                        "source_icon": "youtube",
                        "source_icon_color": [0.90, 0.22, 0.21, 1.0],
                        "track_obj": track_obj,
                    }
                ]
        except Exception:
            pass

        media_utils.download_artwork(
            track_obj.video_id,
            custom_url=track_obj.album_art,
            on_success=lambda p: app.on_artwork_downloaded(track_obj, p),
        )
        if not is_pod:
            app.populate_home_screen_data()
        app.play_selected_track(track_obj)

    def async_spotify_extractor(self, url: str) -> None:
        app = self.app
        try:
            from services.music_provider_router import MusicProviderRouter

            router = MusicProviderRouter()
            if "/track/" in url or "spotify:track:" in url:
                td = router.spotify.get_track_details(url)
                if td:
                    Clock.schedule_once(lambda dt: app._on_search_results([td], "Spotify Track"), 0)
                    Clock.schedule_once(lambda dt: app.show_toast(f"Found: {td['title']}"), 0)
                else:
                    Clock.schedule_once(lambda dt: app.show_toast("Could not resolve Spotify track"), 0)
            else:
                res = router.import_spotify_playlist(url)
                if res.get("success"):
                    title, count = res.get("title"), res.get("count")
                    Clock.schedule_once(lambda dt: app.show_toast(f"Imported '{title}' ({count} tracks)!"), 0)
                    Clock.schedule_once(lambda dt: app.playlist_model.load_from_db(), 0)
                    Clock.schedule_once(lambda dt: app.populate_home_screen_data(), 0)
                    Clock.schedule_once(lambda dt: app._on_search_results(res.get("tracks", []), title), 0)
                else:
                    Clock.schedule_once(lambda dt: app.show_toast(f"Spotify: {res.get('error')}"), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: app._on_search_error(f"Spotify extraction error: {e}"), 0)

    def async_yt_search(self, query: str) -> None:
        app = self.app
        try:
            from services.music_provider_router import MusicProviderRouter

            provider_filter = getattr(app, "active_search_provider", "all")
            entries = MusicProviderRouter().search(query, provider=provider_filter, limit=16)
            app_logger.info(f"[THREAD SUCCESS] MusicApp._async_yt_search for '{query}' -> {len(entries)} items")
            Clock.schedule_once(lambda dt: app._on_search_results(entries, query), 0)
        except Exception as e:
            app_logger.error(f"[THREAD FAILED] MusicApp._async_yt_search error for '{query}': {e}")
            Clock.schedule_once(lambda dt: app._on_search_error(str(e)), 0)

    def on_search_results(self, entries: list, query: str) -> None:
        app = self.app
        app.search_loading = False
        try:
            search_screen = app.root.ids.screen_manager.get_screen("search")
            if "search_status_label" in search_screen.ids:
                search_screen.ids.search_status_label.text = f"Results for '{query}' ({len(entries)})"

            rv_data = []
            for entry in entries:
                vid = entry.get("video_id") or entry.get("id", "")
                title = entry.get("title", "Unknown Title")
                artist = entry.get("artist") or entry.get("uploader") or entry.get("channel") or "Unknown Artist"
                thumb = entry.get("artwork") or (media_utils.get_thumbnail_path(vid) if vid else "album_art.png")
                source = entry.get("source", "youtube")

                track_obj = TrackModel.from_dict(entry)
                if not track_obj.album_art:
                    track_obj.album_art = thumb

                if track_obj.media_type == "podcast":
                    badge_str = f"Podcast • {artist} • {track_obj.formatted_duration}"
                    src_icon = "podcast"
                    src_color = [0.62, 0.38, 0.92, 1.0]
                elif source == "jiosaavn":
                    badge_str = f"320kbps HD • {artist} • {track_obj.formatted_duration}"
                    src_icon = "high-definition-box"
                    src_color = [0.15, 0.65, 0.58, 1.0]
                elif source == "spotify":
                    badge_str = f"Spotify • {artist} • {track_obj.formatted_duration}"
                    src_icon = "spotify"
                    src_color = [0.11, 0.72, 0.33, 1.0]
                else:
                    badge_str = f"YouTube • {artist} • {track_obj.formatted_duration}"
                    src_icon = "youtube"
                    src_color = [0.90, 0.22, 0.21, 1.0]

                rv_data.append({
                    "title": title,
                    "artist": badge_str,
                    "artwork": track_obj.album_art,
                    "source_icon": src_icon,
                    "source_icon_color": src_color,
                    "track_obj": track_obj,
                })

            if "search_results_list" in search_screen.ids:
                search_screen.ids.search_results_list.data = rv_data

            ensure_dl = resolve_symbol("ensure_artworks_downloaded", media_utils.ensure_artworks_downloaded)
            ensure_dl([item["track_obj"] for item in rv_data], on_track_updated=app.on_search_artwork_downloaded)
        except Exception as e:
            app_logger.error("Error rendering search results: %s", e)

    def on_search_artwork_downloaded(self, track, art_path: str) -> None:
        app = self.app
        track.album_art = art_path
        if hasattr(app, "root") and app.root:
            try:
                search_screen = app.root.ids.screen_manager.get_screen("search")
                if "search_results_list" in search_screen.ids:
                    rv = search_screen.ids.search_results_list
                    for item in rv.data:
                        if item.get("track_obj") == track:
                            item["artwork"] = art_path
                    rv.refresh_from_data()
            except Exception:
                pass

    def on_search_error(self, err_msg: str) -> None:
        app = self.app
        app.search_loading = False
        try:
            search_screen = app.root.ids.screen_manager.get_screen("search")
            if "search_status_label" in search_screen.ids:
                search_screen.ids.search_status_label.text = f"Search error ({err_msg[:30]})"
        except Exception:
            pass
