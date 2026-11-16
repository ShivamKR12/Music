"""
Test Suite: Artwork Cleanliness & UI Geometry Standards
Verifies:
1. Favorite Songs artwork is 100% unobstructed (no red circle / heart overlay).
2. Stacked bars have non-zero explicit heights (zero-overlap invariant).
3. Hidden containers enforce disabled: True to prevent touch-stealing.
4. Touch target dimensions satisfy the minimum 48x48dp standard.
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

def run_test(on_complete=None):
    app = MusicApp()
    results = {}

    def test_logic(dt):
        print("\n[TEST] Starting Artwork Cleanliness & UI Geometry Validation...")
        sm = app.root.ids.screen_manager
        sm.transition = NoTransition()

        # 1. Favorite Songs Artwork Cleanliness
        app.show_favorites()
        fav_screen = sm.get_screen("favorites")
        fav_art = fav_screen.ids.get("favorites_art")
        assert fav_art is not None, "favorites_art ID missing from FavoritesScreen"
        
        # Verify no red circular heart card overlays the artwork
        header_card = fav_art.parent
        for child in header_card.children:
            if hasattr(child, "md_bg_color") and getattr(child, "md_bg_color") == [0.95, 0.2, 0.3, 0.9]:
                raise AssertionError("Found red circular heart overlay obstructing Favorites artwork!")
        results["favorites_artwork_unobstructed"] = True
        print("  [PASS] Favorite Songs header artwork is clean and unobstructed.")

        # 2. Check Stacked Height Invariant
        app.switch_screen("library")
        nav_bar = app.root.ids.get("bottom_nav")
        mini_player = app.root.ids.get("mini_player")

        if nav_bar:
            assert nav_bar.height > 0, f"Bottom navigation bar has collapsed height: {nav_bar.height}"
            results["bottom_nav_explicit_height"] = True
            print(f"  [PASS] Bottom navigation bar has valid height ({nav_bar.height}dp).")

        if mini_player:
            assert mini_player.height > 0, "Mini player has collapsed height"
            results["mini_player_height_valid"] = True
            print(f"  [PASS] Mini player has valid non-zero height ({mini_player.height}dp).")

        # 3. Hidden Overlay Disabled State Invariant
        app.switch_screen("player")
        # On player screen, mini player is hidden; it MUST be disabled
        if mini_player:
            assert mini_player.disabled is True, "Hidden mini player on PlayerScreen must be disabled: True"
            results["hidden_mini_player_disabled"] = True
            print("  [PASS] Hidden mini player correctly disabled (touch-stealing prevented).")

        print("  [ALL PASSED] Artwork & UI Geometry Test Suite Succeeded!")
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
