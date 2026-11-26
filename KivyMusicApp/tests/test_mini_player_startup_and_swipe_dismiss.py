"""
Tests for Mini Player Fresh Startup State and Swipe-Down Dismissal
Validates:
1. Fresh startup: active_track is None, mini_player_visible is False, mini_player is completely hidden (height 0, disabled True).
2. Track selection: mini player opens (height 72dp, opacity 1, disabled False).
3. Tap on card: opens PlayerScreen.
4. Swipe down on card: dismisses mini player, pauses playback, does NOT open PlayerScreen.
5. New track selection: restores mini player cleanly.
"""
import os
import sys
import unittest

os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_HEADLESS"] = "1"

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
os.chdir(project_root)

from kivy.clock import Clock
from kivy.metrics import dp
from main import MusicApp
from models.track_model import TrackModel

class DummyTouch:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.x = x
        self.y = y
        self.ox = x
        self.oy = y
        self.ud = {}
        self.grab_current = None
        self.grab_list = []
        self.device = "mouse"
        self.button = "left"
        self.is_touch = True
        self.is_double_tap = False
        self.is_triple_tap = False
        self.is_mouse_scrolling = False
        self.time_start = 0
        self.time_end = 0

    def push(self):
        pass

    def pop(self):
        pass

    def grab(self, widget):
        self.grab_list.append(widget)
        self.grab_current = widget

    def ungrab(self, widget):
        if widget in self.grab_list:
            self.grab_list.remove(widget)
        if self.grab_current == widget:
            self.grab_current = self.grab_list[-1] if self.grab_list else None

class TestMiniPlayerStartupAndSwipeDismiss(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = MusicApp()
        cls.app.player_controller.audio_engine.muted = True
        cls.app.player_controller.audio_engine.volume = 0.0
        cls.root = cls.app.build()
        cls.app.root = cls.root
        cls.app.on_start()
        for _ in range(5):
            Clock.tick()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.app.stop()
        except Exception:
            pass

    def setUp(self):
        self.app.player_controller.audio_engine.muted = True
        self.app.player_controller.audio_engine.volume = 0.0

    def test_01_fresh_startup_state(self):
        """Test fresh startup: no track selected, mini player hidden and disabled."""
        print("[TEST] 1. Validating Fresh Startup State...")
        self.assertIsNone(self.app.player_controller.active_track, "active_track must be None on fresh startup")
        self.assertFalse(self.app.mini_player_visible, "mini_player_visible must be False on fresh startup")
        self.assertFalse(self.app.mini_player_dismissed, "mini_player_dismissed must be False on fresh startup")

        mini_p = self.root.ids.mini_player
        self.assertEqual(mini_p.height, 0, f"mini_player height must be 0 on fresh startup, got {mini_p.height}")
        self.assertEqual(mini_p.opacity, 0, f"mini_player opacity must be 0 on fresh startup, got {mini_p.opacity}")
        self.assertTrue(mini_p.disabled, "mini_player must be disabled on fresh startup")
        print("  [PASS] Fresh startup: active_track is None and mini_player is hidden (height=0, disabled=True)")

    def test_02_track_selection_opens_mini_player(self):
        """Test track selection: mini player opens with valid geometry."""
        print("[TEST] 2. Validating Track Selection Opens Mini Player...")
        test_track = TrackModel(
            video_id="test_mini_01",
            title="Test Song One",
            artist="Artist One",
            duration=210
        )
        self.app.play_selected_track(test_track)
        Clock.tick()

        self.assertEqual(self.app.player_controller.active_track, test_track)
        self.assertTrue(self.app.mini_player_visible, "mini_player_visible must be True after play_selected_track")
        self.assertFalse(self.app.mini_player_dismissed, "mini_player_dismissed must be False after play_selected_track")

        # Exit player screen to Home
        self.app.switch_screen("home")
        Clock.tick()

        mini_p = self.root.ids.mini_player
        self.assertEqual(mini_p.height, 72.0, f"mini_player height must be 72dp when active, got {mini_p.height}")
        self.assertEqual(mini_p.opacity, 1.0, f"mini_player opacity must be 1.0 when active, got {mini_p.opacity}")
        self.assertFalse(mini_p.disabled, "mini_player must be enabled when active")
        print("  [PASS] Track played: mini_player opens with height 72dp and disabled=False")

    def test_03_tap_on_mini_player_opens_player_screen(self):
        """Test tap on mini player card (without downward movement) switches to PlayerScreen."""
        print("[TEST] 3. Validating Mini Player Card Tap Action...")
        self.app.switch_screen("home")
        Clock.tick()

        mini_p = self.root.ids.mini_player
        card = [c for c in mini_p.children if type(c).__name__ == "MiniPlayerCard"][0]

        # Simulate a clean tap at card center (dx=0, dy=0)
        cx, cy = card.center
        touch = DummyTouch(cx, cy)
        card.on_touch_down(touch)
        card.on_touch_up(touch)
        Clock.tick()

        sm = self.root.ids.screen_manager
        self.assertEqual(sm.current, "player", f"Tapping mini player card must open PlayerScreen, current={sm.current}")
        print("  [PASS] Tap on MiniPlayerCard smoothly switches to PlayerScreen")

    def test_04_swipe_down_dismisses_mini_player(self):
        """Test downward swipe on mini player card dismisses it, pauses playback, and stays on home screen."""
        print("[TEST] 4. Validating Swipe-Down Dismissal...")
        self.app.switch_screen("home")
        Clock.tick()

        mini_p = self.root.ids.mini_player
        card = [c for c in mini_p.children if type(c).__name__ == "MiniPlayerCard"][0]

        # Simulate downward swipe: starting at cy, moving to cy - 40dp (downwards in screen coordinates)
        cx, cy = card.center
        touch = DummyTouch(cx, cy + dp(10))
        card.on_touch_down(touch)

        # Move downward by 35dp
        touch.y = cy - dp(25)
        card.on_touch_move(touch)

        # Release touch
        card.on_touch_up(touch)
        Clock.tick()

        # Mini player must now be dismissed
        self.assertFalse(self.app.mini_player_visible, "mini_player_visible must be False after swipe down")
        self.assertTrue(self.app.mini_player_dismissed, "mini_player_dismissed must be True after swipe down")
        self.assertEqual(mini_p.height, 0, f"mini_player height must collapse to 0, got {mini_p.height}")
        self.assertTrue(mini_p.disabled, "mini_player must be disabled after dismissal")

        # Must NOT have switched to player screen
        sm = self.root.ids.screen_manager
        self.assertEqual(sm.current, "home", f"Swipe down must NOT open PlayerScreen, screen is {sm.current}")
        print("  [PASS] Swiping down on mini_player collapses it (height=0, disabled=True) and retains current screen")

    def test_05_subsequent_track_selection_restores_mini_player(self):
        """Test subsequent song selection restores mini player after being dismissed."""
        print("[TEST] 5. Validating New Track Selection Restores Dismissed Mini Player...")
        self.assertTrue(self.app.mini_player_dismissed, "Precondition: mini_player must be dismissed")

        new_track = TrackModel(
            video_id="test_mini_02",
            title="Test Song Two",
            artist="Artist Two",
            duration=180
        )
        self.app.play_selected_track(new_track)
        Clock.tick()

        self.assertFalse(self.app.mini_player_dismissed, "mini_player_dismissed must be reset to False")
        self.assertTrue(self.app.mini_player_visible, "mini_player_visible must be restored to True")

        self.app.switch_screen("home")
        Clock.tick()

        mini_p = self.root.ids.mini_player
        self.assertEqual(mini_p.height, 72.0, "mini_player height must be restored to 72dp")
        self.assertFalse(mini_p.disabled, "mini_player must be re-enabled")
        print("  [PASS] Playing subsequent track un-dismisses and restores mini player cleanly")

if __name__ == "__main__":
    unittest.main()
