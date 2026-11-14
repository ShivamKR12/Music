import os
import sys
import unittest

# Add KivyMusicApp to sys.path
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "KivyMusicApp"))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from utils.media_utils import (
    sanitize_text,
    format_time,
    get_cache_dir,
    extract_video_id,
    get_thumbnail_path,
    enforce_max_cache_size,
)
from services.logger import app_logger, init_logging
from models.database import (
    init_db,
    add_track,
    get_all_tracks,
    get_continue_listening,
    get_recently_added,
    is_favorite,
    toggle_favorite,
    add_search_history,
    get_search_history,
    clear_search_history,
)
from models.track_model import TrackModel, PlaylistModel
from controllers.player_controller import PlayerController

class TestBackendFullFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["KIVY_HEADLESS"] = "1"
        init_logging()

    def test_01_logger(self):
        app_logger.info("Test logging message from scratch script")
        self.assertTrue(True)

    def test_02_url_extraction(self):
        url1 = "https://www.youtube.com/watch?v=TI7RQO2cuh0"
        url2 = "https://youtu.be/TI7RQO2cuh0?si=abcdef"
        id1 = extract_video_id(url1)
        id2 = extract_video_id(url2)
        self.assertEqual(id1, "TI7RQO2cuh0")
        self.assertEqual(id2, "TI7RQO2cuh0")

    def test_03_database_and_playlist_model(self):
        init_db()
        playlist = PlaylistModel()
        self.assertGreater(len(playlist.tracks), 0)
        
        # Check if TI7RQO2cuh0 is recognized
        ti_track = playlist.find_track("TI7RQO2cuh0")
        if ti_track:
            self.assertTrue(ti_track.is_downloaded)
            self.assertTrue(os.path.exists(ti_track.local_path))
            print(f"Verified cached track: {ti_track.title} at {ti_track.local_path}")

    def test_04_player_controller_queue_and_playback(self):
        playlist = PlaylistModel()
        controller = PlayerController()
        controller.set_playlist(playlist)
        
        # Test repeat modes
        m1 = controller.cycle_repeat_mode()
        self.assertEqual(m1, "all")
        m2 = controller.cycle_repeat_mode()
        self.assertEqual(m2, "one")
        m3 = controller.cycle_repeat_mode()
        self.assertEqual(m3, "off")

        # Test queue navigation
        ti_track = playlist.find_track("TI7RQO2cuh0")
        if ti_track:
            controller.set_track(ti_track)
            self.assertEqual(controller.active_track, ti_track)
            controller.play()
            self.assertTrue(controller.is_playing)
            controller.toggle_play()
            self.assertFalse(controller.is_playing)
            controller.stop()

if __name__ == '__main__':
    unittest.main()
