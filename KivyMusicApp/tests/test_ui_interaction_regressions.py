"""Regression tests for UI interaction fixes (stale ripple, FAB, search, filters, lyrics).

Standalone headless suite; no audio playback. Run with:
    python tests/test_ui_interaction_regressions.py
"""
import os
import sys

os.environ["KIVY_HEADLESS"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from kivy.clock import Clock
from kivy.input.motionevent import MotionEvent
from kivymd.app import MDApp
from main import MusicApp
from services.lyrics_service import clean_song_title
from utils.content_filters import filter_tracks, is_ai_generated, is_non_music_video
from utils.interaction_state import clear_press_feedback


def check(name, fn):
    fn()
    print(f"  [PASS] {name}")


def test_content_filters():
    tutorial = {"title": "How to make AI videos for free", "artist": "Channel", "media_type": "song"}
    ai_song = {"title": "My AI Song", "artist": "Suno User", "media_type": "song"}
    normal = {"title": "Fairytale", "artist": "Alexander Rybak", "media_type": "song"}
    assert is_non_music_video(tutorial)
    assert is_ai_generated(ai_song)
    assert not is_non_music_video(normal) and not is_ai_generated(normal)
    assert [t["title"] for t in filter_tracks([tutorial, ai_song, normal])] == ["Fairytale"]
    # AI toggle re-enables AI songs; tutorials stay filtered regardless.
    assert [t["title"] for t in filter_tracks([tutorial, ai_song, normal], include_ai=True)] == [
        "My AI Song", "Fairytale"
    ]


def test_lyrics_title_cleaning():
    title = "Maati - MC Square (8D Audio) | Use Headphones | Darken Nights"
    assert clean_song_title(title) == "Maati"


def test_clear_press_feedback():
    from kivymd.uix.button import MDIconButton

    app = MDApp.get_running_app()
    assert app is not None
    btn = MDIconButton(icon="play")
    btn.state = "down"
    btn._doing_ripple = True
    clear_press_feedback(btn)
    assert btn.state == "normal"
    assert not btn._doing_ripple
    assert btn._ripple_rad == 0


def test_search_debounce():
    app = MDApp.get_running_app()
    coord = app.search_coord
    coord.on_search_text_change("a")
    assert coord._suggest_event is not None
    coord._suggest_event.cancel()
    coord._suggest_event = None


def test_fab_consumes_touch():
    from views.components import TouchBlockingFabButton

    app = MDApp.get_running_app()
    fab = TouchBlockingFabButton(icon="folder-music")
    fab.size = (56, 56)
    fab.pos = (100, 100)

    class Touch(MotionEvent):
        def __init__(self, x, y):
            super().__init__("mouse", {}, x, y)
            self.px = self.py = self.sx = self.sy = self.ox = self.oy = x
            self.x, self.y = x, y

            self.button = "left"

    t = Touch(128, 128)
    assert fab.on_touch_down(t) is True


def main():
    app = MusicApp()
    app.player_controller.audio_engine.muted = True
    app.player_controller.audio_engine.volume = 0.0
    app.root = app.build()
    app.on_start()
    for _ in range(8):
        Clock.tick()
    try:
        print("\n=== UI INTERACTION REGRESSION TESTS ===")
        check("AI/tutorial content filters", test_content_filters)
        check("lyrics title cleaning for real library titles", test_lyrics_title_cleaning)
        check("stale ripple/press state reset", test_clear_press_feedback)
        check("search suggestions debounced", test_search_debounce)
        check("library FAB consumes its own touch", test_fab_consumes_touch)
        print("ALL UI INTERACTION REGRESSION TESTS PASSED")
    finally:
        app.stop()


if __name__ == "__main__":
    main()
