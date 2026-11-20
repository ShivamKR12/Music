"""
KivyMusicApp Master Test Suite Runner
Executes all regression, visual geometry, touch routing, settings persistence,
lyrics math, and dynamic data tests across clean isolated processes in headless mode.
"""
import os
import sys
import subprocess
import time

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

TEST_MODULES = [
    ("Lyrics Engine & Centering Math", "test_lyrics_engine_and_math.py"),
    ("Player Queue & Audio Precision", "test_player_queue_and_offline.py"),
    ("Interactive Widgets Action Binding", "test_interactive_widgets_audit.py"),
    ("Settings & SQLite Persistence", "test_settings_and_persistence.py"),
    ("Interface Style Switch", "test_ui_mode_switch.py"),
    ("Artwork Cleanliness & Geometry", "test_artwork_and_ui_geometry.py"),
    ("Artist & Album Dynamic Invariants", "test_artist_and_album_dynamic.py"),
    ("Podcasts & Trending Invariants", "test_podcasts_and_trending.py"),
    ("Backend & SQLite Integration", "test_backend_integration.py"),
    ("Historical Verification Battery", "test_battery_fixes.py"),
    ("SimpMusic Features & Dynamic Playlists", "test_simpmusic_features_and_dynamic_playlists.py"),
    ("Multi-Source Providers (YouTube, Spotify, JioSaavn)", "test_multi_source_providers.py"),
    ("SimpMusic UI/UX Parity & Fluid Transitions", "test_simpmusic_ui_ux_parity.py"),
    ("SimpMusic Dynamic Palette & Theming", "test_simpmusic_color_palette.py"),
    ("Comprehensive 13-Suite UI/UX Audit", "test_comprehensive_audit.py"),
]

def main():
    print("=" * 70)
    print("KIVYMUSICAPP MASTER HEADLESS TEST SUITE")
    print(f"Python: {sys.version.split()[0]} | Working Dir: {TEST_DIR}")
    print("=" * 70)
    # Test output is decoded with errors="replace" and can contain U+FFFD; make stdout
    # UTF-8-tolerant so console encodings (e.g. cp1252) never crash the runner mid-battery.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    overall_start = time.time()
    suite_results = []
    all_passed = True

    for title, filename in TEST_MODULES:
        filepath = os.path.join(TEST_DIR, filename)
        if not os.path.exists(filepath):
            print(f"[SKIP] Test file not found: {filename}")
            suite_results.append((title, "NOT FOUND", 0.0))
            all_passed = False
            continue

        print(f"\n>>> Running: {title} ({filename})...")
        start_t = time.time()
        
        env = os.environ.copy()
        env["KIVY_HEADLESS"] = "1"
        env["KIVY_LOG_MODE"] = "PYTHON"

        proc = subprocess.run(
            [sys.executable, "-u", filepath],
            cwd=os.path.abspath(os.path.join(TEST_DIR, "..")),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        elapsed = time.time() - start_t

        if proc.stdout:
            print(proc.stdout.strip())
        if proc.returncode != 0:
            if proc.stderr:
                print("--- STDERR ---")
                print(proc.stderr.strip())
            print(f"[FAILED] {title} exited with code {proc.returncode} in {elapsed:.2f}s")
            suite_results.append((title, f"FAILED (code {proc.returncode})", elapsed))
            all_passed = False
        else:
            print(f"[PASSED] {title} completed successfully in {elapsed:.2f}s")
            suite_results.append((title, "PASSED", elapsed))

    total_time = time.time() - overall_start
    print("\n" + "=" * 70)
    print("MASTER TEST SUITE SUMMARY")
    print("=" * 70)
    for title, status, elapsed in suite_results:
        print(f"  {title:<42} : {status:<15} ({elapsed:.2f}s)")
    print("-" * 70)
    print(f"Total Execution Time: {total_time:.2f}s")
    
    if all_passed:
        print("OVERALL RESULT: 100% OF TESTS PASSED WITH ZERO CRASHES OR REGRESSIONS!")
        print("=" * 70)
        sys.exit(0)
    else:
        print("OVERALL RESULT: ONE OR MORE TESTS FAILED. CHECK LOGS ABOVE.")
        print("=" * 70)
        sys.exit(1)

if __name__ == "__main__":
    main()
