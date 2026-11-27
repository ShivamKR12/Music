"""Playback UI, Carousel, File Picker, Queue Sheet, Volume & Listen Together Coordinator."""

from __future__ import annotations

import os
from typing import Any

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogHeadlineText,
    MDDialogSupportingText,
)
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemHeadlineText,
    MDListItemLeadingAvatar,
    MDListItemSupportingText,
)
from kivymd.uix.scrollview import MDScrollView

from app_core.service_container import resolve_symbol
from models.track_model import TrackModel
from services.logger import app_logger
from utils import theme_utils as theme_mod
from utils.media_utils import extract_video_id


class PlaybackUICoordinator:
    """Coordinates Now Playing carousel, mini-player visibility, file import, queue sheet & Listen Together."""

    def __init__(self, app: Any):
        self.app = app

    def on_player_playing_change(self, instance, is_playing: bool) -> None:
        app = self.app
        if hasattr(app, "listen_together_service") and app.listen_together_service.is_host and app.listen_together_service.is_connected:
            app.broadcast_listen_together_state()

    def on_active_track_change(self, instance, track) -> None:
        app = self.app
        updater = resolve_symbol("update_theme_from_image", theme_mod.update_theme_from_image)
        if track:
            if not app.mini_player_dismissed:
                app.mini_player_visible = True
            if hasattr(track, "album_art") and track.album_art and app.extract_artwork_colors:
                updater(track.album_art)
        else:
            app.mini_player_visible = False
        app.update_player_animated_bg()
        app._refresh_player_background_texture()
        app.current_lyric_line = "Tap for synchronized lyrics"
        app._current_inline_lyric_index = -1
        app.populate_inline_lyrics()
        sm = app.root.ids.get("screen_manager") if (hasattr(app, "root") and app.root and hasattr(app.root, "ids")) else None
        if (sm and sm.current == "lyrics") or (
            hasattr(app, "lyrics_sheet") and app.lyrics_sheet and (
                app.lyrics_sheet.state == "open" or getattr(app.lyrics_sheet, "status", None) == "opening_with_animation"
            )
        ):
            app.reload_lyrics_for_active_track()
        if hasattr(app, "listen_together_service") and app.listen_together_service.is_host and app.listen_together_service.is_connected:
            app.broadcast_listen_together_state()

    def ensure_player_carousel(self, force_refresh: bool = False) -> None:
        app = self.app
        if getattr(app, "_player_carousel_initialized", False) and not force_refresh:
            return
        if not hasattr(app, "root") or not app.root or not hasattr(app.root, "ids") or "screen_manager" not in app.root.ids:
            Clock.schedule_once(lambda dt: app.start_warmup_pipeline(), 0.05)
            return
        try:
            player_screen = app.root.ids.screen_manager.get_screen("player")
            carousel = player_screen.ids.album_carousel
        except Exception:
            return

        from kivymd.uix.card import MDCard
        from kivymd.uix.fitimage import FitImage

        app._updating_carousel = True
        try:
            carousel.clear_widgets()

            def create_slide_card():
                c = MDCard(
                    style="elevated",
                    radius=[dp(20)],
                    size_hint=(None, None),
                    size=(dp(230), dp(230)),
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    ripple_behavior=True,
                    theme_bg_color="Custom",
                    md_bg_color=[0, 0, 0, 0],
                    on_release=lambda *args: app.show_lyrics(),
                )
                img = FitImage(source="album_art.png", radius=[dp(20)], mipmap=True)
                c.add_widget(img)
                c._fit_img = img
                return c

            app._carousel_prev_card = create_slide_card()
            app._carousel_active_card = create_slide_card()
            app._carousel_next_card = create_slide_card()

            carousel.add_widget(app._carousel_prev_card)
            carousel.add_widget(app._carousel_active_card)
            carousel.add_widget(app._carousel_next_card)
            carousel.index = 1
            app._player_carousel_initialized = True
        finally:
            app._updating_carousel = False

        if app.player_controller.active_track:
            app.sync_player_carousel_track(app.player_controller.active_track)

    def sync_player_carousel_track(self, track) -> None:
        app = self.app
        if not hasattr(app, "_carousel_active_card") or not app._carousel_active_card:
            app.ensure_player_carousel()
        if not hasattr(app, "_carousel_active_card") or not app._carousel_active_card:
            return

        active_art = track.album_art if (track and getattr(track, "album_art", None)) else "album_art.png"
        app._carousel_active_card._fit_img.source = active_art

        queue = (
            app.player_controller.queue
            if (hasattr(app, "player_controller") and app.player_controller and app.player_controller.queue)
            else ([track] if track else [])
        )
        prev_art = active_art
        next_art = active_art
        if track and track in queue:
            idx = queue.index(track)
            if idx > 0:
                prev_art = queue[idx - 1].album_art or "album_art.png"
            if idx + 1 < len(queue):
                next_art = queue[idx + 1].album_art or "album_art.png"

        if hasattr(app, "_carousel_prev_card") and hasattr(app._carousel_prev_card, "_fit_img"):
            app._carousel_prev_card._fit_img.source = prev_art
        if hasattr(app, "_carousel_next_card") and hasattr(app._carousel_next_card, "_fit_img"):
            app._carousel_next_card._fit_img.source = next_art

        try:
            player_screen = app.root.ids.screen_manager.get_screen("player")
            carousel = player_screen.ids.album_carousel
            app._updating_carousel = True
            carousel.index = 1
        except Exception:
            pass
        finally:
            app._updating_carousel = False

    def on_carousel_index(self, index) -> None:
        app = self.app
        if index is None or getattr(app, "_updating_carousel", False):
            return
        if index == 0:
            app.player_controller.previous_track()
        elif index == 2:
            app.player_controller.next_track()

    def dismiss_mini_player(self) -> None:
        app = self.app
        if hasattr(app, "player_controller") and app.player_controller:
            app.player_controller.pause()
        app.mini_player_dismissed = True
        app.mini_player_visible = False
        app_logger.info("Mini player dismissed via swipe down gesture.")

    def play_selected_track(self, track) -> None:
        app = self.app
        app.mini_player_dismissed = False
        app.mini_player_visible = True
        app.ensure_player_carousel()
        if track not in app.playlist_model.tracks:
            app.playlist_model.add_track(track)
        matched_queue_track = None
        if hasattr(app, "active_playlist_tracks") and app.active_playlist_tracks:
            for pt in app.active_playlist_tracks:
                if pt == track or (getattr(pt, "video_id", None) and pt.video_id == getattr(track, "video_id", None)):
                    matched_queue_track = pt
                    break
        if matched_queue_track:
            app.player_controller.set_custom_queue(app.active_playlist_tracks, start_track=matched_queue_track)
            track = matched_queue_track
        app.player_controller.set_track(track)
        app.switch_screen("player")
        app.player_controller.play()
        app.sync_player_carousel_track(track)

    def file_manager_open(self) -> None:
        app = self.app

        def _open(granted=True):
            if not granted:
                app.show_toast("Storage permission needed to browse files")
                return
            start_path = os.path.expanduser("~")
            from kivy.utils import platform

            if platform == "android":
                for cand in ["/storage/emulated/0/Music", "/sdcard/Music", "/storage/emulated/0/Download", "/storage/emulated/0", "/sdcard"]:
                    if os.path.exists(cand):
                        start_path = cand
                        break
            if app.file_manager is None:
                app.file_manager = MDFileManager(
                    exit_manager=app.exit_manager,
                    select_path=app.select_path,
                    ext=[".mp3", ".m4a", ".wav", ".ogg", ".flac", ".opus", ".aac", ".wma", ".m4b"],
                )
            app.file_manager.show(start_path)

        app.ensure_storage_permissions(_open)

    def select_path(self, path: str) -> None:
        app = self.app
        app.exit_manager()
        if path and os.path.isfile(path):
            from utils.local_audio_utils import extract_local_audio_metadata

            meta = extract_local_audio_metadata(path, app.cache_dir)
            track = TrackModel.from_dict(meta)
            try:
                from models.database import add_playlist, add_track_to_playlist

                add_playlist("Offline Songs")
                add_track_to_playlist("Offline Songs", meta["video_id"], meta)
            except Exception as e:
                app_logger.error("select_path error saving to SQLite: %s", e)

            app.show_toast(f"Imported: {track.title}")
            app.play_selected_track(track)

    def exit_manager(self, *args) -> None:
        if self.app.file_manager:
            self.app.file_manager.close()

    def show_queue_sheet(self) -> None:
        app = self.app
        from kivymd.uix.bottomsheet import (
            MDBottomSheet,
            MDBottomSheetDragHandle,
            MDBottomSheetDragHandleButton,
            MDBottomSheetDragHandleTitle,
        )

        if not hasattr(app, "queue_sheet") or not app.queue_sheet:
            app.queue_sheet = MDBottomSheet(
                MDBottomSheetDragHandle(
                    MDBottomSheetDragHandleTitle(text="Up Next"),
                    MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: app.queue_sheet.set_state("close")),
                    drag_handle_color=app.theme_cls.onSurfaceVariantColor,
                ),
                size_hint_y=None,
                height="460dp",
                opening_time=0.2,
                closing_time=0.15,
            )
            app.queue_scroll = MDScrollView(size_hint=(1, 1), do_scroll_x=False)
            app.queue_box = MDList()
            app.queue_scroll.add_widget(app.queue_box)
            app.queue_sheet.add_widget(app.queue_scroll)
            Window.add_widget(app.queue_sheet)

        app.queue_sheet.width = Window.width
        app.queue_sheet.x = 0

        if hasattr(app, "player_controller") and app.player_controller and app.player_controller.queue:
            tracks = list(app.player_controller.queue)
        elif hasattr(app, "playlist_model") and app.playlist_model.tracks:
            tracks = list(app.playlist_model.tracks)
        else:
            tracks = []

        active = app.player_controller.active_track if hasattr(app, "player_controller") else None
        app.queue_box.clear_widgets()

        def build_queue_item(tr):
            is_active = (tr == active)
            art = tr.album_art if (tr.album_art and os.path.exists(tr.album_art)) else "album_art.png"
            return MDListItem(
                MDListItemLeadingAvatar(source=art, radius=[dp(8)] * 4, disabled=True),
                MDListItemHeadlineText(
                    text=f"▶  {tr.title}" if is_active else tr.title,
                    bold=is_active,
                    theme_text_color="Custom" if is_active else "Primary",
                    text_color=app.theme_cls.primaryColor if is_active else app.theme_cls.onSurfaceColor,
                ),
                MDListItemSupportingText(text=f"{tr.artist} • {tr.formatted_duration}"),
                on_release=lambda x, t=tr: (app.queue_sheet.set_state("close"), app.play_selected_track(t)),
                radius=[dp(12)] * 4,
                md_bg_color=app.theme_cls.surfaceContainerHighestColor if is_active else app.theme_cls.surfaceContainerColor,
            )

        batch_size = 20
        for tr in tracks[:batch_size]:
            app.queue_box.add_widget(build_queue_item(tr))

        def add_queue_chunks(start_idx):
            if start_idx >= len(tracks):
                return
            end_idx = min(start_idx + batch_size, len(tracks))
            for tr in tracks[start_idx:end_idx]:
                app.queue_box.add_widget(build_queue_item(tr))
            if end_idx < len(tracks):
                Clock.schedule_once(lambda dt: add_queue_chunks(end_idx), 0.03)

        if len(tracks) > batch_size:
            Clock.schedule_once(lambda dt: add_queue_chunks(batch_size), 0.03)
        app.queue_sheet.set_state("open")

    def set_volume(self, val: float) -> None:
        app = self.app
        app.current_volume = max(0.0, min(1.0, float(val)))
        if hasattr(app, "player_controller") and app.player_controller:
            app.player_controller.set_volume(app.current_volume)

    def toggle_mute(self) -> None:
        app = self.app
        if hasattr(app, "player_controller") and app.player_controller:
            app.player_controller.toggle_mute()
            app.current_volume = 0.0 if app.player_controller.is_muted else app.player_controller.volume

    def adjust_volume_delta(self, delta: float) -> None:
        app = self.app
        if hasattr(app, "player_controller") and app.player_controller:
            app.player_controller.adjust_volume(delta)
            app.current_volume = app.player_controller.volume

    # Listen Together Handlers & UI Methods
    def on_listen_together_state_changed(self, status: str, room_code: str) -> None:
        app = self.app
        app.listen_together_status = status
        app.listen_together_room_id = room_code
        app.listen_together_active = bool(status in ("HOSTING", "CONNECTED"))
        app.listen_together_role = "host" if status == "HOSTING" else ("client" if status == "CONNECTED" else "idle")

    def on_listen_together_members_updated(self, members: list) -> None:
        self.app.listen_together_members = list(members)

    def on_listen_together_playback_sync(self, msg: dict) -> None:
        app = self.app
        if not app.listen_together_service.is_connected or app.listen_together_service.is_host:
            return
        track_info = msg.get("track", {})
        elapsed = msg.get("elapsed", 0.0)
        is_paused = msg.get("paused", False)
        if not track_info:
            return

        target_vid = track_info.get("video_id") or extract_video_id(track_info.get("url", ""))
        active_t = app.player_controller.active_track
        curr_vid = getattr(active_t, "video_id", "") if active_t else ""

        if target_vid and curr_vid != target_vid:
            t = app.playlist_model.get_track_by_video_id(target_vid) or TrackModel.from_dict(track_info)
            app.play_selected_track(t)
            Clock.schedule_once(lambda dt: app.player_controller.seek(elapsed), 0.3)
        elif active_t and abs(getattr(active_t, "current_time", 0.0) - elapsed) > 1.5:
            app.player_controller.seek(elapsed)

        if is_paused and app.player_controller.is_playing:
            app.player_controller.toggle_play()
        elif not is_paused and not app.player_controller.is_playing:
            app.player_controller.toggle_play()

    def broadcast_listen_together_state(self) -> None:
        app = self.app
        if not hasattr(app, "listen_together_service") or not app.listen_together_service.is_host:
            return
        active_t = app.player_controller.active_track
        if not active_t:
            return
        t_dict = {
            "title": active_t.title,
            "artist": active_t.artist,
            "url": getattr(active_t, "url", ""),
            "video_id": getattr(active_t, "video_id", ""),
            "duration": active_t.duration,
            "artwork": getattr(active_t, "album_art", ""),
        }
        elapsed = getattr(active_t, "current_time", 0.0)
        app.listen_together_service.broadcast_playback_sync(t_dict, elapsed, not app.player_controller.is_playing)

    def create_listen_together_room(self) -> None:
        app = self.app
        room_code = app.listen_together_service.create_room(user_name="You")
        app.show_toast(f"Hosting Listen Together {room_code}!")
        app.broadcast_listen_together_state()

    def show_join_listen_together_dialog(self) -> None:
        app = self.app
        from kivymd.uix.textfield import MDTextField, MDTextFieldHintText

        field = MDTextField(MDTextFieldHintText(text="Enter Room Code (e.g. #8492 or IP)"), text="#", mode="outlined")

        def on_connect(x):
            code = field.text.strip()
            app.listen_together_dialog.dismiss()
            if not code or code == "#":
                app.show_toast("Please enter a valid room code.")
                return
            host_ip = code.split(":")[0] if ":" in code else "127.0.0.1"
            if app.listen_together_service.join_room(room_code=code, host_ip=host_ip, user_name="You"):
                app.show_toast(f"Joined Room {code}!")

        app.listen_together_dialog = MDDialog(
            MDDialogHeadlineText(text="Join Listen Together"),
            MDDialogSupportingText(text="Enter your friend's room code to start synchronized listening:"),
            MDDialogContentContainer(field, orientation="vertical"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: app.listen_together_dialog.dismiss()),
                MDButton(MDButtonText(text="JOIN"), style="text", on_release=on_connect),
            ),
        )
        app.listen_together_dialog.open()

    def copy_listen_together_code(self) -> None:
        app = self.app
        if not app.listen_together_room_id:
            return
        from kivy.core.clipboard import Clipboard

        Clipboard.copy(app.listen_together_room_id)
        app.show_toast(f"Room code {app.listen_together_room_id} copied to clipboard!")

    def add_demo_listen_together_peer(self) -> None:
        app = self.app
        if app.listen_together_service.is_connected:
            peers = ["Alex R.", "Jordan K.", "Sam M.", "Taylor S."]
            curr_names = [m["name"].split(" ")[0] for m in app.listen_together_members]
            avail = [p for p in peers if p.split(" ")[0] not in curr_names]
            name = avail[0] if avail else f"Guest {len(app.listen_together_members)}"
            app.listen_together_service.add_demo_peer(name)
            app.broadcast_listen_together_state()

    def leave_listen_together(self) -> None:
        self.app.listen_together_service.leave_room()
        self.app.show_toast("Left Listen Together session")
