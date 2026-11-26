"""Playlists, Track Options Sheet, Offline Download & Spotify Import Coordinator."""

from __future__ import annotations

import os
import re
import threading
from typing import Any

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.uix.bottomsheet import (
    MDBottomSheet,
    MDBottomSheetDragHandle,
    MDBottomSheetDragHandleButton,
    MDBottomSheetDragHandleTitle,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogHeadlineText,
    MDDialogSupportingText,
)
from kivymd.uix.divider import MDDivider
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
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
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText

from app_core.service_container import resolve_symbol
from models.database import (
    add_playlist,
    add_track,
    add_track_to_playlist,
    delete_playlist,
    get_all_playlists,
    get_all_tracks,
    get_dynamic_playlist_tracks,
    get_playlist_tracks,
    update_local_track_path,
)
from models.track_model import TrackModel
from services.logger import app_logger
from utils import media_utils


class PlaylistOptionsCoordinator:
    """Coordinates playlist screens, track context bottom sheets, offline download & Spotify import."""

    def __init__(self, app: Any):
        self.app = app

    def show_add_playlist_dialog(self, track_to_add=None) -> None:
        app = self.app
        text_field = MDTextField(MDTextFieldHintText(text="Playlist name..."), mode="filled")

        def on_create(*args):
            name = text_field.text.strip() or f"My Playlist #{len(get_all_playlists()) + 1}"
            add_playlist(name)
            if track_to_add:
                vid = getattr(track_to_add, "video_id", "")
                if vid:
                    add_track_to_playlist(
                        name,
                        vid,
                        {
                            "title": track_to_add.title,
                            "artist": track_to_add.artist,
                            "url": track_to_add.url,
                            "artwork": track_to_add.album_art,
                            "duration": track_to_add.duration,
                            "local_path": track_to_add.local_path,
                        },
                    )
            if hasattr(app, "playlist_dialog") and app.playlist_dialog:
                app.playlist_dialog.dismiss()
            app.show_toast(f"Playlist '{name}' created!")
            app.open_playlist(name)

        app.playlist_dialog = MDDialog(
            MDDialogHeadlineText(text="New Playlist"),
            MDDialogSupportingText(text="Enter a name for your new playlist:"),
            MDDialogContentContainer(text_field, orientation="vertical"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: app.playlist_dialog.dismiss()),
                MDButton(MDButtonText(text="CREATE"), style="text", on_release=on_create),
            ),
        )
        app.playlist_dialog.open()

    def show_import_spotify_dialog(self) -> None:
        app = self.app
        text_field = MDTextField(MDTextFieldHintText(text="Paste Spotify Playlist URL..."), mode="filled")

        def on_import(*args):
            url = text_field.text.strip()
            if app._active_spotify_dialog:
                app._active_spotify_dialog.dismiss()
            if url:
                app.import_spotify_playlist(url)

        app._active_spotify_dialog = MDDialog(
            MDDialogHeadlineText(text="Import Spotify Playlist"),
            MDDialogSupportingText(text="Paste any public Spotify playlist or album URL. All tracks will be extracted and saved to your library:"),
            MDDialogContentContainer(text_field, orientation="vertical", spacing="8dp"),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="CANCEL"),
                    style="text",
                    on_release=lambda *a: app._active_spotify_dialog.dismiss() if app._active_spotify_dialog else None,
                ),
                MDButton(MDButtonText(text="IMPORT"), style="text", on_release=on_import),
                spacing="8dp",
            ),
        )
        app._active_spotify_dialog.open()

    def import_spotify_playlist(self, url: str) -> None:
        app = self.app
        app.show_toast("Connecting to Spotify & extracting tracks...")

        def _bg():
            try:
                from services.music_provider_router import MusicProviderRouter

                res = MusicProviderRouter().import_spotify_playlist(url)
                if res.get("success"):
                    title = res.get("title")
                    count = res.get("count")
                    Clock.schedule_once(lambda dt: app.show_toast(f"Imported '{title}' ({count} tracks)!"), 0)
                    Clock.schedule_once(lambda dt: app.playlist_model.load_from_db(), 0)
                    Clock.schedule_once(lambda dt: app.populate_home_screen_data(), 0)
                    Clock.schedule_once(lambda dt: app.open_playlist(title), 0)
                else:
                    err = res.get("error", "Failed to import playlist")
                    Clock.schedule_once(lambda dt: app.show_toast(f"Spotify error: {err}"), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: app.show_toast(f"Import error: {e}"), 0)

        threading.Thread(target=_bg, daemon=True).start()

    def open_playlist(self, playlist_name: str) -> None:
        app = self.app
        app.active_playlist_name = playlist_name
        app.switch_screen("playlist")
        app.sync_active_playlist_screen()
        curated_dynamic_categories = [
            "Top Charts", "Community Picks", "Radio Stations", "Trending Hits",
            "Global Top 50", "YouTube Global Top 50", "Viral Hits Today",
            "Chillwave", "Workout", "Late Night",
        ]
        if (not getattr(app, "active_playlist_tracks", []) or len(app.active_playlist_tracks) < 5) and playlist_name in curated_dynamic_categories:
            app._fetch_playlist_tracks_async(playlist_name)

    def fetch_playlist_tracks_async(self, playlist_name: str) -> None:
        app = self.app
        yt_meta = resolve_symbol("fetch_youtube_metadata", media_utils.fetch_youtube_metadata)

        def _bg():
            try:
                is_podcast_pl = (playlist_name.lower() == "podcasts")
                search_query = f"ytsearch25:{playlist_name} official hits music audio"
                if is_podcast_pl:
                    search_query = "ytsearch15:popular podcast full episode audio"
                elif playlist_name in ("Top Charts", "Global Top 50", "YouTube Global Top 50"):
                    search_query = "ytsearch25:billboard global top 50 official music audio"
                elif playlist_name in ("Viral Hits Today", "Trending Hits"):
                    search_query = "ytsearch25:viral hits today trending songs official audio"
                elif playlist_name == "Chillwave":
                    search_query = "ytsearch25:chillwave lofi beats relaxing study audio"
                elif playlist_name == "Workout":
                    search_query = "ytsearch25:workout gym motivation high energy music audio"
                elif playlist_name == "Late Night":
                    search_query = "ytsearch25:late night drive slow chill aesthetic songs audio"
                elif playlist_name == "Radio Stations":
                    search_query = "ytsearch25:radio hits non stop official audio"
                elif playlist_name == "Community Picks":
                    search_query = "ytsearch25:community favorites viral music hits audio"

                info = yt_meta(search_query, extract_flat=True)
                entries = info.get("entries", []) if info else []
                add_playlist(playlist_name)
                for entry in entries:
                    if not entry:
                        continue
                    meta = media_utils.parse_complete_media_metadata(entry)
                    if not meta or not meta.get("video_id"):
                        continue
                    vid = meta["video_id"]
                    is_pod = (meta.get("media_type") == "podcast" or media_utils.is_podcast_item(entry))
                    if is_podcast_pl:
                        if not is_pod:
                            continue
                        target_media_type = "podcast"
                    else:
                        if is_pod:
                            continue
                        target_media_type = "song"

                    thumb = media_utils.get_thumbnail_path(vid)
                    add_track(
                        video_id=vid,
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
                        media_type=target_media_type,
                    )
                    add_track_to_playlist(playlist_name, vid)
                Clock.schedule_once(lambda dt: app.sync_active_playlist_screen(), 0)
            except Exception as e:
                app_logger.error(f"[_fetch_playlist_tracks_async error]: {e}")

        threading.Thread(target=_bg, daemon=True).start()

    def sync_active_playlist_screen(self) -> None:
        app = self.app
        if not hasattr(app, "root") or not app.root:
            return
        try:
            pl_screen = app.root.ids.screen_manager.get_screen("playlist")
            get_pl = resolve_symbol("get_playlist_tracks", get_playlist_tracks)
            get_all = resolve_symbol("get_all_tracks", get_all_tracks)
            ensure_dl = resolve_symbol("ensure_artworks_downloaded", media_utils.ensure_artworks_downloaded)

            raw_tracks = get_dynamic_playlist_tracks(app.active_playlist_name)
            if not raw_tracks:
                raw_tracks = get_pl(app.active_playlist_name)
            if not raw_tracks and app.active_playlist_name in ("Your Daily Mix", "On Repeat", "Heavy Rotation", "Forgotten Favorites"):
                raw_tracks = get_all()[:20]

            is_podcast_playlist = (app.active_playlist_name.lower() == "podcasts")
            track_objs = []
            for r in raw_tracks:
                is_pod = (r.get("media_type") == "podcast" or media_utils.is_podcast_item(r))
                if is_podcast_playlist and not is_pod:
                    continue
                if not is_podcast_playlist and is_pod:
                    continue
                existing = app.playlist_model.get_track_by_video_id(r["video_id"])
                if existing:
                    if is_podcast_playlist or (existing.media_type != "podcast" and not media_utils.is_podcast_item(existing.to_dict())):
                        track_objs.append(existing)
                else:
                    new_t = TrackModel.from_dict(r)
                    if not is_podcast_playlist:
                        app.playlist_model.add_track(new_t)
                    track_objs.append(new_t)

            app.active_playlist_tracks = track_objs
            app.active_playlist_info = f"{len(track_objs)} tracks"
            app.active_playlist_artwork = track_objs[0].album_art if (track_objs and track_objs[0].album_art) else "album_art2.png"

            if "playlist_tracks_list" in pl_screen.ids:
                all_data = [
                    {"title": t.title, "artist": t.artist, "artwork": t.album_art, "track_obj": t}
                    for t in track_objs
                ]
                pl_screen.ids.playlist_tracks_list.data = all_data[:25]
                if len(all_data) > 25:
                    def _load_more_chunks(dt, current_count=25):
                        if not hasattr(app, "root") or not app.root:
                            return
                        if not pl_screen or "playlist_tracks_list" not in pl_screen.ids:
                            return
                        nxt = min(len(all_data), current_count + 30)
                        pl_screen.ids.playlist_tracks_list.data = all_data[:nxt]
                        if nxt < len(all_data):
                            Clock.schedule_once(lambda _dt: _load_more_chunks(_dt, nxt), 0.016)

                    Clock.schedule_once(lambda _dt: _load_more_chunks(_dt, 25), 0.016)

            if track_objs:
                ensure_dl(track_objs[:30], on_track_updated=app.on_artwork_downloaded, cache_dir=app.cache_dir)
        except Exception as e:
            app_logger.error("open_playlist error: %s", e)

    def play_active_playlist(self, shuffle: bool = False) -> None:
        app = self.app
        if not getattr(app, "active_playlist_tracks", None):
            app.show_toast("Playlist has no tracks to play.")
            return
        tracks = list(app.active_playlist_tracks)
        if shuffle:
            import random
            random.shuffle(tracks)
        first = tracks[0]
        app.player_controller.set_custom_queue(tracks, start_track=first)
        app.play_selected_track(first)

    def download_active_playlist(self, playlist_name=None) -> None:
        app = self.app
        pl_name = playlist_name or app.active_playlist_name
        tracks = get_playlist_tracks(pl_name) if pl_name else []
        if not tracks:
            app.show_toast("No tracks to download.")
            return
        to_download = []
        for r in tracks:
            t = app.playlist_model.get_track_by_video_id(r["video_id"]) or TrackModel.from_dict(r)
            if not t.is_downloaded and not (t.local_path and os.path.exists(t.local_path)):
                to_download.append(t)
        if not to_download:
            app.show_toast(f"All tracks in '{pl_name}' are already downloaded!")
            return
        app.show_toast(f"Queued {len(to_download)} tracks for offline download...")
        for t in to_download:
            app.download_track_offline(t)

    def show_playlists_overview(self) -> None:
        app = self.app
        playlists = get_all_playlists()
        sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text="Your Playlists"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: sheet.set_state("close")),
            ),
            size_hint_y=None,
            height="420dp",
            opening_time=0.2,
            closing_time=0.15,
        )
        scroll = MDScrollView(size_hint_y=None, height="350dp")
        dlist = MDList()
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="playlist-plus"),
                MDListItemHeadlineText(text="Create New Playlist"),
                MDListItemSupportingText(text="Tap to create custom playlist"),
                on_release=lambda x: (sheet.set_state("close"), app.show_add_playlist_dialog()),
            )
        )
        for p in playlists:
            def on_sel(inst, pl_name=p["name"]):
                sheet.set_state("close")
                app.open_playlist(pl_name)

            dlist.add_widget(
                MDListItem(
                    MDListItemLeadingIcon(icon="playlist-music"),
                    MDListItemHeadlineText(text=p["name"]),
                    MDListItemSupportingText(text=f"{p.get('track_count', 0)} tracks"),
                    MDListItemTrailingIcon(icon="chevron-right"),
                    on_release=on_sel,
                )
            )
        scroll.add_widget(dlist)
        sheet.add_widget(scroll)
        Window.add_widget(sheet)
        sheet.width = Window.width
        sheet.x = 0
        sheet.set_state("open")

    def show_add_to_active_playlist_sheet(self) -> None:
        app = self.app
        if not app.active_playlist_name:
            return
        if app.active_playlist_name == "Offline Songs":
            app.show_local_audio_options()
            return

        current_vids = {t.video_id for t in getattr(app, "active_playlist_tracks", [])}
        available_tracks = [t for t in app.playlist_model.tracks if t.video_id not in current_vids]
        if not available_tracks:
            app.show_toast("All library songs are already in this playlist!")
            return

        sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text=f"Add Songs to '{app.active_playlist_name}'"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: sheet.set_state("close")),
            ),
            size_hint_y=None,
            height="400dp",
            opening_time=0.2,
            closing_time=0.15,
        )
        sheet.bind(on_touch_down=lambda inst, touch: True if inst.collide_point(*touch.pos) else False)
        scroll = MDScrollView(size_hint_y=None, height="330dp")
        dlist = MDList()
        scroll.add_widget(dlist)
        sheet.add_widget(scroll)

        Window.add_widget(sheet)
        sheet.width = Window.width
        sheet.x = 0
        sheet.set_state("open")

        def build_track_widget(t):
            def on_add(inst):
                add_track_to_playlist(
                    app.active_playlist_name,
                    t.video_id,
                    {
                        "title": t.title,
                        "artist": t.artist,
                        "url": t.url,
                        "artwork": t.album_art,
                        "duration": t.duration,
                        "local_path": t.local_path,
                    },
                )
                app.show_toast(f"Added '{t.title}' to {app.active_playlist_name}")
                app.sync_active_playlist_screen()
                sheet.set_state("close")

            art_source = t.album_art if (t.album_art and os.path.exists(t.album_art)) else "album_art.png"
            return MDListItem(
                MDListItemLeadingAvatar(source=art_source, radius=[dp(8)] * 4),
                MDListItemHeadlineText(text=t.title),
                MDListItemSupportingText(text=t.artist),
                MDListItemTrailingIcon(icon="plus"),
                on_release=on_add,
            )

        batch_size = 12
        for track in available_tracks[:batch_size]:
            dlist.add_widget(build_track_widget(track))

        def add_remaining_chunks(start_idx):
            if start_idx >= len(available_tracks):
                return
            end_idx = min(start_idx + batch_size, len(available_tracks))
            for tr in available_tracks[start_idx:end_idx]:
                dlist.add_widget(build_track_widget(tr))
            if end_idx < len(available_tracks):
                Clock.schedule_once(lambda dt: add_remaining_chunks(end_idx), 0.02)

        if len(available_tracks) > batch_size:
            Clock.schedule_once(lambda dt: add_remaining_chunks(batch_size), 0.02)

    def show_playlist_options(self) -> None:
        app = self.app
        sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text=f"Options: {app.active_playlist_name}"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: sheet.set_state("close")),
            ),
            size_hint_y=None,
            height="260dp",
            opening_time=0.2,
            closing_time=0.15,
        )
        dlist = MDList()
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="download"),
                MDListItemHeadlineText(text="Download All for Offline"),
                on_release=lambda x: (sheet.set_state("close"), app.download_active_playlist()),
            )
        )
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="plus"),
                MDListItemHeadlineText(text="Add Songs to Playlist"),
                on_release=lambda x: (sheet.set_state("close"), app.show_add_to_active_playlist_sheet()),
            )
        )
        if app.active_playlist_name != "Favorites":
            def on_del(x):
                sheet.set_state("close")
                delete_playlist(app.active_playlist_name)
                app.show_toast(f"Deleted playlist '{app.active_playlist_name}'")
                app.go_back()

            dlist.add_widget(
                MDListItem(
                    MDListItemLeadingIcon(icon="delete"),
                    MDListItemHeadlineText(text="Delete Playlist"),
                    on_release=on_del,
                )
            )
        sheet.add_widget(dlist)
        Window.add_widget(sheet)
        sheet.width = Window.width
        sheet.x = 0
        sheet.set_state("open")
        app.bottom_sheet = sheet

        def _cleanup_sheet(*args):
            if sheet.state == "close" and sheet in Window.children:
                Window.remove_widget(sheet)

        sheet.bind(on_close=lambda *a: Clock.schedule_once(_cleanup_sheet, 0.2))

    def show_add_to_playlist_sheet(self, track=None) -> None:
        app = self.app
        target_track = track or app.player_controller.active_track
        if not target_track:
            return
        playlists = get_all_playlists()
        sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text="Add to Playlist"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: sheet.set_state("close")),
            ),
            size_hint_y=None,
            height="380dp",
            opening_time=0.2,
            closing_time=0.15,
        )
        scroll = MDScrollView(size_hint_y=None, height="310dp")
        dlist = MDList()
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="playlist-plus"),
                MDListItemHeadlineText(text="Create New Playlist"),
                on_release=lambda x: (sheet.set_state("close"), app.show_add_playlist_dialog(track_to_add=target_track)),
            )
        )
        for p in playlists:
            def on_sel(inst, pl_name=p["name"]):
                sheet.set_state("close")
                add_track_to_playlist(
                    pl_name,
                    target_track.video_id,
                    {
                        "title": target_track.title,
                        "artist": target_track.artist,
                        "url": target_track.url,
                        "artwork": target_track.album_art,
                        "duration": target_track.duration,
                        "local_path": target_track.local_path,
                    },
                )
                app.show_toast(f"Added '{target_track.title}' to '{pl_name}'")

            dlist.add_widget(
                MDListItem(
                    MDListItemLeadingIcon(icon="playlist-music"),
                    MDListItemHeadlineText(text=p["name"]),
                    MDListItemSupportingText(text=f"{p.get('track_count', 0)} tracks"),
                    on_release=on_sel,
                )
            )
        scroll.add_widget(dlist)
        sheet.add_widget(scroll)
        Window.add_widget(sheet)
        sheet.width = Window.width
        sheet.x = 0
        sheet.set_state("open")

    def download_track_offline(self, track) -> None:
        app = self.app
        if not track:
            return
        if track.is_downloaded or (track.local_path and os.path.exists(track.local_path)):
            app.show_toast(f"'{track.title}' is already downloaded for offline listening.")
            return

        track.is_loading = True
        track.download_progress = "0%"
        app.show_toast(f"Downloading '{track.title}' for offline...")

        def _worker():
            from services.youtube_extractor import YtdlpLogBridge, get_youtube_extractor, redact_sensitive_text

            try:
                from yt_dlp import YoutubeDL

                cache_dir = app.cache_dir
                media_utils.download_artwork(track.video_id, custom_url=track.album_art, cache_dir=cache_dir)
                target = track.url or f"https://www.youtube.com/watch?v={track.video_id}"
                out_tmpl = os.path.join(cache_dir, f"{track.video_id}.%(ext)s")
                mp3_path = os.path.join(cache_dir, f"{track.video_id}.mp3")

                def hook(d):
                    if d.get("status") == "downloading":
                        raw_p = d.get("_percent_str", "")
                        clean_p = re.sub(r"\x1b\[[0-9;]*m", "", raw_p).strip()
                        if clean_p:
                            Clock.schedule_once(lambda dt: setattr(track, "download_progress", clean_p), 0)

                ydl_opts = get_youtube_extractor().build_ydl_opts(
                    video_id=track.video_id,
                    for_download=True,
                    log_bridge=YtdlpLogBridge(app_logger),
                    extra_opts={
                        "format": "bestaudio/best",
                        "outtmpl": out_tmpl,
                        "continuedl": True,
                        "progress_hooks": [hook],
                        "postprocessors": [{
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }],
                    },
                )
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([target])

                if os.path.exists(mp3_path):
                    track.local_path = mp3_path
                    track.is_downloaded = True
                    try:
                        update_local_track_path(track.video_id, mp3_path, track.duration)
                    except Exception:
                        pass
                    Clock.schedule_once(lambda dt: app._on_download_finished(track, True), 0)
                else:
                    Clock.schedule_once(lambda dt: app._on_download_finished(track, False), 0)
            except Exception as e:
                app_logger.error("Offline Download Error: %s", redact_sensitive_text(e))
                Clock.schedule_once(lambda dt: app._on_download_finished(track, False), 0)

        threading.Thread(target=_worker, daemon=True).start()

    def on_download_finished(self, track, success: bool) -> None:
        track.is_loading = False
        track.download_progress = ""
        if success:
            self.app.show_toast(f"Downloaded '{track.title}' for offline listening!")
        else:
            self.app.show_toast(f"Download completed for '{track.title}'")

    def show_track_options(self) -> None:
        app = self.app
        active_t = app.player_controller.active_track
        if not active_t:
            return

        sheet_h = min(Window.height * 0.78, dp(540))
        sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text="Track Options"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: sheet.set_state("close")),
            ),
            size_hint_y=None,
            height=sheet_h,
            opening_time=0.2,
            closing_time=0.15,
        )

        content_box = MDBoxLayout(orientation="vertical", size_hint_y=1, spacing=dp(4))
        header_card = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(56),
            padding=[dp(16), dp(4), dp(16), dp(4)],
            spacing=dp(12),
        )
        art_img = FitImage(
            source=active_t.album_art if (active_t.album_art and os.path.exists(active_t.album_art)) else "album_art.png",
            size_hint=(None, None),
            size=(dp(44), dp(44)),
            radius=[dp(8)],
            mipmap=True,
            pos_hint={"center_y": 0.5},
        )
        meta_col = MDBoxLayout(orientation="vertical", size_hint_x=1, pos_hint={"center_y": 0.5}, spacing=dp(1))
        meta_col.add_widget(
            MDLabel(
                text=active_t.title,
                font_style="Title",
                role="small",
                bold=True,
                adaptive_height=True,
                max_lines=1,
                theme_text_color="Custom",
                text_color=app.theme_cls.onSurfaceColor,
            )
        )
        meta_col.add_widget(
            MDLabel(
                text=active_t.artist or "Unknown Artist",
                font_style="Body",
                role="small",
                adaptive_height=True,
                max_lines=1,
                theme_text_color="Custom",
                text_color=app.theme_cls.onSurfaceVariantColor,
            )
        )
        header_card.add_widget(art_img)
        header_card.add_widget(meta_col)
        content_box.add_widget(header_card)
        content_box.add_widget(MDDivider())

        sv = MDScrollView(do_scroll_x=False, do_scroll_y=True, size_hint=(1, 1))
        dlist = MDList()

        def _close_and(fn):
            return lambda x: (sheet.set_state("close"), fn())

        def _play_next():
            pc = app.player_controller
            if pc:
                if active_t in pc.queue:
                    pc.queue.remove(active_t)
                pc.queue.insert(pc.current_index + 1, active_t)
                app.show_toast(f"'{active_t.title}' will play next")

        def _add_to_queue():
            pc = app.player_controller
            if pc:
                if active_t not in pc.queue:
                    pc.queue.append(active_t)
                app.show_toast(f"Added '{active_t.title}' to queue")

        def _start_radio():
            app.show_toast(f"Starting radio from '{active_t.title}'...")
            app.play_home_quick_picks()

        is_fav = bool(app.player_controller.is_favorite)
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(
                    icon="heart" if is_fav else "heart-outline",
                    theme_icon_color="Custom",
                    icon_color=get_color_from_hex("#FF4081") if is_fav else app.theme_cls.onSurfaceColor,
                ),
                MDListItemHeadlineText(text="Remove from Favorites" if is_fav else "Add to Favorites"),
                on_release=_close_and(lambda: app.player_controller.toggle_favorite()),
            )
        )
        is_down = bool(active_t.is_downloaded)
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="check-circle" if is_down else "download"),
                MDListItemHeadlineText(text="Downloaded Offline" if is_down else "Download for Offline"),
                on_release=_close_and(lambda: app.download_track_offline(active_t)),
            )
        )
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="playlist-plus"),
                MDListItemHeadlineText(text="Add to Playlist"),
                on_release=_close_and(lambda: app.show_add_to_playlist_sheet(active_t)),
            )
        )
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="play-circle-outline"),
                MDListItemHeadlineText(text="Play Next"),
                on_release=_close_and(_play_next),
            )
        )
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="playlist-play"),
                MDListItemHeadlineText(text="Add to Queue"),
                on_release=_close_and(_add_to_queue),
            )
        )
        if active_t.artist and active_t.artist != "Unknown Artist":
            dlist.add_widget(
                MDListItem(
                    MDListItemLeadingIcon(icon="account-music-outline"),
                    MDListItemHeadlineText(text=f"View Artist ({active_t.artist})"),
                    on_release=_close_and(lambda: app.open_artist(active_t.artist)),
                )
            )
        album_title = active_t.album or "Album"
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="album"),
                MDListItemHeadlineText(text=f"View Album ({album_title})"),
                on_release=_close_and(lambda: app.open_album(album_title, active_t.artist, active_t.album_art)),
            )
        )
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="radio-tower"),
                MDListItemHeadlineText(text="Start Radio"),
                on_release=_close_and(_start_radio),
            )
        )
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="text-box-outline"),
                MDListItemHeadlineText(text="View Lyrics"),
                on_release=_close_and(lambda: app.show_lyrics()),
            )
        )
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="timer-outline"),
                MDListItemHeadlineText(text="Sleep Timer"),
                on_release=_close_and(lambda: app.show_sleep_timer_dialog()),
            )
        )
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="tune"),
                MDListItemHeadlineText(text="Equalizer"),
                on_release=_close_and(lambda: app.switch_screen("equalizer")),
            )
        )
        share_url = active_t.url or (f"https://youtube.com/watch?v={active_t.video_id}" if active_t.video_id else "")
        dlist.add_widget(
            MDListItem(
                MDListItemLeadingIcon(icon="share-variant"),
                MDListItemHeadlineText(text="Share"),
                on_release=_close_and(lambda: app.show_toast(f"Share link: {share_url}")),
            )
        )

        sv.add_widget(dlist)
        content_box.add_widget(sv)
        sheet.add_widget(content_box)

        Window.add_widget(sheet)
        sheet.width = Window.width
        sheet.x = 0
        sheet.set_state("open")
        app.bottom_sheet = sheet

        def _cleanup_sheet(*args):
            if sheet.state == "close" and sheet in Window.children:
                Window.remove_widget(sheet)

        sheet.bind(on_close=lambda *a: Clock.schedule_once(_cleanup_sheet, 0.2))
