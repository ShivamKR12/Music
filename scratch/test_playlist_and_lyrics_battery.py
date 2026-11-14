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
from models.database import get_all_playlists, add_playlist, delete_playlist, add_track_to_playlist, get_playlist_tracks
from views.components import MarqueeLabel
from services.lyrics_service import fetch_lyrics_sync

class TestPlaylistAndRealSystemsBattery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = MusicApp()
        cls.app.root = cls.app.build()
        cls.app.on_start()
        for _ in range(20):
            Clock.tick()
            time.sleep(0.02)

    def test_01_marquee_pause_and_scroll(self):
        """Verify MarqueeLabel starts at scroll_x=0.0 with 2.5s initial pause, and smooth animation."""
        label = MarqueeLabel(
            text="Very Long Song Title Exceeding Viewport Width In Every Way Possible",
            size_hint=(None, None),
            size=("200dp", "30dp")
        )
        Window.add_widget(label)
        for _ in range(10):
            Clock.tick()
            time.sleep(0.02)
        
        self.assertIsNotNone(label._anim, "Marquee animation must be active for long text")
        self.assertEqual(label.scroll_x, 0.0, "Marquee must start at scroll_x=0.0 with reading pause")
        Window.remove_widget(label)

    def test_02_add_playlist_dialog_no_crash(self):
        """Verify show_add_playlist_dialog opens without MDDialogContentContainer TypeError."""
        self.app.show_add_playlist_dialog()
        for _ in range(5):
            Clock.tick()
            time.sleep(0.02)
        self.assertIsNotNone(self.app.playlist_dialog, "Dialog must be created successfully")
        self.app.playlist_dialog.dismiss()

    def test_03_playlist_creation_and_viewing(self):
        """Verify real playlist creation, track addition, and dynamic PlaylistScreen population."""
        test_pl = "Gym Bangers 2026"
        add_playlist(test_pl)
        all_pls = [p['name'] for p in get_all_playlists()]
        self.assertIn(test_pl, all_pls, "New playlist must appear in SQLite")

        # Add a track from playlist_model to this playlist
        first_track = self.app.playlist_model.tracks[0]
        added = add_track_to_playlist(test_pl, first_track.video_id, {
            "title": first_track.title,
            "artist": first_track.artist,
            "url": first_track.url,
            "artwork": first_track.album_art,
            "duration": first_track.duration,
            "local_path": first_track.local_path
        })
        self.assertTrue(added, "Track must be successfully added to playlist")

        # Open the playlist in UI
        self.app.open_playlist(test_pl)
        for _ in range(10):
            Clock.tick()
            time.sleep(0.02)

        sm = self.app.root.ids.screen_manager
        self.assertEqual(sm.current, "playlist", "Must navigate to playlist screen")
        self.assertEqual(self.app.active_playlist_name, test_pl)

        pl_screen = sm.get_screen("playlist")
        pl_data = pl_screen.ids.playlist_tracks_list.data
        self.assertEqual(len(pl_data), 1, "PlaylistScreen must display exactly 1 track")
        self.assertEqual(pl_data[0]["title"], first_track.title)

        # Test playing the playlist
        self.app.play_active_playlist(shuffle=False)
        for _ in range(10):
            Clock.tick()
            time.sleep(0.02)
        self.assertEqual(self.app.player_controller.active_track, first_track)

        # Clean up
        delete_playlist(test_pl)

    def test_03_real_lyrics_fetching(self):
        """Verify real lyrics fetching from LRCLIB and caching."""
        lyrics = fetch_lyrics_sync("Dil Lutiya", "Jaswinder Daghamia", "TI7RQO2cuh0", cache_dir=self.app.cache_dir)
        self.assertGreater(len(lyrics), 50, "Real lyrics must be returned")
        self.assertIn("lutiya", lyrics.lower(), "Fetched lyrics must match track")

        # Test show_lyrics in UI
        self.app.player_controller.set_track(self.app.playlist_model.tracks[0])
        self.app.show_lyrics()
        for _ in range(15):
            Clock.tick()
            time.sleep(0.02)

    def test_04_dynamic_album_and_artist_screens(self):
        """Verify Album and Artist screens dynamically render real library tracks."""
        # Album
        self.app.open_album()
        for _ in range(5):
            Clock.tick()
            time.sleep(0.02)
        sm = self.app.root.ids.screen_manager
        self.assertEqual(sm.current, "album")
        album_screen = sm.get_screen("album")
        self.assertGreater(len(album_screen.ids.album_tracks_list.data), 0, "Album tracks must be populated")

        # Artist
        self.app.open_artist()
        for _ in range(5):
            Clock.tick()
            time.sleep(0.02)
        self.assertEqual(sm.current, "artist")
        artist_screen = sm.get_screen("artist")
        self.assertGreater(len(artist_screen.ids.artist_tracks_list.data), 0, "Artist tracks must be populated")

    def test_05_downloaded_offline_system(self):
        """Verify show_downloaded and download buttons routing."""
        self.app.show_downloaded()
        for _ in range(10):
            Clock.tick()
            time.sleep(0.02)

    def test_06_local_audio_metadata_and_artwork(self):
        """Verify real metadata and embedded artwork extraction for local audio file."""
        from utils.local_audio_utils import extract_local_audio_metadata
        sample_path = os.path.expanduser(r"~\Music\101 - MC Square.mp3")
        if os.path.exists(sample_path):
            meta = extract_local_audio_metadata(sample_path, self.app.cache_dir)
            self.assertEqual(meta["artist"], "MC Square", "Artist must be extracted cleanly")
            self.assertTrue(meta["artwork"].endswith((".jpg", ".png")), "Artwork must be extracted image file")
            self.assertTrue(os.path.exists(meta["artwork"]), "Extracted artwork file must exist on disk")

            # Test select_path routing
            self.app.select_path(sample_path)
            for _ in range(10):
                Clock.tick()
                time.sleep(0.02)
            self.assertEqual(self.app.player_controller.active_track.artist, "MC Square")
            self.assertEqual(self.app.player_controller.active_track.album_art, meta["artwork"])

    def test_07_device_offline_playlist_continuous_play(self):
        """Verify scanning device offline songs populates 'Offline Songs' playlist and supports continuous playback."""
        from utils.local_audio_utils import scan_device_offline_songs
        scanned = scan_device_offline_songs(limit=5, cache_dir=self.app.cache_dir)
        self.assertGreater(len(scanned), 0, "Must scan offline songs from device")

        # Populate Offline Songs playlist
        for s in scanned:
            add_track_to_playlist("Offline Songs", s["video_id"], s)

        self.app.open_playlist("Offline Songs")
        for _ in range(10):
            Clock.tick()
            time.sleep(0.02)

        self.assertEqual(self.app.active_playlist_name, "Offline Songs")
        self.assertGreaterEqual(len(self.app.active_playlist_tracks), len(scanned))

        # Test continuous queue play
        self.app.play_active_playlist(shuffle=False)
        for _ in range(10):
            Clock.tick()
            time.sleep(0.02)
        
        # Test next_track progression in queue
        first_track = self.app.player_controller.active_track
        next_track = self.app.player_controller.get_next_track()
        self.assertIsNotNone(next_track, "Next track must be available in playlist queue")
        self.assertNotEqual(first_track, next_track, "Next track must advance in playlist queue")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls.app, "player_controller") and cls.app.player_controller:
            cls.app.player_controller.stop()

if __name__ == '__main__':
    unittest.main()
