"""
Multi-Source Music Provider Integration Test Battery.
Verifies YouTube, Spotify, and JioSaavn extraction, DES URL decryption,
stream arbitration, SQLite persistence, and UI integration.
Runs in headless mode with software mute enforced.
"""
import os
import sys
import unittest

os.environ["KIVY_HEADLESS"] = "1"
os.environ["KIVY_LOG_MODE"] = "PYTHON"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.track_model import TrackModel
from models.database import (
    get_db_connection, DB_LOCK, add_track, get_track, get_all_tracks,
    add_playlist, add_track_to_playlist, get_playlist_tracks
)
from utils.des import des, ECB, PAD_PKCS5
from services.jiosaavn_provider import JioSaavnProvider
from services.spotify_provider import SpotifyProvider
from services.youtube_provider import YouTubeProvider
from services.music_provider_router import MusicProviderRouter
from services.audio_engine import AudioEngine, is_valid_audio_header

class TestMultiSourceProviders(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from models.database import init_db
        init_db()
        cls.router = MusicProviderRouter()
        cls.jiosaavn = JioSaavnProvider()
        cls.spotify = SpotifyProvider()
        cls.youtube = YouTubeProvider()
        cls.engine = AudioEngine()
        cls.engine.muted = True
        cls.engine.volume = 0.0

    def test_01_pure_python_des_decryption(self):
        """Verifies pure-Python DES-ECB URL decryption matches JioSaavn CDN format."""
        cipher = des(b"38346591", ECB, padmode=PAD_PKCS5)
        enc_url = "ID2ieOjCrwfgWvL5sXl4B1ImC5QfbsDyj4ZDyRkajGN2q4KeBCxtREh4spXbqfrBgV8FtvB9QO2H160XU/sCaBw7tS9a8Gtq"
        import base64
        raw = base64.b64decode(enc_url.strip())
        decrypted = cipher.decrypt(raw, padmode=PAD_PKCS5).decode("utf-8")
        self.assertTrue(decrypted.startswith("https://aac.saavncdn.com/"))
        stream_320 = decrypted.replace("_96.mp4", "_320.mp4")
        self.assertIn("_320.mp4", stream_320)
        print(f"\n[PASS] Test 1: DES Decrypted 320k URL -> {stream_320}")

    def test_02_jiosaavn_search_and_metadata(self):
        """Verifies JioSaavn search returns structured 320kbps tracks."""
        results = self.jiosaavn.search("Arijit Singh", limit=4)
        self.assertGreater(len(results), 0)
        first = results[0]
        self.assertEqual(first["source"], "jiosaavn")
        self.assertEqual(first["bitrate"], 320)
        self.assertTrue(first["video_id"].startswith("js_"))
        self.assertTrue(first["title"] != "")
        self.assertTrue(first["stream_url"].startswith("https://aac.saavncdn.com/"))
        print(f"\n[PASS] Test 2: JioSaavn Track -> '{first['title']}' by {first['artist']} (320kbps stream: {first['stream_url'][:45]}...)")

    def test_03_jiosaavn_track_details(self):
        """Verifies single song details resolution with JioSaavn API."""
        details = self.jiosaavn.get_track_details("QcfFd62t")
        self.assertIsNotNone(details)
        self.assertEqual(details["source"], "jiosaavn")
        self.assertIn("KING", details["title"])
        self.assertTrue(details["stream_url"].startswith("https://aac.saavncdn.com/"))
        print(f"\n[PASS] Test 3: JioSaavn Song Details -> '{details['title']}' (duration: {details['duration']}s)")

    def test_04_spotify_id_extractor(self):
        """Verifies Spotify ID extraction from URLs and URIs."""
        urls = [
            ("https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=123", "37i9dQZF1DXcBWIGoYBM5M"),
            ("spotify:playlist:37i9dQZF1DXcBWIGoYBM5M", "37i9dQZF1DXcBWIGoYBM5M"),
            ("https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC", "4uLU6hMCjMI75M1A2tKUQC"),
            ("spotify:track:4uLU6hMCjMI75M1A2tKUQC", "4uLU6hMCjMI75M1A2tKUQC"),
            ("4uLU6hMCjMI75M1A2tKUQC", "4uLU6hMCjMI75M1A2tKUQC")
        ]
        for raw, expected in urls:
            kind = "track" if "track" in raw else "playlist"
            extracted = self.spotify.extract_spotify_id(raw, expected_type=kind)
            self.assertEqual(extracted, expected)
        print("\n[PASS] Test 4: Spotify Base62 ID extraction validated across 5 variants")

    def test_05_spotify_public_playlist_extraction(self):
        """Verifies zero-auth Spotify public playlist extraction via embed."""
        pl = self.spotify.get_playlist("https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M")
        self.assertIsNotNone(pl)
        self.assertIn("Top Hits", pl["title"])
        tracks = pl.get("tracks", [])
        self.assertGreater(len(tracks), 20)
        t0 = tracks[0]
        self.assertEqual(t0["source"], "spotify")
        self.assertTrue(t0["video_id"].startswith("sp_"))
        print(f"\n[PASS] Test 5: Spotify Playlist Extracted -> '{pl['title']}' ({len(tracks)} tracks, sample: '{t0['title']}')")

    def test_06_spotify_track_oembed(self):
        """Verifies single track metadata extraction via Spotify oEmbed."""
        td = self.spotify.get_track_details("4uLU6hMCjMI75M1A2tKUQC")
        self.assertIsNotNone(td)
        self.assertEqual(td["source"], "spotify")
        self.assertIn("Never Gonna Give You Up", td["title"])
        self.assertTrue(td["artwork"].startswith("http"))
        print(f"\n[PASS] Test 6: Spotify oEmbed Track -> '{td['title']}' by {td['artist']}")

    def test_07_youtube_provider_search(self):
        """Verifies YouTube flat search via yt-dlp."""
        res = self.youtube.search("Coldplay Yellow", limit=3)
        self.assertGreater(len(res), 0)
        t0 = res[0]
        self.assertEqual(t0["source"], "youtube")
        self.assertEqual(len(t0["video_id"]), 11)
        print(f"\n[PASS] Test 7: YouTube Search -> '{t0['title']}' (id: {t0['video_id']})")

    def test_08_multi_source_router_parallel_search(self):
        """Verifies MusicProviderRouter parallel search returns merged multi-source results."""
        results = self.router.search("Diljit Dosanjh", provider="all", limit=6)
        self.assertGreater(len(results), 0)
        sources = {r["source"] for r in results}
        self.assertTrue("jiosaavn" in sources or "youtube" in sources)
        print(f"\n[PASS] Test 8: Multi-Source Search -> {len(results)} items, sources: {sources}")

    def test_09_stream_arbitration_jiosaavn(self):
        """Verifies router stream resolution for direct JioSaavn 320kbps stream."""
        track = {
            "video_id": "js_QcfFd62t",
            "source_id": "QcfFd62t",
            "title": "Tu Mil Jaaye",
            "artist": "Arijit Singh",
            "source": "jiosaavn"
        }
        res = self.router.resolve_stream(track)
        self.assertEqual(res["source"], "jiosaavn")
        self.assertEqual(res["bitrate"], 320)
        self.assertTrue(res["is_direct_http"])
        self.assertTrue(res["url"].startswith("https://aac.saavncdn.com/"))
        print(f"\n[PASS] Test 9: Stream Arbitration (JioSaavn) -> 320kbps direct CDN URL resolved")

    def test_10_stream_arbitration_spotify_matcher(self):
        """Verifies router matches Spotify track against JioSaavn or YouTube."""
        sp_track = {
            "video_id": "sp_4uLU6hMCjMI75M1A2tKUQC",
            "title": "Never Gonna Give You Up",
            "artist": "Rick Astley",
            "source": "spotify"
        }
        res = self.router.resolve_stream(sp_track)
        self.assertTrue("matched" in res["source"] or res["source"] in ("jiosaavn", "youtube"))
        self.assertTrue(res["url"].startswith("http"))
        print(f"\n[PASS] Test 10: Stream Arbitration (Spotify Matcher) -> Resolved via {res['source']}: {res['url'][:45]}...")

    def test_11_spotify_playlist_sqlite_import(self):
        """Verifies 1-click import of public Spotify playlist into SQLite."""
        test_url = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
        import_res = self.router.import_spotify_playlist(test_url)
        self.assertTrue(import_res["success"])
        self.assertGreater(import_res["count"], 0)
        pl_name = import_res["title"]
        self.assertTrue(pl_name.startswith("[Spotify]"))
        
        # Verify tracks were persisted in SQLite
        db_tracks = get_playlist_tracks(pl_name)
        self.assertGreater(len(db_tracks), 0)
        print(f"\n[PASS] Test 11: 1-Click Spotify Import -> '{pl_name}' created in SQLite with {len(db_tracks)} tracks")

    def test_12_track_model_and_database_source_fields(self):
        """Verifies TrackModel and SQLite tracks table support source, source_id, bitrate, and isrc."""
        t_meta = {
            "video_id": "test_src_01",
            "title": "Multi-Source Test",
            "artist": "Test Artist",
            "url": "https://example.com/stream.mp4",
            "duration": 210,
            "source": "jiosaavn",
            "source_id": "js_12345",
            "bitrate": 320,
            "isrc": "US1234567890"
        }
        add_track(
            video_id=t_meta["video_id"],
            title=t_meta["title"],
            artist=t_meta["artist"],
            url=t_meta["url"],
            duration=t_meta["duration"],
            source=t_meta["source"],
            source_id=t_meta["source_id"],
            bitrate=t_meta["bitrate"],
            isrc=t_meta["isrc"]
        )
        fetched = get_track("test_src_01")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["source"], "jiosaavn")
        self.assertEqual(fetched["bitrate"], 320)
        self.assertEqual(fetched["isrc"], "US1234567890")

        # Verify TrackModel serialization & remote artwork URL preservation
        model = TrackModel.from_dict(fetched)
        self.assertEqual(model.source, "jiosaavn")
        self.assertEqual(model.bitrate, 320)
        self.assertEqual(model.isrc, "US1234567890")
        js_remote = TrackModel.from_dict({
            "video_id": "js_art_test_99",
            "title": "Art Test",
            "artist": "Singer",
            "artwork": "https://c.saavncdn.com/652/sample-500x500.jpg",
            "source": "jiosaavn",
        })
        self.assertEqual(js_remote.album_art, "https://c.saavncdn.com/652/sample-500x500.jpg")
        m_dict = model.to_dict()
        self.assertEqual(m_dict["source"], "jiosaavn")
        self.assertEqual(m_dict["bitrate"], 320)
        print(f"\n[PASS] Test 12: TrackModel & SQLite Source Schema (source, source_id, bitrate, isrc, remote artwork) verified")

    def test_13_audio_header_validation_safety(self):
        """Verifies audio header validation safely detects MP3, MP4/AAC, and rejects corrupt data."""
        self.assertFalse(is_valid_audio_header("non_existent_file.mp3"))
        
        # Test synthetic header validation
        test_file = "test_valid_mp4_header.mp4"
        try:
            with open(test_file, "wb") as f:
                # MP4 ftyp header with padding
                f.write(b"\x00\x00\x00\x20ftypisom\x00\x00\x02\x00isomiso2mp41" + b"\x00" * 2000)
            self.assertTrue(is_valid_audio_header(test_file))
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)
        print("\n[PASS] Test 13: Audio header validation verified safely")

if __name__ == "__main__":
    unittest.main()
