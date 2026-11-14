import os
import sys
import time

os.environ["KIVY_HEADLESS"] = "1"
os.chdir(os.path.abspath('KivyMusicApp'))
sys.path.insert(0, os.path.abspath('.'))

from kivy.clock import Clock
from kivymd.app import MDApp
from main import MusicApp

def run_integration_test():
    app = MusicApp()
    app.build()
    
    # Process initial frames
    for _ in range(5):
        Clock.tick()
        time.sleep(0.02)
        
    print(f"Playlist tracks count: {len(app.playlist_model.tracks)}")
    first_track = app.playlist_model.tracks[0]
    print(f"First track: {first_track.title} | id: {first_track.video_id} | local_path: {first_track.local_path} | is_downloaded: {first_track.is_downloaded}")
    
    # Play first track (which is the installed TI7RQO2cuh0)
    print("Starting playback via app.play_selected_track(first_track)...")
    app.play_selected_track(first_track)
    
    for _ in range(15):
        Clock.tick()
        time.sleep(0.04)
        
    print(f"PlayerController is_playing: {app.player_controller.is_playing}")
    print(f"AudioEngine player: {app.player_controller.audio_engine.player}")
    print(f"Active track: {app.player_controller.active_track.title}")
    print(f"Elapsed: {app.player_controller.audio_engine.elapsed:.2f}s / {app.player_controller.audio_engine.duration:.2f}s")
    
    assert app.player_controller.is_playing is True, "Track should be playing!"
    assert app.player_controller.audio_engine.player is not None, "Sound player must not be None!"
    assert app.player_controller.audio_engine.elapsed > 0.1, "Elapsed time should be progressing!"
    
    # Test pause
    app.player_controller.toggle_play()
    for _ in range(5):
        Clock.tick()
        time.sleep(0.02)
    assert app.player_controller.is_playing is False, "Playback should be paused!"
    assert app.player_controller.audio_engine.paused is True, "AudioEngine should be paused!"
    
    # Test unpause
    app.player_controller.toggle_play()
    for _ in range(5):
        Clock.tick()
        time.sleep(0.02)
    assert app.player_controller.is_playing is True, "Playback should resume!"
    assert app.player_controller.audio_engine.paused is False, "AudioEngine should be unpaused!"
    
    # Test stop & cleanup
    app.player_controller.stop()
    assert app.player_controller.is_playing is False
    assert app.player_controller.audio_engine.player is None
    
    print("SUCCESS: FULL APP AUDIO PLAYBACK INTEGRATION TEST PASSED ON PURE KIVY!")

if __name__ == "__main__":
    run_integration_test()
