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
from utils.local_audio_utils import scan_device_offline_songs
from models.database import add_track_to_playlist

def capture():
    app = MusicApp()
    app.root = app.build()
    app.on_start()

    artifacts_dir = r"C:\Users\Shivam\.gemini\antigravity\brain\3fa220f8-2d51-4ed4-9907-ad9bbebdaeb5"
    os.makedirs(artifacts_dir, exist_ok=True)

    for _ in range(25):
        Clock.tick()
        time.sleep(0.02)

    # 1. Scan and populate Offline Songs playlist
    scanned = scan_device_offline_songs(limit=10, cache_dir=app.cache_dir)
    for s in scanned:
        add_track_to_playlist("Offline Songs", s["video_id"], s)

    # Open Offline Songs playlist
    app.open_playlist("Offline Songs")
    for _ in range(20):
        Clock.tick()
        time.sleep(0.02)
    Window.screenshot(os.path.join(artifacts_dir, "verified_offline_playlist0001.png"))

    # 2. Play active offline playlist and capture PlayerScreen
    app.play_active_playlist(shuffle=False)
    for _ in range(20):
        Clock.tick()
        time.sleep(0.02)
    Window.screenshot(os.path.join(artifacts_dir, "verified_offline_player0001.png"))

    # 3. Capture Library screen with Downloaded card
    app.switch_screen("library")
    for _ in range(15):
        Clock.tick()
        time.sleep(0.02)
    Window.screenshot(os.path.join(artifacts_dir, "verified_library_offline0001.png"))

    app.player_controller.stop()
    print("ALL OFFLINE & MARQUEE SCREENSHOTS CAPTURED!")

if __name__ == '__main__':
    capture()
