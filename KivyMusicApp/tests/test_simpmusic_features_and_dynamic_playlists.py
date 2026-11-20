"""
Automated Headless Test Suite for SimpMusic Key Features & Dynamic Playlists.
Validates:
1. AutoEq Database and Headphone Calibration Profiles
2. SponsorBlock API Segment Matching & Skipping Logic
3. Discord Rich Presence Graceful Cross-Platform Fallback
4. Enhanced Lyrics Engine (Timing Offset, Word Parsing, Romanization)
5. Dynamic Behavioral Playlists (On Repeat, Heavy Rotation, Forgotten Favorites, Daily Mix)
6. DJ-Style Audio Crossfade Configuration & SQLite Persistence
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Ensure app root is on path
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from services.autoeq_service import (
    get_all_autoeq_profiles,
    get_autoeq_profile_names,
    get_autoeq_curve,
    search_autoeq_profiles,
    EQ_FREQUENCIES
)
from services.sponsorblock_service import SponsorBlockService
from services.discord_rpc_service import DiscordRPCService
from services.lyrics_service import parse_lrc, parse_lrc_words, romanize_text
from models.database import (
    init_db,
    add_track,
    mark_track_played,
    get_on_repeat,
    get_heavy_rotation,
    get_forgotten_favorites,
    get_daily_mix,
    get_dynamic_playlist_tracks,
    get_setting,
    set_setting,
)

class TestSimpMusicFeaturesAndDynamicPlaylists(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    def test_01_autoeq_database_integrity(self):
        """Verifies AutoEq headphone profiles have 10 valid clamped bands across ISO frequencies."""
        profiles = get_all_autoeq_profiles()
        self.assertGreaterEqual(len(profiles), 10, "AutoEq database should contain at least 10 profiles")
        self.assertEqual(len(EQ_FREQUENCIES), 10)

        for name, curve in profiles.items():
            self.assertEqual(len(curve), 10, f"Profile '{name}' must have exactly 10 frequency bands")
            for gain in curve:
                self.assertTrue(-12.0 <= gain <= 12.0, f"Gain {gain} in '{name}' outside -12 to +12 dB limits")

        # Verify specific popular models exist
        self.assertIsNotNone(get_autoeq_curve("Sony WH-1000XM5"))
        self.assertIsNotNone(get_autoeq_curve("Apple AirPods Pro 2"))
        self.assertIsNotNone(get_autoeq_curve("Sennheiser HD 650"))
        self.assertIsNotNone(get_autoeq_curve("Harman In-Ear Target"))

        # Verify search
        sony_results = search_autoeq_profiles("Sony")
        self.assertGreaterEqual(len(sony_results), 2)
        print("  [PASS] AutoEq database loaded and all 10-band curves are strictly validated.")

    def test_02_sponsorblock_segment_matching(self):
        """Verifies SponsorBlock service detects non-music segments and returns skip target."""
        sb = SponsorBlockService()
        video_id = "test_vid_123"

        # Mock segment cache with music_offtopic and sponsor segments
        # [0.0s - 15.0s] intro, [120.0s - 135.0s] sponsor
        sb._cache[video_id] = [
            (0.0, 15.0, "intro"),
            (120.0, 135.0, "sponsor")
        ]

        # In the middle of intro -> should skip to 15.0s
        self.assertEqual(sb.get_skip_target(video_id, 5.0), 15.0)

        # In normal playback -> should return None
        self.assertIsNone(sb.get_skip_target(video_id, 45.0))

        # In sponsor block -> should skip to 135.0s
        self.assertEqual(sb.get_skip_target(video_id, 122.5), 135.0)

        # End of sponsor block -> should return None
        self.assertIsNone(sb.get_skip_target(video_id, 135.5))
        print("  [PASS] SponsorBlock segment evaluation and skip seeking verified.")

    def test_03_discord_rpc_cross_platform_safety(self):
        """Verifies Discord RPC service handles connection gracefully without crashing on any platform."""
        rpc = DiscordRPCService()
        self.assertIsNotNone(rpc)
        # Calling update_track or clear when not connected must succeed safely
        rpc.update_track("Song Title", "Artist", 10.0, 180.0, True)
        rpc.clear()
        rpc.close()
        print("  [PASS] Discord RPC service initialized and executed with safe non-blocking fallback.")

    def test_04_enhanced_lyrics_timing_and_words(self):
        """Verifies LRC timing offset adjustment and word-level tokenization."""
        lrc_sample = (
            "[00:10.00]First line of song\n"
            "[00:20.50]Second line of song"
        )

        # Standard parsing
        parsed = parse_lrc(lrc_sample, timing_offset=0.0)
        self.assertEqual(len(parsed), 2)
        self.assertAlmostEqual(parsed[0][0], 10.0)
        self.assertAlmostEqual(parsed[1][0], 20.5)

        # Positive offset (+0.5s)
        parsed_plus = parse_lrc(lrc_sample, timing_offset=0.5)
        self.assertAlmostEqual(parsed_plus[0][0], 10.5)
        self.assertAlmostEqual(parsed_plus[1][0], 21.0)

        # Negative offset (-1.0s)
        parsed_minus = parse_lrc(lrc_sample, timing_offset=-1.0)
        self.assertAlmostEqual(parsed_minus[0][0], 9.0)
        self.assertAlmostEqual(parsed_minus[1][0], 19.5)

        # Word-level parsing
        words_data = parse_lrc_words(lrc_sample)
        self.assertEqual(len(words_data), 2)
        self.assertEqual(words_data[0]["text"], "First line of song")

        # Romanization helper
        accented = "Café Müller & Señorita"
        romanized = romanize_text(accented)
        self.assertEqual(romanized, "Cafe Muller & Senorita")
        print("  [PASS] Enhanced lyrics timing offset, word extraction, and romanization verified.")

    def test_05_dynamic_playlists_and_play_count(self):
        """Verifies user play count tracking and behavioral dynamic playlist aggregation."""
        test_vid = "dyn_track_99"
        add_track(
            video_id=test_vid,
            title="Dynamic Behavioral Song",
            artist="Dynamic Artist",
            url="https://youtube.com/watch?v=dyn_track_99",
            duration=210,
            artwork="album_art.png"
        )

        # Increment play count twice
        mark_track_played(test_vid)
        mark_track_played(test_vid)

        # The shared dev DB accumulates real play counts from usage and older battery
        # runs (top tracks can reach 25+); push the fixture track decisively above the
        # crowd so the top-N ranking assertions below stay stable.
        for _ in range(100):
            mark_track_played(test_vid)

        # Check On Repeat
        on_repeat = get_on_repeat(limit=10)
        self.assertIsInstance(on_repeat, list)
        self.assertTrue(any(t["video_id"] == test_vid for t in on_repeat))

        # Check Heavy Rotation
        heavy = get_heavy_rotation(limit=10)
        self.assertIsInstance(heavy, list)
        self.assertTrue(any(t["video_id"] == test_vid for t in heavy))

        # Check Dynamic Routing
        routed_repeat = get_dynamic_playlist_tracks("On Repeat")
        self.assertIsNotNone(routed_repeat)
        self.assertTrue(len(routed_repeat) > 0)

        routed_daily = get_dynamic_playlist_tracks("Your Daily Mix")
        self.assertIsNotNone(routed_daily)
        print("  [PASS] Play count tracking and dynamic behavioral playlists verified.")

    def test_06_crossfade_persistence(self):
        """Verifies crossfade duration setting persistence."""
        set_setting("crossfade_duration", "5")
        saved = get_setting("crossfade_duration")
        self.assertEqual(str(saved), "5")

        set_setting("crossfade_duration", "0")
        saved_zero = get_setting("crossfade_duration")
        self.assertEqual(str(saved_zero), "0")
        print("  [PASS] Audio crossfade duration setting persisted and restored successfully.")


if __name__ == "__main__":
    print("=" * 65)
    print("[TEST] Running SimpMusic Key Features & Dynamic Playlists Suite...")
    print("=" * 65)
    unittest.main()
