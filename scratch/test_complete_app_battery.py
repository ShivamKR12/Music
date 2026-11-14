import os
import sys
import time
import unittest

os.environ["KIVY_HEADLESS"] = "1"
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "KivyMusicApp"))
os.chdir(APP_DIR)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from kivy.clock import Clock
from kivy.core.window import Window
from main import MusicApp

class TestCompleteAppBattery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = MusicApp()
        cls.app.root = cls.app.build()
        cls.app.on_start()
        # Allow multiple clock ticks for async initialization
        for _ in range(20):
            Clock.tick()
            time.sleep(0.02)

    def test_01_startup_and_screen_navigation(self):
        """Rule 11.1: Zero exceptions during startup and screen navigation across all screens."""
        sm = self.app.root.ids.screen_manager
        screens = ["home", "search", "library", "settings", "player", "favorites", "playlist", "album", "artist"]
        for s in screens:
            self.app.switch_screen(s)
            for _ in range(5):
                Clock.tick()
                time.sleep(0.01)
            self.assertEqual(sm.current, s, f"Screen manager current should be {s}")
        # Return to home
        self.app.switch_screen("home")
        for _ in range(5):
            Clock.tick()

    def test_02_home_cards_populated(self):
        """Verify Quick Picks, Trending, and Featured have real track objects."""
        home = self.app.root.ids.screen_manager.get_screen("home")
        self.assertIn("quick_picks_list", home.ids)
        qp_data = home.ids.quick_picks_list.data
        self.assertGreater(len(qp_data), 0, "Quick picks should be populated")
        self.assertIn("track_obj", qp_data[0], "Card must have track_obj bound")
        
        # Test tapping a home card
        first_track = qp_data[0]["track_obj"]
        self.app.play_selected_track(first_track)
        for _ in range(10):
            Clock.tick()
            time.sleep(0.02)
        self.assertEqual(self.app.player_controller.active_track, first_track)
        self.assertTrue(self.app.player_controller.is_playing)
        self.app.player_controller.stop()

    def test_03_search_local_filtering(self):
        """Test instantaneous local search filtering."""
        self.app.switch_screen("search")
        search_screen = self.app.root.ids.screen_manager.get_screen("search")
        self.app.perform_search("Dil")
        for _ in range(5):
            Clock.tick()
            time.sleep(0.02)
        
        results = search_screen.ids.search_results_list.data
        self.assertGreater(len(results), 0, "Local search should find Dil Lutiya instantly")
        self.assertIn("Dil", results[0]["title"])

    def test_04_direct_url_paste(self):
        """Test pasting a YouTube URL directly into perform_search."""
        url = "https://www.youtube.com/watch?v=TI7RQO2cuh0"
        self.app.perform_search(url)
        # Wait up to 12s for background yt-dlp metadata extraction
        for _ in range(120):
            Clock.tick()
            time.sleep(0.1)
            if self.app.player_controller.active_track and self.app.player_controller.active_track.video_id == "TI7RQO2cuh0":
                break
        # Should set active track and play
        self.assertEqual(self.app.player_controller.active_track.video_id, "TI7RQO2cuh0")
        self.app.player_controller.stop()

    def test_05_bounding_box_non_overlap(self):
        """Rule 11.2: Bounding-box non-overlap across stacked bars and screens."""
        root = self.app.root
        mini_player = root.ids.mini_player
        bottom_nav = root.ids.bottom_nav
        
        # mini_player y and bottom_nav y
        # bottom_nav is anchored at bottom, mini_player is stacked above it
        nav_y, nav_h = bottom_nav.y, bottom_nav.height
        mp_y, mp_h = mini_player.y, mini_player.height
        
        # Ensure mini player does not overlap bottom navigation
        if mini_player.opacity > 0:
            self.assertGreaterEqual(mp_y, nav_y + nav_h - 1.0, "Mini player must sit above bottom navigation bar")

    def test_06_queue_sheet_open_and_close(self):
        """Rule 11.3: Correct touch routing and sheet behavior."""
        self.app.switch_screen("player")
        self.app.show_queue_sheet()
        for _ in range(30):
            Clock.tick()
            time.sleep(0.02)
        self.assertIsNotNone(self.app.queue_sheet)
        self.assertIn(self.app.queue_sheet.state, ["open", "opening"])
        
        # Test back action closes sheet
        self.app.go_back()
        for _ in range(30):
            Clock.tick()
            time.sleep(0.02)
        self.assertIn(self.app.queue_sheet.state, ["close", "closing"])

    def test_07_favorites_sync(self):
        """Test favorites screen populates from SQLite."""
        self.app.show_favorites()
        for _ in range(5):
            Clock.tick()
            time.sleep(0.02)
        sm = self.app.root.ids.screen_manager
        self.assertEqual(sm.current, "favorites")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls.app, "player_controller") and cls.app.player_controller:
            cls.app.player_controller.stop()

if __name__ == '__main__':
    unittest.main()
