import os
import sys
import unittest

os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_HEADLESS"] = "1"

# Add project root to sys.path and chdir
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
os.chdir(project_root)

from kivy.clock import Clock
from kivy.uix.screenmanager import SlideTransition, NoTransition
from kivy.utils import get_color_from_hex
from main import MusicApp
from models.track_model import TrackModel

class TestSimpMusicUIUXParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = MusicApp()
        cls.app.player_controller.audio_engine.muted = True
        cls.app.player_controller.audio_engine.volume = 0.0
        cls.root = cls.app.build()
        cls.app.root = cls.root
        cls.app.on_start()
        Clock.tick()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.app.stop()
        except Exception:
            pass

    def setUp(self):
        # Strictly ensure muted volume for every test
        self.app.player_controller.audio_engine.muted = True
        self.app.player_controller.audio_engine.volume = 0.0

    def test_01_fitimage_and_image_mipmap_enabled(self):
        """Verify global mipmap rule is active on FitImage, eliminating aliasing/graininess."""
        from kivymd.uix.fitimage.fitimage import FitImage
        from kivy.uix.image import Image, AsyncImage

        fit_img = FitImage()
        self.assertTrue(getattr(fit_img, "mipmap", False), "FitImage must have mipmap=True globally")

        img = Image()
        self.assertTrue(getattr(img, "mipmap", False), "Image must have mipmap=True globally")

        async_img = AsyncImage()
        self.assertTrue(getattr(async_img, "mipmap", False), "AsyncImage must have mipmap=True globally")
        print("[PASS] Test 1: Global mipmapping enabled on FitImage, Image, and AsyncImage")

    def test_02_directional_screen_transitions(self):
        """Verify intelligent directional SlideTransitions (up for player, down on exit, left/right on tabs/details)."""
        sm = self.root.ids.screen_manager

        # Temporarily unset KIVY_HEADLESS to test transition direction assignment
        prev_headless = os.environ.get("KIVY_HEADLESS")
        try:
            os.environ["KIVY_HEADLESS"] = "0"
            sm.width = 400
            sm.height = 800

            # 1. Switch home -> search: tab forward -> direction 'left'
            sm.current = "home"
            self.app.switch_screen("search")
            self.assertEqual(sm.current, "search")
            self.assertEqual(sm.transition.direction, "left")

            # 2. Switch search -> home: tab backward -> direction 'right'
            self.app.switch_screen("home")
            self.assertEqual(sm.current, "home")
            self.assertEqual(sm.transition.direction, "right")

            # 3. Switch home -> player: opening player expands upward -> direction 'up'
            self.app.switch_screen("player")
            self.assertEqual(sm.current, "player")
            self.assertEqual(sm.transition.direction, "up")

            # 4. Exit player via go_back -> direction 'down'
            self.app.go_back()
            self.assertEqual(sm.current, "home")
            self.assertEqual(sm.transition.direction, "down")

            # 5. Open sub-screen (album/settings) -> direction 'left'
            self.app.switch_screen("settings")
            self.assertEqual(sm.current, "settings")
            self.assertEqual(sm.transition.direction, "left")

            # 6. Exit sub-screen via go_back -> direction 'right'
            self.app.go_back()
            self.assertEqual(sm.current, "home")
            self.assertEqual(sm.transition.direction, "right")
        finally:
            if prev_headless is not None:
                os.environ["KIVY_HEADLESS"] = prev_headless
            sm.width = 0
            sm.height = 0

        print("[PASS] Test 2: Directional SlideTransitions verified (up, down, left, right)")

    def test_03_mini_player_simpmusic_floating_capsule_geometry(self):
        """Verify MiniPlayer floating capsule pill geometry, radius, and components."""
        sm = self.root.ids.screen_manager
        sm.current = "home"
        mini = self.root.ids.mini_player

        # Activate track so mini player is visible for geometry verification
        if self.app.playlist_model.tracks:
            self.app.player_controller.set_track(self.app.playlist_model.tracks[0])
            self.app.mini_player_visible = True
            Clock.tick()

        # Mini player container must have 72dp height when visible on home
        self.assertEqual(mini.height, 72.0)
        self.assertFalse(mini.disabled)

        # Inspect child card
        card = mini.children[0]
        # Radius must be pill capsule [24dp]
        self.assertEqual(card.radius, [24.0, 24.0, 24.0, 24.0])
        self.assertEqual(card.height, 64.0)

        # Find linear progress indicator inside card
        progress_indicators = [w for w in card.walk() if "MDLinearProgressIndicator" in w.__class__.__name__]
        self.assertTrue(len(progress_indicators) > 0, "Mini player card must contain an MDLinearProgressIndicator")
        self.assertEqual(progress_indicators[0].height, 2.0)

        # Find circular album art with radius 23dp
        fit_images = [w for w in card.walk() if "FitImage" in w.__class__.__name__]
        self.assertTrue(len(fit_images) > 0, "Mini player must contain a FitImage")
        self.assertEqual(fit_images[0].radius, [23.0, 23.0, 23.0, 23.0])

        # Find circular filled Play/Pause button
        icon_buttons = [w for w in card.walk() if "MDIconButton" in w.__class__.__name__]
        filled_play = [b for b in icon_buttons if getattr(b, "style", "") == "filled"]
        self.assertTrue(len(filled_play) > 0, "Mini player must contain a filled circular Play/Pause button")
        self.assertEqual(filled_play[0].size, [42.0, 42.0])

        print("[PASS] Test 3: MiniPlayer SimpMusic floating capsule pill geometry verified")

    def test_04_simpmusic_favorite_pink_color_consistency(self):
        """Verify SimpMusic favorite pink #FF4081 is applied on favorite toggles."""
        expected_pink = get_color_from_hex("#FF4081")

        # 1. MiniPlayer favorite button
        mini = self.root.ids.mini_player
        self.app.player_controller.is_favorite = True
        fav_btn = [b for b in mini.walk() if "MDIconButton" in b.__class__.__name__ and "heart" in getattr(b, "icon", "")]
        self.assertTrue(len(fav_btn) > 0)
        self.assertEqual(fav_btn[0].icon_color[:3], expected_pink[:3])

        # 2. Player screen favorite button
        player_screen = self.root.ids.screen_manager.get_screen("player")
        p_fav = [b for b in player_screen.walk() if "MDIconButton" in b.__class__.__name__ and "heart" in getattr(b, "icon", "")]
        if p_fav:
            self.assertEqual(p_fav[0].icon_color[:3], expected_pink[:3])

        self.app.player_controller.is_favorite = False
        print("[PASS] Test 4: SimpMusic favorite pink #FF4081 verified across components")

    def test_05_animated_background_cpu_preservation(self):
        """Verify AnimatedBackground _tick skips mesh calculation when player screen is not current."""
        from views.components import AnimatedBackground

        bg = AnimatedBackground()
        bg.is_active = True
        bg.variation = "gradient"
        bg.mesh.vertices = [1.0, 2.0, 3.0]

        # Home screen current -> _tick should skip and not mutate vertices
        self.root.ids.screen_manager.current = "home"
        bg._tick(0.016)
        # Vertices should remain unchanged because it returned immediately
        self.assertEqual(bg.mesh.vertices, [1.0, 2.0, 3.0])

        # Inactive/off -> should clear vertices
        bg.is_active = False
        bg._tick(0.016)
        self.assertEqual(bg.mesh.vertices, [])

        print("[PASS] Test 5: AnimatedBackground CPU preservation invariant verified")

    def test_06_player_screen_top_app_bar_controls(self):
        """Verify PlayerScreen has Now Playing title, chevron-down, heart favorite, lyrics, and options."""
        sm = self.root.ids.screen_manager
        if not sm.has_screen("player"):
            self.app.switch_screen("player")
        player_screen = sm.get_screen("player")
        bars = [w for w in player_screen.walk() if "MDTopAppBar" in type(w).__name__]
        self.assertTrue(len(bars) > 0, "PlayerScreen must contain an MDTopAppBar")
        bar = bars[0]

        leading_icons = [getattr(c, "icon", "") for c in getattr(bar, "_leading_button_container", []).children]
        trailing_icons = [getattr(c, "icon", "") for c in getattr(bar, "_trailing_button_container", []).children]
        all_appbar_icons = leading_icons + trailing_icons

        self.assertIn("chevron-down", all_appbar_icons, f"PlayerScreen must have chevron-down exit button (found: {all_appbar_icons})")
        self.assertIn("dots-vertical", all_appbar_icons, f"PlayerScreen must have options button (found: {all_appbar_icons})")
        # In SimpMusic M3 Expressive, heart is beside track title and lyrics is in action bar & below-the-fold card
        all_screen_icons = [getattr(w, "icon", "") for w in player_screen.walk() if hasattr(w, "icon")]
        self.assertTrue(any("heart" in icon for icon in all_screen_icons), f"PlayerScreen must have favorite heart button (found: {all_screen_icons})")
        self.assertTrue(any(icon in ("format-quote-close", "text-box-outline", "microphone-variant") for icon in all_screen_icons), f"PlayerScreen must have lyrics trigger (found: {all_screen_icons})")
        print("[PASS] Test 6: PlayerScreen top app bar and controls verified")

if __name__ == "__main__":
    unittest.main()
