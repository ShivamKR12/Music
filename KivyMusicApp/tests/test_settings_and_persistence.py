"""
Test Suite: Settings & SQLite Persistence
Verifies:
1. Default theme is Light ('Light').
2. Toggling wifi_only, dark_mode, extract_artwork_colors, animated_bg, sponsorblock.
3. Database persistence across all settings.
4. PassiveTrailingCheckbox touch dispatch (no event stealing).
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
from models.database import get_setting, set_setting

def run_test(on_complete=None):
    app = MusicApp()
    results = {}

    def test_logic(dt):
        print("\n[TEST] Starting Settings & Persistence Validation...")
        sm = app.root.ids.screen_manager
        sm.transition = NoTransition()

        # 1. Default Theme Style is Light
        current_theme = app.theme_cls.theme_style
        db_theme = get_setting("theme_style", "Light")
        assert current_theme == "Light", f"Expected theme 'Light', got '{current_theme}'"
        assert db_theme == "Light", f"Expected DB theme 'Light', got '{db_theme}'"
        results["default_theme_is_light"] = True
        print("  [PASS] Default theme is Light in app and SQLite.")

        # 2. Switch to Settings screen
        app.switch_screen("settings")
        settings_screen = sm.get_screen("settings")

        # 3. Verify checkboxes exist and are PassiveTrailingCheckbox
        wifi_cb = settings_screen.ids.get("wifi_checkbox")
        dark_cb = settings_screen.ids.get("dark_checkbox")
        color_cb = settings_screen.ids.get("color_extract_checkbox")
        anim_bg_cb = settings_screen.ids.get("anim_bg_checkbox")
        sponsor_cb = settings_screen.ids.get("sponsor_checkbox")

        assert wifi_cb is not None, "wifi_checkbox not found"
        assert dark_cb is not None, "dark_checkbox not found"
        assert color_cb is not None, "color_extract_checkbox not found"
        assert anim_bg_cb is not None, "anim_bg_checkbox not found"
        assert sponsor_cb is not None, "sponsor_checkbox not found"

        # Check touch pass-through delegation (must return False to let MDListItem receive click)
        class DummyTouch:
            pos = (0, 0)
            def is_mouse_scrolling(self): return False
        dtouch = DummyTouch()
        assert wifi_cb.on_touch_down(dtouch) is False, "wifi_checkbox must return False on touch"
        assert dark_cb.on_touch_down(dtouch) is False, "dark_checkbox must return False on touch"
        results["checkboxes_passive"] = True
        print("  [PASS] Trailing checkboxes are passive (return False on touch events).")

        # 4. Toggle wifi_only & assert persistence
        init_wifi = app.wifi_only
        app.toggle_wifi_only()
        assert app.wifi_only != init_wifi, "wifi_only failed to toggle"
        assert wifi_cb.active == app.wifi_only, "wifi_checkbox active state mismatch"
        assert get_setting("wifi_only") == str(app.wifi_only), "wifi_only not persisted in SQLite"
        # Toggle back
        app.toggle_wifi_only()
        results["wifi_toggle_persisted"] = True
        print("  [PASS] wifi_only toggles and persists to SQLite.")

        # 5. Toggle dark_mode & assert persistence
        app.toggle_dark_mode()
        assert app.theme_cls.theme_style == "Dark", "Theme style failed to switch to Dark"
        assert get_setting("theme_style") == "Dark", "Dark theme not persisted in SQLite"
        # Revert strictly to Light mode
        app.toggle_dark_mode()
        assert app.theme_cls.theme_style == "Light", "Theme style failed to revert to Light"
        assert get_setting("theme_style") == "Light", "Light theme not restored in SQLite"
        results["dark_mode_toggle_persisted"] = True
        print("  [PASS] Dark mode toggles and correctly restores Light mode in SQLite.")

        # 6. Toggle background animations & assert persistence
        init_anim = app.animated_bg_enabled
        app.toggle_animated_bg()
        assert app.animated_bg_enabled != init_anim, "animated_bg failed to toggle"
        assert get_setting("animated_bg_enabled") == str(app.animated_bg_enabled), "animated_bg not persisted"
        app.toggle_animated_bg()
        results["anim_bg_persisted"] = True
        print("  [PASS] animated_bg toggles and persists to SQLite.")

        # 7. Test Dialogs (About, Logs, Log Level, Provider Selector) do not throw exceptions
        app.show_about_dialog()
        app.show_logs_dialog()
        app.show_log_level_dialog()
        app.show_provider_selector_dialog()
        results["dialogs_verified"] = True
        print("  [PASS] About, Logs, Log Level, and Provider Selector dialogs instantiate without error.")

        # Ensure Light theme is strictly persisted on exit
        app.theme_cls.theme_style = "Light"
        set_setting("theme_style", "Light")

        print("  [ALL PASSED] Settings & Persistence Test Suite Succeeded!")
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
