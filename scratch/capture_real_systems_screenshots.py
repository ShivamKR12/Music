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

def capture():
    app = MusicApp()
    app.root = app.build()
    app.on_start()

    artifacts_dir = r"C:\Users\Shivam\.gemini\antigravity\brain\3fa220f8-2d51-4ed4-9907-ad9bbebdaeb5"
    os.makedirs(artifacts_dir, exist_ok=True)

    for _ in range(20):
        Clock.tick()
        time.sleep(0.02)

    # 1. Capture dynamic PlaylistScreen with Chillwave
    app.open_playlist("Chillwave")
    for _ in range(15):
        Clock.tick()
        time.sleep(0.02)
    Window.screenshot(os.path.join(artifacts_dir, "verified_playlist_real0001.png"))

    # 2. Capture Now Playing screen
    if app.playlist_model.tracks:
        app.play_selected_track(app.playlist_model.tracks[0])
    for _ in range(15):
        Clock.tick()
        time.sleep(0.02)
    Window.screenshot(os.path.join(artifacts_dir, "verified_player_real0001.png"))

    # 3. Capture Album Screen
    app.open_album()
    for _ in range(10):
        Clock.tick()
        time.sleep(0.02)
    Window.screenshot(os.path.join(artifacts_dir, "verified_album_real0001.png"))

    # 4. Capture Artist Screen
    app.open_artist()
    for _ in range(10):
        Clock.tick()
        time.sleep(0.02)
    Window.screenshot(os.path.join(artifacts_dir, "verified_artist_real0001.png"))

    app.player_controller.stop()
    print("Verification screenshots captured successfully!")

if __name__ == '__main__':
    capture()
