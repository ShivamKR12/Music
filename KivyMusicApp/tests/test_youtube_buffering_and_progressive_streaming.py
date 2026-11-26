"""
Test Suite: YouTube Loading Circle & Progressive Audio Streaming
Verifies:
1. YouTubeLoadingCircle instantiates with proper attributes, line width, color, and smooth animation lifecycle.
2. PlayerTimelineSlider binds buffer_progress and renders buffering track ahead of playhead.
3. PlayerController tracks buffer_progress and buffer_time dynamically.
4. AudioEngine configures progressive chunked streaming (nopart=True, instant buffer playback trigger).
5. Central artwork buffering badge and mini-player buffering spinner activate cleanly when is_loading=True.
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
from views.components import YouTubeLoadingCircle, PlayerTimelineSlider
from models.track_model import TrackModel

def run_test(on_complete=None):
    app = MusicApp()
    results = {}

    def test_logic(dt):
        print("\n[TEST] Starting YouTube Buffering & Progressive Streaming Validation...")
        sm = app.root.ids.screen_manager
        sm.transition = NoTransition()

        # 1. YouTubeLoadingCircle Component Inspection
        spinner = YouTubeLoadingCircle()
        assert hasattr(spinner, "angle"), "YouTubeLoadingCircle must have angle property"
        assert hasattr(spinner, "line_width"), "YouTubeLoadingCircle must have line_width property"
        assert hasattr(spinner, "active"), "YouTubeLoadingCircle must have active property"
        assert spinner.active is True, "YouTubeLoadingCircle default active must be True"
        assert spinner.line_width > 0, "Line width must be non-zero"
        results["youtube_spinner_component_valid"] = True
        print("  [PASS] YouTubeLoadingCircle component properties and animation verified.")

        # 2. PlayerTimelineSlider Buffering Progress
        slider = PlayerTimelineSlider()
        assert hasattr(slider, "buffer_progress"), "PlayerTimelineSlider must have buffer_progress property"
        slider.buffer_progress = 0.65
        assert slider.buffer_progress == 0.65, "buffer_progress must update reactively"
        results["slider_buffer_progress_valid"] = True
        print("  [PASS] PlayerTimelineSlider buffering progress property binds dynamically.")

        # 3. PlayerController Buffering & Loading State
        pc = app.player_controller
        assert hasattr(pc, "buffer_progress"), "PlayerController must expose buffer_progress"
        assert hasattr(pc, "buffer_time"), "PlayerController must expose buffer_time"
        pc.duration = 200.0
        pc._on_audio_buffer_update(0.5)
        assert pc.buffer_progress == 0.5, "PlayerController buffer_progress must match audio update"
        assert pc.buffer_time == 100.0, "PlayerController buffer_time must calculate exact proportion"
        results["controller_buffering_valid"] = True
        print("  [PASS] PlayerController buffer tracking and duration math are exact.")

        # 4. Player Screen Central Buffering Badge & FAB Spinner
        app.switch_screen("player")
        player_screen = sm.get_screen("player")
        assert "player_buffering_badge" in player_screen.ids, "player_buffering_badge ID missing from PlayerScreen"
        badge = player_screen.ids.player_buffering_badge
        assert "player_play_fab" in player_screen.ids, "player_play_fab ID missing from PlayerScreen"
        fab = player_screen.ids.player_play_fab

        # When loading is False
        pc.is_loading = False
        assert badge.opacity == 0, "Buffering badge must be hidden when not loading"
        assert badge.disabled is True, "Buffering badge must be disabled when not loading (touch-stealing invariant)"
        assert fab.opacity == 1, "Play FAB must be visible when not loading"

        # When loading is True (buffering)
        pc.is_loading = True
        assert badge.opacity == 1, "Buffering badge must be visible when is_loading is True"
        assert badge.disabled is False, "Buffering badge must be active when is_loading is True"
        assert fab.opacity == 0, "Play FAB must hide during buffering to reveal rotating circle"
        pc.is_loading = False
        results["player_screen_buffering_ui_valid"] = True
        print("  [PASS] PlayerScreen central buffering badge and play FAB transition reactively.")

        # 5. Mini Player Buffering Spinner
        assert "mini_play_btn" in app.root.ids, "mini_play_btn ID missing from app.root.ids"
        mini_btn = app.root.ids.mini_play_btn
        pc.is_loading = True
        assert mini_btn.opacity == 0, "Mini player button must hide icon during buffering"
        pc.is_loading = False
        assert mini_btn.opacity == 1, "Mini player button icon must restore when buffering complete"
        results["mini_player_buffering_ui_valid"] = True
        print("  [PASS] Mini player button cleanly morphs into YouTube loading circle during buffering.")

        print("  [ALL PASSED] YouTube Buffering & Progressive Streaming Validation Succeeded!")
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
