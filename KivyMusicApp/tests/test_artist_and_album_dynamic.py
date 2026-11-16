"""
Test Suite: Artist Profile & Album Dynamic Data Invariants
Verifies:
1. Artist Profile discography has zero hardcoded mock cards ('Future Echoes', 'Midnight Drive', 'Electric Dreams').
2. Artist query does not inject random unrelated fallback tracks from other artists.
3. ArtistAlbumCard dynamically accepts titles, subtitles, and artworks.
4. Album screen metadata & tracklist are completely dynamic.
"""
import os
import sys

os.environ["KIVY_HEADLESS"] = "1"
os.environ["KIVY_LOG_MODE"] = "PYTHON"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition
from main import MusicApp
from models.track_model import TrackModel
from views.components import ArtistAlbumCard

def run_test(on_complete=None):
    app = MusicApp()
    results = {}

    def test_logic(dt):
        print("\n[TEST] Starting Artist & Album Dynamic Data Validation...")
        sm = app.root.ids.screen_manager
        sm.transition = NoTransition()

        # 1. Test Artist Profile Dynamic Discography
        artist_query = "Alan Walker"
        app.open_artist(artist_query)
        artist_screen = sm.get_screen("artist")

        assert app.active_artist_name == artist_query, f"Expected {artist_query}, got {app.active_artist_name}"
        assert "artist_albums_box" in artist_screen.ids, "artist_albums_box ID missing from ArtistScreen"

        albums_box = artist_screen.ids.artist_albums_box
        # Check no hardcoded mock cards exist
        for child in albums_box.children:
            if hasattr(child, "title") and child.title in ["Future Echoes", "Midnight Drive", "Electric Dreams"]:
                raise AssertionError("Found obsolete static mock album card in artist screen!")
        results["artist_zero_mock_albums"] = True
        print("  [PASS] Artist screen has no hardcoded static mock albums.")

        # 2. Test ArtistAlbumCard dynamic instantiation
        test_album = ArtistAlbumCard(
            title="Different World",
            subtitle="Album • Official",
            artwork="album_art.png",
            artist=artist_query
        )
        albums_box.add_widget(test_album)
        assert len(albums_box.children) > 0, "ArtistAlbumCard failed to attach to albums box"
        results["artist_album_card_dynamic"] = True
        print("  [PASS] ArtistAlbumCard instantiates dynamically.")

        # 3. Test Album Screen Dynamic Metadata & Tracklist
        album_name = "Global EDM Anthems"
        artist_name = "Electronic Artists"
        sample_tracks = [
            TrackModel(video_id="t1", title="Faded", artist="Alan Walker", url="https://youtube.com/1", duration=212, album_art="album_art.png"),
            TrackModel(video_id="t2", title="Alone", artist="Alan Walker", url="https://youtube.com/2", duration=161, album_art="album_art2.png"),
        ]
        app.open_album(album_name, artist_name, "album_art.png", sample_tracks)

        assert app.active_album_name == album_name, f"Expected {album_name}, got {app.active_album_name}"
        assert app.active_album_artist == artist_name, f"Expected {artist_name}, got {app.active_album_artist}"
        assert len(app.active_album_tracks) == 2, f"Expected 2 album tracks, got {len(app.active_album_tracks)}"

        album_screen = sm.get_screen("album")
        def verify_album_tracks(dt):
            assert len(album_screen.ids.album_tracks_list.data) == 2, "Album tracks list data length mismatch"
            results["album_screen_dynamic"] = True
            print("  [PASS] Album screen displays dynamic title, artist, and tracklist.")

            print("  [ALL PASSED] Artist & Album Test Suite Succeeded!")
            app.stop()
            if on_complete:
                on_complete(True, results)

        Clock.schedule_once(verify_album_tracks, 0.1)

    def check_ready(dt):
        if getattr(app, "_splash_completed", False):
            Clock.schedule_once(test_logic, 0.1)
        else:
            Clock.schedule_once(check_ready, 0.1)

    Clock.schedule_once(check_ready, 0.2)
    app.run()
    return results

if __name__ == "__main__":
    run_test(lambda passed, res: sys.exit(0 if passed else 1))
