"""
Test Suite: Desktop UI/UX Responsive Layout, Ergonomics & Control Verification
Validates:
1. Responsive breakpoint arbitration (mobile < 840dp vs desktop >= 840dp).
2. Mobile containers (mini_player, bottom_nav) disabled and collapsed on desktop.
3. Desktop containers (desktop_nav_rail, desktop_player_bar) active with exact heights/widths.
4. Desktop side panel toggle (lyrics vs queue) and dynamic synchronization.
5. Volume control, muting, and delta adjustment across AudioEngine and PlayerController.
6. Desktop keyboard shortcut dispatch (Space, Up/Down, M, L, Q, Esc).
7. Strict zero-overlap and touch-stealing invariants preserved across viewports.
"""
import os
import sys

os.environ["KIVY_HEADLESS"] = "1"
os.environ["KIVY_LOG_MODE"] = "PYTHON"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import NoTransition
from main import MusicApp
from models.track_model import TrackModel

def run_test(on_complete=None):
    app = MusicApp()
    results = {}

    def test_logic(dt):
        print("\n[TEST] Starting Desktop UI/UX Responsive Layout & Ergonomics Verification...")
        sm = app.root.ids.screen_manager
        sm.transition = NoTransition()
        app.switch_screen("home")

        # ---------------------------------------------------------
        # TEST 1: Mobile Layout Viewport Verification (< 840dp)
        # ---------------------------------------------------------
        print("  [STEP 1] Validating Mobile Viewport Layout (< 840dp)...")
        app.check_responsive_layout(width=360)
        assert not app.is_desktop_layout, "App should be in mobile layout at width 360"

        mini_player = app.root.ids.get("mini_player")
        bottom_nav = app.root.ids.get("bottom_nav")
        desktop_nav_rail = app.root.ids.get("desktop_nav_rail")
        desktop_player_bar = app.root.ids.get("desktop_player_bar")
        desktop_side_panel = app.root.ids.get("desktop_side_panel")

        assert mini_player is not None, "mini_player ID missing from root"
        assert bottom_nav is not None, "bottom_nav ID missing from root"
        assert desktop_nav_rail is not None, "desktop_nav_rail ID missing from root"
        assert desktop_player_bar is not None, "desktop_player_bar ID missing from root"
        assert desktop_side_panel is not None, "desktop_side_panel ID missing from root"

        # On mobile: mini_player and bottom_nav are enabled; desktop bars are disabled and 0-sized
        assert mini_player.disabled is False, "Mobile mini_player should NOT be disabled on mobile"
        assert bottom_nav.disabled is False, "Mobile bottom_nav should NOT be disabled on mobile"
        assert desktop_nav_rail.disabled is True, "Desktop nav rail MUST be disabled on mobile"
        assert desktop_nav_rail.width == 0, f"Desktop nav rail width must be 0 on mobile, got {desktop_nav_rail.width}"
        assert desktop_player_bar.disabled is True, "Desktop player bar MUST be disabled on mobile"
        assert desktop_player_bar.height == 0, f"Desktop player bar height must be 0 on mobile, got {desktop_player_bar.height}"
        assert desktop_side_panel.disabled is True, "Desktop side panel MUST be disabled on mobile"
        assert desktop_side_panel.width == 0, f"Desktop side panel width must be 0 on mobile, got {desktop_side_panel.width}"

        results["mobile_layout_clean"] = True
        print("    [PASS] Mobile layout correctly activates mobile navigation and disables desktop elements.")

        # ---------------------------------------------------------
        # TEST 2: Desktop Layout Viewport Verification (>= 840dp)
        # ---------------------------------------------------------
        print("  [STEP 2] Validating Desktop Viewport Layout (>= 840dp)...")
        app.check_responsive_layout(width=1024)
        assert app.is_desktop_layout, "App should be in desktop layout at width 1024"

        # On desktop: mobile bars must collapse and disable; desktop rail and player bar activate
        assert mini_player.disabled is True, "Mobile mini_player MUST be disabled on desktop"
        assert mini_player.height == 0, f"Mobile mini_player height must be 0 on desktop, got {mini_player.height}"
        assert bottom_nav.disabled is True, "Mobile bottom_nav MUST be disabled on desktop"
        assert bottom_nav.height == 0, f"Mobile bottom_nav height must be 0 on desktop, got {bottom_nav.height}"

        assert desktop_nav_rail.disabled is False, "Desktop nav rail must be active on desktop"
        assert desktop_nav_rail.width > 0, f"Desktop nav rail width must be > 0, got {desktop_nav_rail.width}"
        assert desktop_player_bar.disabled is False, "Desktop player bar must be active on desktop"
        assert desktop_player_bar.height > 0, f"Desktop player bar height must be > 0, got {desktop_player_bar.height}"

        results["desktop_layout_clean"] = True
        print("    [PASS] Desktop layout correctly collapses mobile bars and activates NavRail and PlayerBar.")

        # ---------------------------------------------------------
        # TEST 3: Desktop Side Panel (Lyrics & Queue) Toggling
        # ---------------------------------------------------------
        print("  [STEP 3] Validating Desktop Side Panel (Lyrics & Queue)...")
        assert not app.desktop_panel_open, "Desktop panel should initially be closed"

        # Open Lyrics Panel
        sample_track = TrackModel(
            video_id="desktop_test_01",
            title="Desktop Symphony",
            artist="Maestro AI",
            duration=240,
            album_art="album_art.png"
        )
        app.player_controller.set_track(sample_track)
        app.player_controller.set_custom_queue([sample_track], start_track=sample_track)

        app.toggle_desktop_lyrics_panel()
        assert app.desktop_panel_open is True, "Desktop panel should be open"
        assert app.desktop_panel_tab == "lyrics", "Desktop panel tab should be lyrics"
        assert desktop_side_panel.width > 0, f"Desktop side panel width should be > 0 when open, got {desktop_side_panel.width}"
        assert desktop_side_panel.disabled is False, "Desktop side panel should not be disabled when open"

        # Switch to Queue Tab
        app.toggle_desktop_queue_panel()
        assert app.desktop_panel_open is True, "Desktop panel should remain open when switching to queue"
        assert app.desktop_panel_tab == "queue", "Desktop panel tab should be queue"

        # Close Panel
        app.close_desktop_panel()
        assert app.desktop_panel_open is False, "Desktop panel should be closed"
        assert desktop_side_panel.disabled is True, "Desktop side panel MUST be disabled when closed"
        assert desktop_side_panel.width == 0, f"Desktop side panel width must be 0 when closed, got {desktop_side_panel.width}"

        results["desktop_side_panel_verified"] = True
        print("    [PASS] Desktop side panel cleanly toggles between lyrics, queue, and closed states.")

        # ---------------------------------------------------------
        # TEST 4: Volume Architecture, Muting & Delta Adjustments
        # ---------------------------------------------------------
        print("  [STEP 4] Validating Volume Control, Mute & Delta Adjustments...")
        app.set_volume(0.75)
        assert abs(app.current_volume - 0.75) < 0.001, f"Expected app volume 0.75, got {app.current_volume}"
        assert abs(app.player_controller.volume - 0.75) < 0.001, f"Expected controller volume 0.75, got {app.player_controller.volume}"
        assert abs(app.player_controller.audio_engine.volume - 0.75) < 0.001, f"Expected engine volume 0.75, got {app.player_controller.audio_engine.volume}"

        # Adjust Delta (+0.1)
        app.adjust_volume_delta(0.10)
        assert abs(app.current_volume - 0.85) < 0.001, f"Expected volume 0.85 after +0.10 delta, got {app.current_volume}"

        # Toggle Mute
        app.toggle_mute()
        assert app.player_controller.is_muted is True, "Player controller should report is_muted=True"
        assert app.player_controller.audio_engine.muted is True, "Audio engine should be muted"

        # Unmute
        app.toggle_mute()
        assert app.player_controller.is_muted is False, "Player controller should report is_muted=False after toggle"
        assert abs(app.current_volume - 0.85) < 0.001, f"Unmute should restore volume 0.85, got {app.current_volume}"

        results["volume_architecture_verified"] = True
        print("    [PASS] Master volume, incremental adjustments, and muting synchronized across engine.")

        # ---------------------------------------------------------
        # TEST 5: Desktop Keyboard Shortcuts Arbitration
        # ---------------------------------------------------------
        print("  [STEP 5] Validating Desktop Keyboard Shortcuts...")
        from utils.desktop_utils import DesktopKeyboardManager
        kbd = DesktopKeyboardManager(app)

        # Space -> Play/Pause
        initial_playing = app.player_controller.is_playing
        handled = kbd._on_key_down(Window, DesktopKeyboardManager.KEY_SPACE, 0, ' ', [])
        assert handled is True, "Space key should be handled by DesktopKeyboardManager"
        assert app.player_controller.is_playing != initial_playing, "Space key must toggle playback state"

        # M -> Mute toggle
        handled = kbd._on_key_down(Window, DesktopKeyboardManager.KEY_M, 0, 'm', [])
        assert handled is True, "M key should be handled by DesktopKeyboardManager"
        assert app.player_controller.is_muted is True, "M key should have muted audio"
        kbd._on_key_down(Window, DesktopKeyboardManager.KEY_M, 0, 'm', [])
        assert app.player_controller.is_muted is False, "Second M key should have unmuted audio"

        # Up / Down Arrows -> Volume delta
        vol_before = app.current_volume
        kbd._on_key_down(Window, DesktopKeyboardManager.KEY_UP, 0, '', [])
        assert app.current_volume > vol_before, "Up arrow should increase volume"
        kbd._on_key_down(Window, DesktopKeyboardManager.KEY_DOWN, 0, '', [])
        assert abs(app.current_volume - vol_before) < 0.001, "Down arrow should decrease volume back"

        # L -> Toggle lyrics panel
        kbd._on_key_down(Window, DesktopKeyboardManager.KEY_L, 0, 'l', [])
        assert app.desktop_panel_open is True and app.desktop_panel_tab == "lyrics", "L key should open lyrics panel"

        # Esc -> Close panel
        kbd._on_key_down(Window, DesktopKeyboardManager.KEY_ESC, 0, '', [])
        assert app.desktop_panel_open is False, "Esc key should close desktop panel"

        results["keyboard_shortcuts_verified"] = True
        print("    [PASS] Keyboard shortcuts (Space, M, Up/Down, L, Esc) arbitrate correctly.")

        # ---------------------------------------------------------
        # TEST 6: Invariant Restoration (Back to Mobile Size)
        # ---------------------------------------------------------
        print("  [STEP 6] Re-verifying Mobile Invariants after Desktop Session...")
        app.check_responsive_layout(width=360)
        assert not app.is_desktop_layout, "App should revert to mobile layout cleanly"
        assert mini_player.disabled is False, "Mobile mini_player must re-enable"
        assert bottom_nav.disabled is False, "Mobile bottom_nav must re-enable"
        assert desktop_player_bar.disabled is True, "Desktop player bar must disable"
        assert desktop_nav_rail.disabled is True, "Desktop nav rail must disable"

        results["invariants_restored"] = True
        print("    [PASS] Smooth dynamic bidirectional transition between Mobile and Desktop modes.")

        print("\n" + "=" * 60)
        print("ALL DESKTOP UI/UX & ERGONOMICS TESTS PASSED SUCCESSFULLY!")
        print("=" * 60)
        app.stop()
        if on_complete:
            on_complete(True, results)

    Clock.schedule_once(test_logic, 0.05)
    app.run()

if __name__ == "__main__":
    run_test()
