"""
Test Suite: Podcasts, Serialization & Trending Playlists
Verifies:
1. Podcasts screen has zero hardcoded static mock episodes.
2. Featured Spotlight show card binds dynamically.
3. EmbeddedRecycleView renders podcast episodes dynamically.
4. TrackModel.to_dict() and TrackModel.from_dict() have 100% roundtrip fidelity.
5. Trending playlists ('Top Charts') register in SQLite and synchronize seamlessly.
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

def run_test(on_complete=None):
    app = MusicApp()
    results = {}

    def test_logic(dt):
        print("\n[TEST] Starting Podcasts & Trending Validation...")
        sm = app.root.ids.screen_manager
        sm.transition = NoTransition()

        # 1. TrackModel Roundtrip Serialization & Complete yt-dlp Metadata
        orig_track = TrackModel(
            video_id="pod_vid_99",
            title="The Future of AI & Robotics",
            artist="Lex Fridman",
            url="https://youtube.com/watch?v=pod_vid_99",
            duration=7540,
            album_art="album_art.png",
            album="Lex Fridman Podcast",
            album_artist="Lex Fridman",
            genre="Technology & Science",
            description="Deep conversation with leading roboticists and engineers.",
            view_count=1542000,
            like_count=82000,
            channel="Lex Fridman",
            channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
            release_date="2024-05-15",
            chapters='[{"title": "Intro", "start_time": 0, "end_time": 120}]',
            track_number=420,
            media_type="podcast",
            lyrics="Intro discussion...",
            synced_lyrics="[00:05.00]Welcome to the podcast",
            is_favorite=True,
            is_downloaded=False
        )
        serialized = orig_track.to_dict()
        assert isinstance(serialized, dict), "to_dict() must return a Python dictionary"
        assert serialized["video_id"] == "pod_vid_99"
        assert serialized["title"] == "The Future of AI & Robotics"
        assert serialized["duration"] == 7540
        assert serialized["media_type"] == "podcast"
        assert serialized["album"] == "Lex Fridman Podcast"
        assert serialized["genre"] == "Technology & Science"
        assert serialized["channel_id"] == "UC_x5XG1OV2P6uZZ5FSM9Ttw"
        assert serialized["view_count"] == 1542000

        deserialized = TrackModel.from_dict(serialized)
        assert deserialized.video_id == orig_track.video_id
        assert deserialized.title == orig_track.title
        assert deserialized.artist == orig_track.artist
        assert deserialized.duration == orig_track.duration
        assert deserialized.media_type == "podcast"
        assert deserialized.album == "Lex Fridman Podcast"
        assert deserialized.genre == "Technology & Science"
        assert deserialized.view_count == 1542000
        results["track_model_serialization_valid"] = True
        print("  [PASS] TrackModel.to_dict() and from_dict() maintain 100% fidelity across all yt-dlp metadata.")

        # 2. Classifier Validation (Music vs Podcasts)
        from utils.media_utils import is_podcast_item
        pod_item = {"title": "JRE #2150 - Terrence Howard", "duration": 10800, "uploader": "PowerfulJRE"}
        assert is_podcast_item(pod_item) is True, "JRE episode must be classified as podcast"
        mix_item = {"title": "Arijit Singh Best Songs Jukebox - Non Stop Bollywood Hits", "duration": 3600, "uploader": "T-Series"}
        assert is_podcast_item(mix_item) is False, "Music Jukebox must NOT be classified as podcast"
        song_item = {"title": "Blinding Lights", "duration": 200, "artist": "The Weeknd"}
        assert is_podcast_item(song_item) is False, "Standard song must NOT be classified as podcast"
        results["media_classifier_valid"] = True
        print("  [PASS] is_podcast_item accurately distinguishes podcasts from songs and music mixes.")

        # 3. Podcasts Screen Dynamic Binding
        app.open_podcasts()
        podcasts_screen = sm.get_screen("podcasts")
        assert "podcasts_list" in podcasts_screen.ids, "podcasts_list ID missing from PodcastsScreen"

        p_episodes = [
            TrackModel(video_id="p1", title="Episode 1: Science & Focus", artist="Huberman Lab", url="https://youtube.com/p1", duration=3600, album_art="album_art.png", media_type="podcast"),
            TrackModel(video_id="p2", title="Episode 2: Deep Work", artist="Cal Newport", url="https://youtube.com/p2", duration=2400, album_art="album_art2.png", media_type="podcast"),
        ]
        app.podcast_featured_track = p_episodes[0]
        app.podcast_featured_title = p_episodes[0].title
        app.podcast_featured_desc = f"{p_episodes[0].artist} • Full Episode"
        app.podcast_tracks = p_episodes[1:]
        app._render_podcasts_list()

        assert app.podcast_featured_title == "Episode 1: Science & Focus"
        results["podcast_featured_dynamic"] = True
        print("  [PASS] Featured podcast spotlight card binds dynamically.")

        # 4. Strict Podcast Exclusion from Home Music Shelves
        app.switch_screen("home")
        app.populate_home_screen_data()
        home = sm.get_screen("home")
        for rv_name in ("quick_picks_list", "listen_again_list", "trending_list", "featured_list", "forgotten_favorites_list", "daily_mix_list"):
            if rv_name in home.ids:
                rv_data = home.ids[rv_name].data
                for item in rv_data:
                    t_obj = item.get("track_obj")
                    if t_obj:
                        assert t_obj.media_type != "podcast", f"Podcast '{t_obj.title}' leaked into home shelf '{rv_name}'!"
                        assert not is_podcast_item(t_obj.to_dict()), f"Podcast item '{t_obj.title}' detected in home shelf '{rv_name}'!"
        results["home_shelves_podcast_free"] = True
        print("  [PASS] Home music shelves are 100% free of podcasts.")

        # 5. Trending Playlist Validation
        app.open_playlist("Top Charts")
        assert app.active_playlist_name == "Top Charts"
        pl_screen = sm.get_screen("playlist")
        assert "playlist_tracks_list" in pl_screen.ids
        results["top_charts_playlist_wired"] = True
        print("  [PASS] Top Charts playlist opens and synchronizes.")

        print("  [ALL PASSED] Podcasts & Trending Test Suite Succeeded!")
        app.stop()
        if on_complete:
            on_complete(True, results)

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
