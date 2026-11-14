import os
import sys
import unittest

# Headless mode for Kivy
os.environ["KIVY_HEADLESS"] = "1"

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "KivyMusicApp"))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from kivy.clock import Clock
from models.database import init_db, add_track, get_all_tracks, get_continue_listening
from models.track_model import TrackModel, PlaylistModel
from controllers.player_controller import PlayerController
from services.logger import init_logging, app_logger
from utils.media_utils import extract_video_id, fetch_youtube_metadata

class TestMainIntegrationScratch(unittest.TestCase):
    def setUp(self):
        init_logging()
        init_db()
        self.playlist_model = PlaylistModel()
        self.player_controller = PlayerController()
        self.player_controller.set_playlist(self.playlist_model)

    def test_local_search_filtering(self):
        q = "Honey"
        matches = [
            t for t in self.playlist_model.tracks
            if q.lower() in t.title.lower() or q.lower() in t.artist.lower()
        ]
        self.assertGreater(len(matches), 0)
        self.assertIn("Honey", matches[0].artist)

    def test_home_screen_data_mapping(self):
        recent = get_continue_listening(limit=8)
        quick_picks_tracks = []
        if recent:
            for row in recent:
                vid = row.get("video_id")
                t = self.playlist_model.find_track(vid)
                if t and t not in quick_picks_tracks:
                    quick_picks_tracks.append(t)
        for t in self.playlist_model.tracks:
            if t not in quick_picks_tracks:
                quick_picks_tracks.append(t)

        self.assertGreater(len(quick_picks_tracks), 0)
        qp_data = [{"text": t.title, "track_obj": t} for t in quick_picks_tracks]
        self.assertIsInstance(qp_data[0]["track_obj"], TrackModel)

    def test_cached_track_play(self):
        ti = self.playlist_model.find_track("TI7RQO2cuh0")
        if ti:
            self.player_controller.set_track(ti)
            self.player_controller.play()
            self.assertTrue(self.player_controller.is_playing)
            self.player_controller.stop()

if __name__ == '__main__':
    unittest.main()
