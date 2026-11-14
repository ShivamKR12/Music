import os
import sys

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "KivyMusicApp"))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from utils.local_audio_utils import extract_local_audio_metadata, scan_device_offline_songs

print("Testing single file extraction on 101 - MC Square...")
f1 = os.path.expanduser("~/Music/101 - MC Square.mp3")
if os.path.exists(f1):
    meta1 = extract_local_audio_metadata(f1)
    print("Meta 1:", meta1["title"], "|", meta1["artist"], "| Art:", bool(meta1["artwork"]))
    assert meta1["artist"] == "MC Square"
    assert meta1["artwork"] and os.path.exists(meta1["artwork"])

print("Testing single file extraction on Aditya Rikhari (PNG art)...")
f2 = os.path.expanduser("~/Music/Aditya Rikhari - SAMJHO NA ( NASAMAJH ).mp3")
if os.path.exists(f2):
    meta2 = extract_local_audio_metadata(f2)
    print("Meta 2:", meta2["title"], "|", meta2["artist"], "| Art:", bool(meta2["artwork"]))
    assert "Aditya Rikhari" in meta2["artist"]
    assert meta2["artwork"] and os.path.exists(meta2["artwork"])

print("Testing device scan...")
tracks = scan_device_offline_songs(limit=10)
print(f"Scanned {len(tracks)} offline tracks from device!")
assert len(tracks) > 0
for t in tracks[:3]:
    print(f" - {t['title']} by {t['artist']} (Art: {os.path.basename(t['artwork']) if t['artwork'] else 'None'})")

print("ALL LOCAL AUDIO UTILS TESTS PASSED!")
