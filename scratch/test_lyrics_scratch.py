import os
import sys

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "KivyMusicApp"))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from services.lyrics_service import fetch_lyrics_sync

print("Testing lyrics fetch sync...")
lyrics = fetch_lyrics_sync("Dil Lutiya", "Jaswinder Daghamia", "TI7RQO2cuh0")
print("Fetched length:", len(lyrics))
print("Preview:\n", lyrics[:150])
assert len(lyrics) > 20
assert "lutiya" in lyrics.lower()
print("Lyrics test PASSED!")
