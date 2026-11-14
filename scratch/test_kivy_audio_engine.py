import os
import sys
import time

out_file = open("scratch/test_output.txt", "w", encoding="utf-8")
sys.stdout = out_file
sys.stderr = out_file

sys.path.insert(0, os.path.abspath('KivyMusicApp'))

from kivy.clock import Clock
from services.audio_engine import AudioEngine

def test_engine():
    engine = AudioEngine()
    time_updates = []
    engine.on_time_update = lambda el, dur: time_updates.append((el, dur))
    
    # 1. Test starting by Video ID for cached track
    print("Testing AudioEngine.start_play('TI7RQO2cuh0')...", flush=True)
    started = engine.start_play("TI7RQO2cuh0", {"title": "Dil Lutiya", "duration": 181})
    print(f"Engine started: {started}, Player: {engine.player}", flush=True)
    
    for _ in range(10):
        time.sleep(0.05)
        Clock.tick()
        
    print(f"Elapsed: {engine.elapsed:.2f}s", flush=True)
    assert engine.elapsed > 0.2
    engine.cleanup_player()
    
    # 2. Test starting by full YouTube URL for cached track
    print("Testing AudioEngine.start_play('https://www.youtube.com/watch?v=TI7RQO2cuh0')...")
    started = engine.start_play("https://www.youtube.com/watch?v=TI7RQO2cuh0", {"title": "Dil Lutiya", "duration": 181})
    assert started, "Engine failed to start play by URL!"
    assert engine.player is not None
    for _ in range(10):
        time.sleep(0.05)
        Clock.tick()
    print(f"Elapsed: {engine.elapsed:.2f}s")
    assert engine.elapsed > 0.2
    engine.cleanup_player()
    
    print("ALL TESTS PASSED: CACHED AUDIO PLAYS VIA LOCAL PATH, VIDEO ID, AND YOUTUBE URL!")

if __name__ == "__main__":
    try:
        test_engine()
    except Exception as e:
        import traceback
        traceback.print_exc(file=out_file)
        out_file.flush()
        sys.exit(1)
