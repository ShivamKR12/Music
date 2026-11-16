import os
import sys
import time
import tempfile

os.chdir(r"c:\Users\Shivam\Desktop\Music\KivyMusicApp")
sys.path.insert(0, r"c:\Users\Shivam\Desktop\Music\KivyMusicApp")

os.environ['KIVY_HEADLESS'] = '1'

from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition

from models.database import (
    init_db,
    add_track,
    get_all_tracks,
    get_track,
    add_playlist,
    get_all_playlists,
    add_track_to_playlist,
    get_playlist_tracks,
    toggle_favorite,
    is_favorite,
    add_search_history,
    get_search_history,
    clear_search_history,
)
from models.track_model import TrackModel, PlaylistModel
from controllers.player_controller import PlayerController
from services.audio_engine import AudioEngine
from main import MusicApp

def pump_events(app, n=5):
    for _ in range(n):
        Clock.tick()
        time.sleep(0.02)

test_results = {}

def test_assert(name, condition, msg=""):
    test_results[name] = condition
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}: {msg}")
    if not condition:
        raise AssertionError(f"Test failed: {name} - {msg}")

def run_tests():
    print("=== STARTING BACKEND & DATABASE INTEGRATION TEST BATTERY ===")

    # 1. Database CRUD & Schema Test
    print("\n--- 1. Testing SQLite Database Engine ---")
    init_db()
    
    # Test track insertion
    test_vid = "test_vid_123"
    add_track(test_vid, "Integration Track", "Test Artist", "https://example.com/audio", duration=240, artwork="album_art.png")
    track_record = get_track(test_vid)
    test_assert("Database Track Add & Get", track_record is not None and track_record["title"] == "Integration Track",
                f"Track retrieved: {track_record}")

    # Test playlist creation and track attachment
    test_pl = "Night Drive 2026"
    add_playlist(test_pl)
    all_pl = [p["name"] for p in get_all_playlists()]
    test_assert("Database Add Playlist", test_pl in all_pl, f"Playlists in db: {all_pl}")

    add_track_to_playlist(test_pl, test_vid)
    pl_tracks = get_playlist_tracks(test_pl)
    test_assert("Database Playlist Tracks", len(pl_tracks) > 0 and pl_tracks[0]["video_id"] == test_vid,
                f"Playlist tracks count: {len(pl_tracks)}")

    # Test Favorites toggle
    if is_favorite(test_vid):
        toggle_favorite(test_vid)
    fav_initial = is_favorite(test_vid)
    toggled = toggle_favorite(test_vid)
    test_assert("Database Favorite Toggle ON", toggled == True and is_favorite(test_vid) == True,
                f"Initial={fav_initial}, Toggled={toggled}, Now={is_favorite(test_vid)}")
    toggled_off = toggle_favorite(test_vid)
    test_assert("Database Favorite Toggle OFF", toggled_off == False and is_favorite(test_vid) == False,
                f"Toggled off={toggled_off}, Now={is_favorite(test_vid)}")

    # Test Search History
    clear_search_history()
    add_search_history("Acoustic Sessions")
    add_search_history("EDM Festival")
    history = get_search_history()
    test_assert("Database Search History Persistence", "EDM Festival" in history and "Acoustic Sessions" in history,
                f"Search history: {history}")

    # 2. AudioEngine Non-Blocking Lifecycle Test
    print("\n--- 2. Testing AudioEngine State & Callbacks ---")
    engine = AudioEngine()
    test_assert("AudioEngine Initialization", engine.player is None and engine.paused is False, "AudioEngine initialized cleanly")

    time_updates = []
    engine.on_time_update = lambda el, dur: time_updates.append((el, dur))
    
    # Test start_play with valid local wave audio
    import wave, struct
    test_wav = os.path.abspath("test_tone.wav")
    with wave.open(test_wav, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)
        data = [struct.pack("<h", 0) for _ in range(44100 // 2)]
        f.writeframes(b"".join(data))

    engine.start_play(test_wav, {"title": "Local Asset", "duration": 120})
    test_assert("AudioEngine Player Loaded", engine.player is not None, f"engine.player={engine.player}")
    engine.pause()
    test_assert("AudioEngine Pause State", engine.paused == True, f"engine.paused={engine.paused}")
    engine.unpause()
    test_assert("AudioEngine Unpause State", engine.paused == False, f"engine.paused={engine.paused}")
    engine.seek(0.25)
    test_assert("AudioEngine Seek", abs(engine.elapsed - 0.25) < 0.1, f"engine.elapsed={engine.elapsed}")
    engine.cleanup_player()
    test_assert("AudioEngine Cleanup", engine.player is None and engine.elapsed == 0.0, "Player cleaned up safely")
    try:
        if os.path.exists(test_wav):
            os.remove(test_wav)
    except Exception:
        pass

    # 3. Model & Controller Wiring Test
    print("\n--- 3. Testing PlayerController & Model Integration ---")
    playlist_model = PlaylistModel()
    test_assert("PlaylistModel Loads from DB", len(playlist_model.tracks) > 0, 
                f"Loaded {len(playlist_model.tracks)} tracks from database")

    controller = PlayerController()
    controller.set_playlist(playlist_model)
    test_track = playlist_model.tracks[0]
    controller.set_track(test_track)
    test_assert("Controller Set Track", controller.active_track == test_track, f"Active track: {test_track.title}")

    # Test toggle favorite on controller
    initial_fav = controller.is_favorite
    controller.toggle_favorite()
    test_assert("Controller Toggle Favorite", controller.is_favorite != initial_fav,
                f"Favorite changed from {initial_fav} to {controller.is_favorite}")
    # Restore
    controller.toggle_favorite()

    # Test next/prev track
    curr_idx = playlist_model.tracks.index(controller.active_track)
    # Test shuffle toggle
    controller.toggle_shuffle()
    test_assert("Controller Shuffle Toggle", controller.is_shuffle == True, "Shuffle active")
    controller.toggle_repeat()
    test_assert("Controller Repeat Toggle", controller.is_repeat == True, "Repeat active")

    # 4. Full App Search & Favorites Screen Live Verification
    print("\n--- 4. Testing Live MusicApp with Real Database & Search ---")
    app = MusicApp()
    root = app.build()
    app.root = root
    Window.add_widget(root)
    root.size = Window.size
    root.ids.screen_manager.transition = NoTransition()
    app.on_start()
    pump_events(app, 10)

    sm = root.ids.screen_manager

    # Test Search screen real history and query
    app.switch_screen("search")
    pump_events(app, 5)
    app.perform_search("Punjabi Pop")
    pump_events(app, 5)
    
    search_screen = sm.get_screen("search")
    input_text = search_screen.ids.search_input.text
    test_assert("Search Input Populated", input_text == "Punjabi Pop", f"Input text: '{input_text}'")
    
    # Check that search history has the query in SQLite and UI
    saved_history = get_search_history()
    test_assert("Search Query Persisted to SQLite", "Punjabi Pop" in saved_history, f"SQLite history: {saved_history}")

    # Test Favorites Screen dynamic sync
    # Add a track to favorites in SQLite
    toggle_favorite(playlist_model.tracks[0].video_id)
    app.show_favorites()
    pump_events(app, 5)
    fav_screen = sm.get_screen("favorites")
    test_assert("Favorites Screen Active", sm.current == "favorites", f"Active screen: {sm.current}")
    
    # Verify playlist creation in database
    init_pl_count = len(get_all_playlists())
    pl_name = f"Dynamic_PL_{int(time.time()*1000)}"
    add_playlist(pl_name)
    new_pl_count = len(get_all_playlists())
    test_assert("Playlist Created in SQLite", new_pl_count == init_pl_count + 1,
                f"Playlist count before={init_pl_count}, after={new_pl_count}")

    # Clean up app
    app.on_stop()
    pump_events(app, 3)
    if os.path.exists("test_tone.wav"):
        try: os.remove("test_tone.wav")
        except: pass

    print("\n==========================================")
    passed_count = sum(1 for v in test_results.values() if v)
    total_count = len(test_results)
    print(f"BACKEND INTEGRATION TESTS PASSED ({passed_count} / {total_count})")
    print("==========================================")
    return passed_count == total_count

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
