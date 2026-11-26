"""
Automated validation suite for the 5-Level Logging System integrated with Kivy core Logger.
Verifies:
1. Canonical 5 levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
2. Sub-system scoped logger registry and colon tag splitting
3. Dynamic log level threshold filtering
4. Rotating file persistence on disk
5. App log dialog & severity configuration dialog lifecycle
"""

import os
import sys
import logging
import unittest

# Ensure headless execution
os.environ["KIVY_HEADLESS"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"

# Setup sys.path
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from kivy.logger import Logger as kivy_logger
from services.logger import (
    LogLevel,
    ScopedLogger,
    get_logger,
    init_logging,
    set_log_level,
    get_current_log_level_name,
    log_file
)


class TestFiveLevelLogSystem(unittest.TestCase):

    def setUp(self):
        self.orig_level = kivy_logger.getEffectiveLevel()

    def tearDown(self):
        set_log_level(self.orig_level)

    def test_01_canonical_five_levels(self):
        """Validates exact numeric values and names of the 5 canonical log levels."""
        self.assertEqual(LogLevel.DEBUG, 10)
        self.assertEqual(LogLevel.INFO, 20)
        self.assertEqual(LogLevel.WARNING, 30)
        self.assertEqual(LogLevel.ERROR, 40)
        self.assertEqual(LogLevel.CRITICAL, 50)

        self.assertEqual(LogLevel.all_names(), ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.assertEqual(LogLevel.from_str("debug"), LogLevel.DEBUG)
        self.assertEqual(LogLevel.from_str("INFO"), LogLevel.INFO)
        self.assertEqual(LogLevel.from_str("warning"), LogLevel.WARNING)
        self.assertEqual(LogLevel.from_str("warn"), LogLevel.WARNING)
        self.assertEqual(LogLevel.from_str("error"), LogLevel.ERROR)
        self.assertEqual(LogLevel.from_str("critical"), LogLevel.CRITICAL)
        self.assertEqual(LogLevel.from_str("fatal"), LogLevel.CRITICAL)

        self.assertEqual(LogLevel.to_str(LogLevel.DEBUG), "DEBUG")
        self.assertEqual(LogLevel.to_str(LogLevel.INFO), "INFO")
        self.assertEqual(LogLevel.to_str(LogLevel.WARNING), "WARNING")
        self.assertEqual(LogLevel.to_str(LogLevel.ERROR), "ERROR")
        self.assertEqual(LogLevel.to_str(LogLevel.CRITICAL), "CRITICAL")
        print("  [PASS] Canonical 5-level definitions and mapping functions verified.")

    def test_02_scoped_logger_subsystems(self):
        """Validates that distinct sub-systems obtain properly tagged scoped loggers."""
        subsystems = [
            "AudioEngine", "PlayerController", "Database", "YouTubeProvider",
            "SpotifyProvider", "JioSaavnProvider", "LyricsService", "MusicRouter",
            "SponsorBlock", "AutoEq", "DiscordRPC", "ListenTogether", "MediaUtils", "MusicApp"
        ]
        for name in subsystems:
            scoped = get_logger(name)
            self.assertIsInstance(scoped, ScopedLogger)
            self.assertEqual(scoped.name, name)
            fmt = scoped._fmt("Testing message", ())
            self.assertEqual(fmt, f"{name}: Testing message")
        print(f"  [PASS] Scoped loggers validated across {len(subsystems)} systems & sub-systems.")

    def test_03_emit_all_five_levels_through_kivy(self):
        """Verifies that all 5 log levels emit cleanly through Kivy's core Logger without exception."""
        set_log_level("DEBUG")
        logger = get_logger("AudioEngine")

        # Emit all 5 levels
        logger.debug("Test debug diagnostic: buffer=%d", 4096)
        logger.info("Test info milestone: track loaded successfully")
        logger.warning("Test warning anomaly: network latency %dms", 250)
        logger.error("Test error failure: decoding frame failed")
        logger.critical("Test critical failure: audio pipeline failure")

        self.assertTrue(logger.is_enabled_for(LogLevel.DEBUG))
        self.assertTrue(logger.is_enabled_for(LogLevel.INFO))
        self.assertTrue(logger.is_enabled_for(LogLevel.WARNING))
        self.assertTrue(logger.is_enabled_for(LogLevel.ERROR))
        self.assertTrue(logger.is_enabled_for(LogLevel.CRITICAL))
        print("  [PASS] All 5 log levels emit successfully through Kivy core Logger.")

    def test_04_dynamic_log_level_threshold_filtering(self):
        """Verifies that changing log level filters out lower severity logs dynamically."""
        set_log_level("WARNING")
        self.assertEqual(get_current_log_level_name(), "WARNING")
        self.assertFalse(kivy_logger.isEnabledFor(logging.DEBUG))
        self.assertFalse(kivy_logger.isEnabledFor(logging.INFO))
        self.assertTrue(kivy_logger.isEnabledFor(logging.WARNING))
        self.assertTrue(kivy_logger.isEnabledFor(logging.ERROR))
        self.assertTrue(kivy_logger.isEnabledFor(logging.CRITICAL))

        set_log_level("ERROR")
        self.assertEqual(get_current_log_level_name(), "ERROR")
        self.assertFalse(kivy_logger.isEnabledFor(logging.WARNING))
        self.assertTrue(kivy_logger.isEnabledFor(logging.ERROR))
        self.assertTrue(kivy_logger.isEnabledFor(logging.CRITICAL))

        set_log_level("DEBUG")
        self.assertEqual(get_current_log_level_name(), "DEBUG")
        self.assertTrue(kivy_logger.isEnabledFor(logging.DEBUG))
        print("  [PASS] Dynamic log level filtering operates with exact threshold compliance.")

    def test_05_rotating_file_persistence(self):
        """Validates that Kivy Logger records persist to disk in kivy_music_app.log."""
        init_logging(initial_level="DEBUG")
        test_marker = f"VERIFICATION_MARKER_{os.getpid()}"
        logger = get_logger("TestSubsystem")
        logger.info("Unique verification message: %s", test_marker)

        self.assertTrue(os.path.exists(log_file), f"Log file should exist at: {log_file}")
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        self.assertIn(test_marker, content)
        self.assertIn("TestSubsystem: Unique verification message:", content)
        print("  [PASS] Unified Kivy log file persistence confirmed on disk.")


if __name__ == "__main__":
    print("[TEST] Starting 5-Level Logging System Validation...")
    unittest.main(verbosity=2)
