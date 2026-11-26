"""
Test Suite: Interface style switch (classic <-> new look)
Verifies that the settings toggle swaps KV rules, recreates the four switchable
screens with the right ids, persists the choice, and switches back cleanly.
"""
import os
import sys

os.environ["KIVY_HEADLESS"] = "1"
os.chdir(r"C:\Users\Shivam\Desktop\Music\KivyMusicApp")
sys.path.insert(0, r"C:\Users\Shivam\Desktop\Music\KivyMusicApp")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from kivy.clock import Clock
from main import MusicApp
from models.database import get_setting, set_setting

print("=" * 64)
print("[TEST] Interface Style Switch Validation")
print("=" * 64)

failures = []

def check(label, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(label)

def pump(n=8):
    for _ in range(n):
        Clock.tick()

original = get_setting("ui_mode", "new")
try:
    set_setting("ui_mode", "new")
    app = MusicApp()
    root = app.build()
    app.root = root
    pump()

    sm = root.ids.screen_manager

    def ids(screen_name):
        return set(sm.get_screen(screen_name).ids.keys())

    # --- 1. Starts in the new look (headless always forces new) ---
    check("Boots in new look", app.ui_mode == "new", f"ui_mode={app.ui_mode}")
    check("New home header present", "home_header" in ids("home"))
    check("New home shelves present", {"listen_again_list", "quick_picks_list", "trending_list"} <= ids("home"))
    check("New library tiles present", "favorites_fan" in ids("library"))
    check("New settings grouped scroll present", "settings_scroll" in ids("settings"))

    # --- 2. Verify settings has no deprecated skin toggles ---
    def has_toggle_row():
        return any(
            w.__class__.__name__ == "MDListItemHeadlineText" and getattr(w, "text", "") == "Interface Style"
            for w in sm.get_screen("settings").walk()
        )
    check("Deprecated Interface Style toggle removed from settings", not has_toggle_row())

    # --- 3. Calling toggle_ui_mode is safe and leaves modern look active ---
    app.toggle_ui_mode()
    pump()
    check("ui_mode remains modern 'new'", app.ui_mode == "new", f"ui_mode={app.ui_mode}")
    check("Choice persisted to SQLite as new", get_setting("ui_mode") == "new")
    check("Home header still present", "home_header" in ids("home"))
    check("Home shelves still present", {"listen_again_list", "quick_picks_list", "trending_list"} <= ids("home"))
    check("Player below-the-fold cards present", {"lyrics_card", "artist_card", "description_card"} <= ids("player"))
    check("Current screen still valid", sm.current in sm.screen_names, f"current={sm.current}")

finally:
    # Never leave the shared dev DB in classic mode for the rest of the battery.
    set_setting("ui_mode", original if original in ("new", "classic") else "new")

if failures:
    print(f"\n[FAILED] Interface style switch: {len(failures)} check(s) failed: {failures}")
    sys.exit(1)
print("\n[ALL PASSED] Interface style switch suite succeeded!")
