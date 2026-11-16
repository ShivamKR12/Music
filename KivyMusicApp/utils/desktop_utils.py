"""
Desktop Integration & Ergonomics Utility for KivyMusicApp.
Provides:
1. Global keyboard shortcuts arbitration (Space, Arrows, Media keys, M, L, Q, F, Esc).
2. Desktop window constraints (minimum width/height, state persistence).
3. System media controls (SMTC) and system tray hooks with safe cross-platform fallbacks.
"""

import sys
import os
from typing import Optional
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock
from models.database import get_setting, set_setting

class DesktopKeyboardManager:
    """Manages global keyboard shortcuts for desktop playback and navigation."""

    KEY_SPACE = 32
    KEY_LEFT = 276
    KEY_RIGHT = 275
    KEY_UP = 273
    KEY_DOWN = 274
    KEY_M = 109
    KEY_L = 108
    KEY_Q = 113
    KEY_F = 102
    KEY_F11 = 292
    KEY_SLASH = 47
    KEY_ESC = 27

    def __init__(self, app):
        self.app = app
        self.enabled = (platform not in ('android', 'ios'))
        if self.enabled:
            Window.bind(on_key_down=self._on_key_down)

    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        """Dispatches keyboard shortcuts if not currently typing in a text field."""
        # 1. Check if user is typing in a text input
        focused_widget = None
        for w in Window.children:
            if hasattr(w, "focus") and w.focus:
                focused_widget = w
                break
            if hasattr(w, "walk"):
                for child in w.walk():
                    if hasattr(child, "focus") and child.focus:
                        focused_widget = child
                        break
        if focused_widget is not None:
            # Let text input handle typing
            if key == self.KEY_ESC:
                focused_widget.focus = False
                return True
            return False

        ctrl_pressed = 'ctrl' in modifiers
        shift_pressed = 'shift' in modifiers

        # Space: Play / Pause toggle
        if key == self.KEY_SPACE:
            if hasattr(self.app, "player_controller") and self.app.player_controller:
                self.app.player_controller.toggle_play()
            return True

        # Left / Right Arrow: Seek or Prev/Next
        elif key == self.KEY_LEFT:
            if shift_pressed:
                if hasattr(self.app, "player_controller"):
                    self.app.player_controller.prev_track()
            else:
                if hasattr(self.app, "player_controller"):
                    cur = self.app.player_controller.current_time
                    self.app.player_controller.seek(max(0.0, cur - 5.0))
            return True

        elif key == self.KEY_RIGHT:
            if shift_pressed:
                if hasattr(self.app, "player_controller"):
                    self.app.player_controller.next_track()
            else:
                if hasattr(self.app, "player_controller"):
                    cur = self.app.player_controller.current_time
                    dur = self.app.player_controller.duration
                    self.app.player_controller.seek(min(dur, cur + 5.0))
            return True

        # Up / Down Arrow: Volume adjustments
        elif key == self.KEY_UP:
            if hasattr(self.app, "adjust_volume_delta"):
                self.app.adjust_volume_delta(+0.05)
            return True

        elif key == self.KEY_DOWN:
            if hasattr(self.app, "adjust_volume_delta"):
                self.app.adjust_volume_delta(-0.05)
            return True

        # M: Mute toggle
        elif key == self.KEY_M:
            if hasattr(self.app, "toggle_mute"):
                self.app.toggle_mute()
            return True

        # L: Toggle Lyrics
        elif key == self.KEY_L:
            if hasattr(self.app, "toggle_desktop_lyrics_panel"):
                self.app.toggle_desktop_lyrics_panel()
            elif hasattr(self.app, "show_lyrics"):
                self.app.show_lyrics()
            return True

        # Q: Toggle Queue
        elif key == self.KEY_Q:
            if hasattr(self.app, "toggle_desktop_queue_panel"):
                self.app.toggle_desktop_queue_panel()
            elif hasattr(self.app, "show_up_next"):
                self.app.show_up_next()
            return True

        # F or F11: Fullscreen toggle
        elif key in (self.KEY_F, self.KEY_F11):
            if not ctrl_pressed:
                self.app.toggle_fullscreen()
                return True

        # Ctrl+F or /: Search
        elif (key == self.KEY_SLASH) or (ctrl_pressed and codepoint == 'f'):
            self.app.switch_screen("search")
            return True

        # Esc: Close side panels or go back
        elif key == self.KEY_ESC:
            if getattr(self.app, "desktop_panel_open", False):
                self.app.desktop_panel_open = False
                return True
            self.app.go_back()
            return True

        return False


def setup_desktop_window(app):
    """Configures minimum window dimensions and restores saved window state."""
    if platform in ('android', 'ios'):
        return

    # In headless testing or mobile simulation, do not lock minimum desktop window bounds
    if os.environ.get("KIVY_HEADLESS") == "1":
        return

    # Set minimum window boundary to prevent layout collapse
    Window.minimum_width = 860
    Window.minimum_height = 600

    # Restore saved window size if exists
    saved_w = get_setting("window_width")
    saved_h = get_setting("window_height")
    if saved_w and saved_h:
        try:
            w = int(saved_w)
            h = int(saved_h)
            if w >= 860 and h >= 600:
                Window.size = (w, h)
        except Exception:
            pass

    # Save window dimensions on window resize
    def _on_window_resize(win, w, h):
        if w >= 860 and h >= 600:
            set_setting("window_width", str(int(w)))
            set_setting("window_height", str(int(h)))

    Window.bind(on_resize=_on_window_resize)
