"""Synchronized Lyrics Coordinator (Popup Bottom Sheet & Inline Player Card)."""

from __future__ import annotations

from typing import Any

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.bottomsheet import (
    MDBottomSheet,
    MDBottomSheetDragHandle,
    MDBottomSheetDragHandleButton,
    MDBottomSheetDragHandleTitle,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel

from services.lyrics_service import fetch_lyrics_async, find_active_line_index, parse_lrc
from views.components import LyricsScrollView


class LyricsCoordinator:
    """Manages interactive synchronized lyrics sheet and inline Now Playing card centering."""

    def __init__(self, app: Any):
        self.app = app

    def _cleanup_sheet_timers(self, reset_scroll_top: bool = False) -> None:
        app = self.app
        if hasattr(app, "_lyrics_event") and app._lyrics_event:
            app._lyrics_event.cancel()
            app._lyrics_event = None
        if hasattr(app, "_lyrics_scroll_anim") and app._lyrics_scroll_anim:
            try:
                app._lyrics_scroll_anim.stop(app._lyrics_scroll_view)
            except Exception:
                pass
            app._lyrics_scroll_anim = None
        if hasattr(app, "_lyrics_scroll_view") and app._lyrics_scroll_view:
            if app._lyrics_scroll_view.resume_event:
                app._lyrics_scroll_view.resume_event.cancel()
                app._lyrics_scroll_view.resume_event = None
            app._lyrics_scroll_view.user_scrolling = False
            if reset_scroll_top:
                app._lyrics_scroll_view.scroll_y = 1.0

    def on_player_time_change(self, instance, current_time: float) -> None:
        app = self.app
        parsed = getattr(app, "_inline_active_parsed_lyrics", None)
        widgets = getattr(app, "_inline_lyric_widgets", None)
        if not parsed or not widgets:
            return
        idx = find_active_line_index(parsed, float(current_time or 0.0) + getattr(app, "lyrics_timing_offset", 0.0))
        old_idx = getattr(app, "_current_inline_lyric_index", -1)
        if idx != old_idx and 0 <= idx < len(widgets):
            if 0 <= old_idx < len(widgets):
                _, old_box, old_lbl = widgets[old_idx]
                old_lbl.font_style = "Body"
                old_lbl.role = "large"
                old_lbl.bold = False
                old_lbl.opacity = 0.45
                old_box.md_bg_color = [0, 0, 0, 0]

            _, new_box, new_lbl = widgets[idx]
            new_lbl.font_style = "Title"
            new_lbl.role = "medium"
            new_lbl.bold = True
            new_lbl.opacity = 1.0
            new_box.md_bg_color = [1, 1, 1, 0.12]
            app._current_inline_lyric_index = idx
            app.current_lyric_line = new_lbl.text
            app._recenter_inline_lyric()

    def show_lyrics_sheet(self):
        return self.show_lyrics()

    def show_lyrics(self) -> None:
        app = self.app
        track = app.player_controller.active_track
        if not track:
            return

        def close_lyrics(*args):
            self._cleanup_sheet_timers()
            if hasattr(app, "lyrics_sheet") and app.lyrics_sheet:
                if app.lyrics_sheet.state != "close" and getattr(app.lyrics_sheet, "status", None) != "closing_with_animation":
                    app.lyrics_sheet.set_state("close")

        app._lyrics_drag_title = MDBottomSheetDragHandleTitle(text=f"Lyrics - {track.title[:22]}")
        app.lyrics_sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                app._lyrics_drag_title,
                MDBottomSheetDragHandleButton(icon="close", on_release=close_lyrics),
            ),
            size_hint_y=None,
            height="480dp",
            opening_time=0.2,
            closing_time=0.15,
        )
        app.lyrics_sheet.bind(on_close=lambda *a: self._cleanup_sheet_timers())

        app._lyrics_scroll_view = LyricsScrollView(size_hint_y=None, height="400dp", do_scroll_x=False)
        app._lyrics_scroll_view.scroll_y = 1.0
        app._lyrics_box = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=["16dp", "180dp", "16dp", "200dp"],
            spacing="8dp",
        )
        app._lyrics_scroll_view.add_widget(app._lyrics_box)
        app._lyrics_scroll_view.on_resume_callback = app._recenter_active_lyric
        app._lyrics_scroll_anim = None

        app.lyrics_sheet.add_widget(app._lyrics_scroll_view)
        Window.add_widget(app.lyrics_sheet)
        app.lyrics_sheet.width = Window.width
        app.lyrics_sheet.x = 0
        app.lyrics_sheet.set_state("open")

        app._populate_lyrics_content(track)

    def recenter_active_lyric(self) -> None:
        app = self.app
        if not getattr(app, "_lyric_line_widgets", None):
            return
        if not getattr(app, "_lyrics_scroll_view", None):
            return
        idx = getattr(app, "_current_lyric_index", -1)
        if not (0 <= idx < len(app._lyric_line_widgets)):
            return
        _, active_box, _ = app._lyric_line_widgets[idx]
        scroll = app._lyrics_scroll_view
        box = app._lyrics_box
        H_view = scroll.height
        H_box = box.height

        if (H_box <= H_view or (idx == 0 and active_box.y == 0)) and len(app._lyric_line_widgets) > 2:
            Clock.schedule_once(lambda dt: app._recenter_active_lyric(), 0.05)
            return

        if H_box > H_view:
            y_target = active_box.y + active_box.height / 2.0
            target_scroll_y = max(0.0, min(1.0, (y_target - H_view / 2.0) / (H_box - H_view)))
            if hasattr(app, "_lyrics_scroll_anim") and app._lyrics_scroll_anim:
                try:
                    app._lyrics_scroll_anim.stop(scroll)
                except Exception:
                    pass
                app._lyrics_scroll_anim = None
            anim = Animation(scroll_y=target_scroll_y, duration=0.35, t="out_quad")
            app._lyrics_scroll_anim = anim
            Clock.schedule_once(
                lambda dt: anim.start(scroll) if hasattr(app, "_lyrics_scroll_view") and app._lyrics_scroll_view else None,
                0,
            )

    def populate_lyrics_content(self, track) -> None:
        app = self.app
        box = app._lyrics_box
        box.clear_widgets()
        self._cleanup_sheet_timers(reset_scroll_top=True)

        class ClickableLyricBox(ButtonBehavior, MDBoxLayout):
            pass

        if hasattr(app, "_lyrics_drag_title") and app._lyrics_drag_title:
            app._lyrics_drag_title.text = f"Lyrics - {track.title[:22]}"

        def populate_lyrics(synced_src, plain_src):
            box.clear_widgets()
            self._cleanup_sheet_timers(reset_scroll_top=True)

            box.add_widget(
                MDLabel(
                    text=f"{track.title}\n{track.artist}",
                    font_style="Title",
                    role="medium",
                    bold=True,
                    adaptive_height=True,
                    halign="center",
                    font_name=app.resolved_unicode_font_name,
                    padding=["0dp", "8dp"],
                )
            )

            if synced_src:
                offset_bar = MDBoxLayout(
                    orientation="horizontal",
                    adaptive_size=True,
                    pos_hint={"center_x": 0.5},
                    spacing="8dp",
                    padding=["0dp", "4dp"],
                )
                offset_bar.add_widget(MDButton(MDButtonText(text="-0.5s"), style="tonal", height="32dp", on_release=lambda x: app.adjust_lyrics_offset(-0.5)))
                offset_bar.add_widget(
                    MDButton(
                        MDButtonText(text=f"Sync ({app.lyrics_timing_offset:+.1f}s)" if app.lyrics_timing_offset != 0.0 else "Sync (0.0s)"),
                        style="text",
                        height="32dp",
                        on_release=lambda x: app.adjust_lyrics_offset(0.0),
                    )
                )
                offset_bar.add_widget(MDButton(MDButtonText(text="+0.5s"), style="tonal", height="32dp", on_release=lambda x: app.adjust_lyrics_offset(+0.5)))
                box.add_widget(offset_bar)

            parsed = parse_lrc(synced_src or plain_src, timing_offset=app.lyrics_timing_offset)
            if parsed:
                app._active_parsed_lyrics = parsed
                app._lyric_line_widgets = []
                app._current_lyric_index = -1

                for sec, line_text in parsed:
                    cbox = ClickableLyricBox(
                        orientation="vertical",
                        size_hint_y=None,
                        adaptive_height=True,
                        padding=["16dp", "8dp"],
                        radius=[dp(12)],
                        md_bg_color=[0, 0, 0, 0],
                    )
                    lbl = MDLabel(
                        text=line_text,
                        font_style="Body",
                        role="large",
                        adaptive_height=True,
                        halign="center",
                        font_name=app.resolved_unicode_font_name,
                        opacity=0.45,
                        theme_text_color="Custom",
                        text_color=app.theme_cls.onSurfaceVariantColor,
                    )
                    cbox.add_widget(lbl)

                    def _on_lyric_click(s_sec):
                        app.player_controller.seek(s_sec)
                        if hasattr(app, "_lyrics_scroll_view") and app._lyrics_scroll_view:
                            app._lyrics_scroll_view.user_scrolling = False
                            if app._lyrics_scroll_view.resume_event:
                                app._lyrics_scroll_view.resume_event.cancel()
                                app._lyrics_scroll_view.resume_event = None
                        Clock.schedule_once(lambda dt: app._recenter_active_lyric(), 0)

                    cbox.bind(on_release=lambda instance, s=sec: _on_lyric_click(s))
                    box.add_widget(cbox)
                    app._lyric_line_widgets.append((sec, cbox, lbl))

                box.do_layout()

                def _update_lyric_tracker(dt):
                    if not getattr(app, "_active_parsed_lyrics", None):
                        return
                    elapsed = getattr(app.player_controller, "current_time", 0.0)
                    idx = find_active_line_index(app._active_parsed_lyrics, elapsed)
                    old_idx = getattr(app, "_current_lyric_index", -1)
                    if idx != old_idx and 0 <= idx < len(app._lyric_line_widgets):
                        if 0 <= old_idx < len(app._lyric_line_widgets):
                            _, old_box, old_lbl = app._lyric_line_widgets[old_idx]
                            old_lbl.font_style = "Body"
                            old_lbl.role = "large"
                            old_lbl.bold = False
                            old_lbl.opacity = 0.45
                            old_lbl.text_color = app.theme_cls.onSurfaceVariantColor
                            old_box.md_bg_color = [0, 0, 0, 0]

                        _, new_box, new_lbl = app._lyric_line_widgets[idx]
                        new_lbl.font_style = "Title"
                        new_lbl.role = "medium"
                        new_lbl.bold = True
                        new_lbl.opacity = 1.0
                        new_lbl.text_color = app.theme_cls.primaryColor
                        new_box.md_bg_color = [app.theme_cls.primaryColor[0], app.theme_cls.primaryColor[1], app.theme_cls.primaryColor[2], 0.15]
                        app._current_lyric_index = idx

                        if hasattr(app, "_lyrics_scroll_view") and app._lyrics_scroll_view and not app._lyrics_scroll_view.user_scrolling:
                            app._recenter_active_lyric()

                if hasattr(app, "_lyrics_event") and app._lyrics_event:
                    app._lyrics_event.cancel()
                app._lyrics_event = Clock.schedule_interval(_update_lyric_tracker, 0.25)
                Clock.schedule_once(lambda dt: _update_lyric_tracker(0), 0.05)
            else:
                box.add_widget(
                    MDLabel(
                        text=plain_src or synced_src or "No lyrics found for this track.",
                        font_style="Body",
                        role="large",
                        adaptive_height=True,
                        halign="center",
                        font_name=app.resolved_unicode_font_name,
                        padding=["16dp", "16dp"],
                    )
                )

        synced = getattr(track, "synced_lyrics", "").strip()
        plain = getattr(track, "lyrics", "").strip()
        if synced or (plain and "dummy lyrics" not in plain.lower() and "fetching lyrics" not in plain.lower()):
            populate_lyrics(synced, plain)
        else:
            box.add_widget(
                MDLabel(
                    text=f"{track.title}\n{track.artist}",
                    font_style="Title",
                    role="medium",
                    bold=True,
                    adaptive_height=True,
                    halign="center",
                    font_name=app.resolved_unicode_font_name,
                    padding=["0dp", "8dp"],
                )
            )
            box.add_widget(
                MDLabel(
                    text="Fetching synchronized lyrics...",
                    font_style="Body",
                    role="medium",
                    adaptive_height=True,
                    halign="center",
                    font_name=app.resolved_unicode_font_name,
                    opacity=0.7,
                )
            )

            def on_fetched(res):
                track.lyrics = getattr(res, "plain", str(res))
                track.synced_lyrics = getattr(res, "synced", "")
                populate_lyrics(track.synced_lyrics, track.lyrics)

            fetch_lyrics_async(
                track.title, track.artist, track.video_id,
                cache_dir=app.cache_dir, on_success=on_fetched,
                local_path=getattr(track, "local_path", None),
            )

    def reload_lyrics_for_active_track(self) -> None:
        app = self.app
        track = app.player_controller.active_track
        if not track:
            return
        self._cleanup_sheet_timers(reset_scroll_top=True)
        app._current_lyric_index = -1
        if hasattr(app, "_lyrics_box") and app._lyrics_box:
            app._populate_lyrics_content(track)

    def populate_inline_lyrics(self) -> None:
        app = self.app
        if not app.root or not hasattr(app.root, "ids") or "screen_manager" not in app.root.ids:
            return
        sm = app.root.ids.screen_manager
        if not sm.has_screen("player"):
            return
        player = sm.get_screen("player")
        if "inline_lyrics_box" not in player.ids:
            return

        box = player.ids.inline_lyrics_box
        scroll = player.ids.inline_lyrics_scroll
        scroll.scroll_y = 1.0
        scroll.user_scrolling = False
        box.clear_widgets()
        app._inline_lyric_widgets = []
        app._inline_active_parsed_lyrics = []

        track = app.player_controller.active_track
        if not track:
            box.add_widget(
                MDLabel(
                    text="No track currently playing",
                    font_style="Body",
                    role="medium",
                    adaptive_height=True,
                    halign="center",
                    opacity=0.6,
                    theme_text_color="Custom",
                    text_color=[1, 1, 1, 0.6],
                )
            )
            return

        class ClickableInlineLyricBox(ButtonBehavior, MDBoxLayout):
            pass

        def _render_lines(synced_src, plain_src):
            box.clear_widgets()
            app._inline_lyric_widgets = []
            app._inline_active_parsed_lyrics = []
            scroll.scroll_y = 1.0
            scroll.user_scrolling = False

            if synced_src:
                parsed = parse_lrc(synced_src)
                app._inline_active_parsed_lyrics = parsed
                for timestamp, text in parsed:
                    line_box = ClickableInlineLyricBox(
                        orientation="horizontal",
                        adaptive_height=True,
                        padding=["12dp", "6dp"],
                        radius=[dp(10)],
                        spacing="8dp",
                    )
                    lbl = MDLabel(
                        text=text,
                        font_style="Body",
                        role="large",
                        adaptive_height=True,
                        opacity=0.45,
                        font_name=app.resolved_unicode_font_name,
                        theme_text_color="Custom",
                        text_color=[1, 1, 1, 0.70],
                    )
                    line_box.add_widget(lbl)
                    line_box.bind(on_release=lambda instance, t=timestamp: app.player_controller.seek_to(t))
                    box.add_widget(line_box)
                    app._inline_lyric_widgets.append((timestamp, line_box, lbl))
                if "inline_lyrics_footer" in player.ids:
                    player.ids.inline_lyrics_footer.text = "LINE_SYNCED • SimpMusic / LRCLIB / YouTube"
            else:
                box.add_widget(
                    MDLabel(
                        text=plain_src or "No lyrics available for this track.",
                        font_style="Body",
                        role="medium",
                        adaptive_height=True,
                        halign="center",
                        font_name=app.resolved_unicode_font_name,
                        theme_text_color="Custom",
                        text_color=[1, 1, 1, 0.8],
                    )
                )
                if "inline_lyrics_footer" in player.ids:
                    player.ids.inline_lyrics_footer.text = "UNSYNCED • YouTube Music"

        synced = getattr(track, "synced_lyrics", "").strip()
        plain = getattr(track, "lyrics", "").strip()
        if synced or (plain and "dummy lyrics" not in plain.lower() and "fetching lyrics" not in plain.lower()):
            _render_lines(synced, plain)
        else:
            box.add_widget(
                MDLabel(
                    text="Fetching synchronized lyrics...",
                    font_style="Body",
                    role="medium",
                    adaptive_height=True,
                    halign="center",
                    opacity=0.6,
                    theme_text_color="Custom",
                    text_color=[1, 1, 1, 0.6],
                )
            )

            def _on_fetched_inline(res):
                track.lyrics = getattr(res, "plain", str(res))
                track.synced_lyrics = getattr(res, "synced", "")
                _render_lines(track.synced_lyrics, track.lyrics)

            fetch_lyrics_async(
                track.title, track.artist, track.video_id,
                cache_dir=app.cache_dir, on_success=_on_fetched_inline,
                local_path=getattr(track, "local_path", None),
            )

    def recenter_inline_lyric(self) -> None:
        app = self.app
        if not getattr(app, "_inline_lyric_widgets", None):
            return
        if not app.root or not hasattr(app.root, "ids") or "screen_manager" not in app.root.ids:
            return
        sm = app.root.ids.screen_manager
        if not sm.has_screen("player"):
            return
        player = sm.get_screen("player")
        if "inline_lyrics_scroll" not in player.ids or "inline_lyrics_box" not in player.ids:
            return
        scroll = player.ids.inline_lyrics_scroll
        box = player.ids.inline_lyrics_box
        if getattr(scroll, "user_scrolling", False):
            return
        idx = getattr(app, "_current_inline_lyric_index", -1)
        if not (0 <= idx < len(app._inline_lyric_widgets)):
            return
        _, active_box, _ = app._inline_lyric_widgets[idx]
        H_view = scroll.height
        H_box = box.height
        if H_box > H_view:
            y_target = active_box.y + active_box.height / 2.0
            target_scroll_y = max(0.0, min(1.0, (y_target - H_view / 2.0) / (H_box - H_view)))
            Animation.stop_all(scroll, "scroll_y")
            Animation(scroll_y=target_scroll_y, duration=0.3, t="out_quad").start(scroll)
