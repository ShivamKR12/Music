import os
import sys
import time

os.environ["KIVY_HEADLESS"] = "1"
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "KivyMusicApp"))
os.chdir(APP_DIR)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from kivy.clock import Clock
from kivy.core.window import Window
from main import MusicApp

def capture_screens():
    app = MusicApp()
    app.root = app.build()
    app.on_start()

    artifacts_dir = r"C:\Users\Shivam\.gemini\antigravity\brain\3fa220f8-2d51-4ed4-9907-ad9bbebdaeb5"
    os.makedirs(artifacts_dir, exist_ok=True)

    for _ in range(20):
        Clock.tick()
        time.sleep(0.02)

    # 1. Capture Home Screen
    app.switch_screen("home")
    for _ in range(10):
        Clock.tick()
        time.sleep(0.02)
    home_shot = os.path.join(artifacts_dir, "verified_home_backend0001.png")
    Window.screenshot(home_shot)
    for _ in range(5):
        Clock.tick()
        time.sleep(0.02)

    # 2. Capture Now Playing Screen with active track
    first_track = app.playlist_model.tracks[0]
    app.play_selected_track(first_track)
    for _ in range(15):
        Clock.tick()
        time.sleep(0.02)
    player_shot = os.path.join(artifacts_dir, "verified_player_backend0001.png")
    Window.screenshot(player_shot)
    for _ in range(5):
        Clock.tick()
        time.sleep(0.02)

    # 3. Capture Search Screen
    app.switch_screen("search")
    app.perform_search("Dil")
    for _ in range(10):
        Clock.tick()
        time.sleep(0.02)
    search_shot = os.path.join(artifacts_dir, "verified_search_backend0001.png")
    Window.screenshot(search_shot)
    for _ in range(5):
        Clock.tick()
        time.sleep(0.02)

    app.player_controller.stop()
    print("Screenshots captured successfully!")

if __name__ == '__main__':
    capture_screens()
