"""Navigation Coordinator (ScreenManager stack, transitions, hardware back & nav bar)."""

from __future__ import annotations

import os
from typing import Any

from services.logger import app_logger


class NavigationCoordinator:
    """Manages screen switching, history back-stack, transitions, overlays dismissal, and bottom nav."""

    def __init__(self, app: Any):
        self.app = app

    def toggle_ui_mode(self) -> None:
        self.app.show_toast("Modern SimpMusic UI is permanently active")

    def switch_ui_mode(self, mode: str) -> None:
        self.app.ui_mode = self.app.UI_MODE_NEW

    def switch_screen(self, screen_name: str) -> None:
        """Navigate to screen, lazy-instantiating on demand, and push to navigation stack."""
        app = self.app
        if hasattr(app, "root") and app.root and hasattr(app.root, "ids") and "screen_manager" in app.root.ids:
            sm = app.root.ids.screen_manager
            if not sm.has_screen(screen_name):
                try:
                    sm.get_screen(screen_name)
                except Exception as e:
                    app_logger.error(f"Failed to instantiate screen '{screen_name}': {e}")
                    return
            if sm.has_screen(screen_name) and sm.current != screen_name:
                old_screen = sm.current
                app.screen_history.append(old_screen)
                if os.environ.get("KIVY_HEADLESS") == "1" or sm.width == 0 or sm.height == 0:
                    from kivy.uix.screenmanager import NoTransition

                    prev_trans = sm.transition
                    sm.transition = NoTransition()
                    sm.current = screen_name
                    sm.transition = prev_trans
                else:
                    from kivy.uix.screenmanager import SlideTransition

                    if not isinstance(sm.transition, SlideTransition):
                        sm.transition = SlideTransition(duration=0.18)

                    tab_indices = {"home": 0, "search": 1, "library": 2, "browse": 3}
                    if screen_name == "player":
                        sm.transition.direction = "up"
                    elif old_screen == "player":
                        sm.transition.direction = "down"
                    elif old_screen in tab_indices and screen_name in tab_indices:
                        sm.transition.direction = "left" if tab_indices[screen_name] > tab_indices[old_screen] else "right"
                    else:
                        sm.transition.direction = "left"

                    sm.current = screen_name
                app.sync_nav_bar(screen_name)
                if screen_name == "player":
                    app.ensure_player_carousel()
                elif screen_name == "recently_played":
                    app.load_recently_played_data()
                elif screen_name == "analytics":
                    app.load_analytics_data()
                elif screen_name == "podcasts":
                    app.load_podcasts_data()
                elif screen_name == "library":
                    app.refresh_library_data()
                elif screen_name == "settings":
                    app.refresh_cache_size()

    def _close_open_overlays(self) -> bool:
        app = self.app
        if hasattr(app, "lyrics_sheet") and app.lyrics_sheet and (
            app.lyrics_sheet.state == "open" or getattr(app.lyrics_sheet, "status", None) == "opening_with_animation"
        ):
            if hasattr(app, "_lyrics_event") and app._lyrics_event:
                app._lyrics_event.cancel()
                app._lyrics_event = None
            if hasattr(app, "_lyrics_scroll_anim") and app._lyrics_scroll_anim:
                try:
                    app._lyrics_scroll_anim.stop(app._lyrics_scroll_view)
                except Exception:
                    pass
                app._lyrics_scroll_anim = None
            app.lyrics_sheet.set_state("close")
            return True
        if hasattr(app, "queue_sheet") and app.queue_sheet and (
            app.queue_sheet.state == "open" or getattr(app.queue_sheet, "status", None) == "opening_with_animation"
        ):
            app.queue_sheet.set_state("close")
            return True
        if hasattr(app, "bottom_sheet") and app.bottom_sheet and (
            app.bottom_sheet.state == "open" or getattr(app.bottom_sheet, "status", None) == "opening_with_animation"
        ):
            app.bottom_sheet.set_state("close")
            return True
        for attr in ("dialog", "quality_dialog", "cache_dialog", "autoeq_dialog", "auth_dialog"):
            dlg = getattr(app, attr, None)
            if dlg and getattr(dlg, "_is_open", False):
                dlg.dismiss()
                return True
        return False

    def go_back(self, target=None) -> None:
        """Unified back action for UI back buttons and Android hardware back key."""
        app = self.app
        if self._close_open_overlays():
            return
        if hasattr(app, "root") and app.root and hasattr(app.root, "ids") and "screen_manager" in app.root.ids:
            sm = app.root.ids.screen_manager
            old_screen = sm.current
            dest = target
            if not dest:
                if app.screen_history:
                    dest = app.screen_history.pop()
                    while dest == "splash" and app.screen_history:
                        dest = app.screen_history.pop()
                    if dest == "splash":
                        dest = "home"
                else:
                    dest = "home"
            if os.environ.get("KIVY_HEADLESS") == "1" or sm.width == 0 or sm.height == 0:
                from kivy.uix.screenmanager import NoTransition

                prev_trans = sm.transition
                sm.transition = NoTransition()
                sm.current = dest
                sm.transition = prev_trans
            else:
                from kivy.uix.screenmanager import SlideTransition

                if not isinstance(sm.transition, SlideTransition):
                    sm.transition = SlideTransition(duration=0.22)
                sm.transition.direction = "down" if old_screen == "player" else "right"
                sm.current = dest
            app.sync_nav_bar(dest)

    def on_keyboard(self, window, key, scancode=None, codepoint=None, modifier=None, *args, **kwargs) -> bool:
        """Handle hardware keys, including Android back button (Key 27 / Escape)."""
        app = self.app
        if key == 27:
            if hasattr(app, "root") and app.root and hasattr(app.root, "ids") and "screen_manager" in app.root.ids:
                sm = app.root.ids.screen_manager
                has_overlay = (
                    (hasattr(app, "lyrics_sheet") and app.lyrics_sheet and (
                        app.lyrics_sheet.state == "open" or getattr(app.lyrics_sheet, "status", None) == "opening_with_animation"
                    ))
                    or (hasattr(app, "queue_sheet") and app.queue_sheet and (
                        app.queue_sheet.state == "open" or getattr(app.queue_sheet, "status", None) == "opening_with_animation"
                    ))
                    or (hasattr(app, "bottom_sheet") and app.bottom_sheet and (
                        app.bottom_sheet.state == "open" or getattr(app.bottom_sheet, "status", None) == "opening_with_animation"
                    ))
                    or any(
                        getattr(getattr(app, attr, None), "_is_open", False)
                        for attr in ("dialog", "quality_dialog", "cache_dialog", "autoeq_dialog", "auth_dialog")
                    )
                )
                if has_overlay or sm.current != "home":
                    app.go_back()
                    return True
            return False
        return False

    def on_switch_tabs(self, bar, item, item_icon: str, item_text: str) -> None:
        """Handle tab transitions from the Material 3 Navigation Bar."""
        mapping = {"Home": "home", "Search": "search", "Library": "library"}
        target = mapping.get(item_text, item_text.lower())
        app = self.app
        if hasattr(app, "root") and app.root and hasattr(app.root, "ids") and "screen_manager" in app.root.ids:
            app.switch_screen(target)

    def sync_nav_bar(self, screen_name: str) -> None:
        """Keep the MDNavigationBar active indicator in sync with the ScreenManager."""
        app = self.app
        app.active_tab_name = screen_name
        mapping = {"home": "Home", "search": "Search", "library": "Library"}
        target_text = mapping.get(screen_name, screen_name.capitalize())
        if hasattr(app, "root") and app.root and hasattr(app.root, "ids") and "bottom_nav" in app.root.ids:
            nav = app.root.ids.bottom_nav
            for item in nav.children:
                if hasattr(item, "text") and item.text == target_text:
                    nav.set_active_item(item)
                    return
