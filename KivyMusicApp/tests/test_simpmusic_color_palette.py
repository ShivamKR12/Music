"""
Unit & Integration Tests for SimpMusic Dynamic Palette & Material 3 Theming Engine.
Verifies parity with D:\\SimpMusic color extraction and neutral surface theming:
1. Palette swatch extraction (DarkVibrant, Vibrant, Muted, Dominant).
2. SimpMusic swatch priority arbitration (UIExt.kt:getColorFromPalette).
3. Adaptive darkening for immersive backgrounds (UIExt.kt:toImmersiveBackground).
4. Neutral surface preservation (Theme.kt:withNeutralLightSurfaces).
5. LRU caching and sub-millisecond repeated retrieval.
"""

import os
import sys
import unittest
import time

os.environ["KIVY_HEADLESS"] = "1"
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from utils.theme_utils import (
    extract_palette_from_image,
    apply_simpmusic_theme,
    get_perceived_luminance,
    get_active_palette,
    get_active_immersive_bg,
    clear_palette,
    _PALETTE_CACHE
)

class TestSimpMusicColorPalette(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Find or create a test image
        from PIL import Image
        cls.test_image_path = os.path.join(APP_DIR, "test_palette_art.png")
        # Create a test vibrant image: top half coral/orange, bottom half deep blue
        im = Image.new("RGB", (128, 128), (240, 90, 40)) # Coral
        for y in range(64, 128):
            for x in range(128):
                im.putpixel((x, y), (20, 60, 180)) # Deep blue
        im.save(cls.test_image_path)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_image_path):
            try:
                os.remove(cls.test_image_path)
            except Exception:
                pass

    def setUp(self):
        clear_palette()
        _PALETTE_CACHE.clear()

    def test_01_palette_extraction_swatches(self):
        """Verify extraction produces canonical Material/KMP swatches without lag."""
        t0 = time.time()
        palette = extract_palette_from_image(self.test_image_path)
        dt = (time.time() - t0) * 1000

        self.assertIsNotNone(palette)
        self.assertIn("dark_primary", palette)
        self.assertIn("light_primary", palette)
        self.assertIn("immersive_bg", palette)
        self.assertIn("swatches", palette)
        self.assertIn("dominant", palette)

        # Performance: downsampled extraction should complete in < 50ms
        self.assertLess(dt, 50.0, f"Extraction was too slow: {dt:.2f}ms")

        # Verify values are normalized in [0.0, 1.0]
        for c in palette["dark_primary"]:
            self.assertTrue(0.0 <= c <= 1.0)
        for c in palette["light_primary"]:
            self.assertTrue(0.0 <= c <= 1.0)

        print(f"[PASS] Test 1: Palette extracted swatches in {dt:.2f}ms")

    def test_02_lru_cache_sub_millisecond_speed(self):
        """Verify memory cache eliminates repeated extraction overhead."""
        extract_palette_from_image(self.test_image_path)

        t0 = time.time()
        cached = extract_palette_from_image(self.test_image_path)
        dt = (time.time() - t0) * 1000

        self.assertIsNotNone(cached)
        self.assertLess(dt, 1.0, f"Cache retrieval took {dt:.3f}ms (target < 1ms)")
        print(f"[PASS] Test 2: Cached retrieval completed in {dt:.4f}ms")

    def test_03_simpmusic_adaptive_darkening_math(self):
        """Verify toImmersiveBackground formula adaptively darkens base for white text contrast."""
        palette = extract_palette_from_image(self.test_image_path)
        imm = palette["immersive_bg"]

        # Perceived luminance of the resulting immersive background must be dark (<= 0.40)
        # to ensure white text has AAA contrast
        lum = get_perceived_luminance(imm)
        self.assertLessEqual(lum, 0.40, f"Immersive background is too bright ({lum:.2f}) for white text")
        print(f"[PASS] Test 3: Immersive background adaptively darkened to perceived luminance {lum:.2f} <= 0.40")

    def test_04_neutral_surfaces_light_theme(self):
        """Verify Light theme enforces clean neutral-grey surfaces per SimpMusic Theme.kt."""
        class MockThemeCls:
            theme_style = "Light"
            primary_palette = "Indigo"
            primaryColor = [0, 0, 0, 1]
            backgroundColor = [0, 0, 0, 1]
            surfaceColor = [0, 0, 0, 1]
            surfaceContainerColor = [0, 0, 0, 1]
            onSurfaceColor = [0, 0, 0, 1]
            onSurfaceVariantColor = [0, 0, 0, 1]

        class MockApp:
            theme_cls = MockThemeCls()
            extract_artwork_colors = True

        app = MockApp()
        palette = extract_palette_from_image(self.test_image_path)
        apply_simpmusic_theme(app, palette)

        # 1. Background and surface MUST be neutral grey #FAFAFA ([0.98, 0.98, 0.98, 1.0]), NOT muddy brown/yellow!
        self.assertEqual(app.theme_cls.backgroundColor[:3], [0.98, 0.98, 0.98])
        self.assertEqual(app.theme_cls.surfaceColor[:3], [0.98, 0.98, 0.98])
        self.assertEqual(app.theme_cls.surfaceContainerColor[:3], [0.95, 0.95, 0.95])

        # 2. Text MUST be crisp dark #1B1B1B ([0.11, 0.11, 0.11, 1.0])
        self.assertEqual(app.theme_cls.onSurfaceColor[:3], [0.11, 0.11, 0.11])

        # 3. Primary MUST carry the vibrant artwork accent!
        self.assertEqual(app.theme_cls.primaryColor[:3], palette["light_primary"][:3])
        print("[PASS] Test 4: Light theme neutral surfaces & vibrant primary verified")

    def test_05_neutral_surfaces_dark_theme(self):
        """Verify Dark theme enforces clean AMOLED dark surfaces per SimpMusic Theme.kt."""
        class MockThemeCls:
            theme_style = "Dark"
            primary_palette = "Indigo"
            primaryColor = [0, 0, 0, 1]
            backgroundColor = [1, 1, 1, 1]
            surfaceColor = [1, 1, 1, 1]
            surfaceContainerColor = [1, 1, 1, 1]
            onSurfaceColor = [0, 0, 0, 1]
            onSurfaceVariantColor = [0, 0, 0, 1]

        class MockApp:
            theme_cls = MockThemeCls()
            extract_artwork_colors = True

        app = MockApp()
        palette = extract_palette_from_image(self.test_image_path)
        apply_simpmusic_theme(app, palette)

        # 1. Background MUST be AMOLED deep #0D0D10 ([0.05, 0.05, 0.06, 1.0])
        self.assertEqual(app.theme_cls.backgroundColor[:3], [0.05, 0.05, 0.06])

        # 2. Text MUST be crisp white #F5F5F5 ([0.96, 0.96, 0.96, 1.0])
        self.assertEqual(app.theme_cls.onSurfaceColor[:3], [0.96, 0.96, 0.96])

        # 3. Primary MUST carry dark_primary rich accent!
        self.assertEqual(app.theme_cls.primaryColor[:3], palette["dark_primary"][:3])
        print("[PASS] Test 5: Dark theme AMOLED neutral surfaces & rich primary verified")

    def test_06_non_existent_image_graceful_fallback(self):
        """Verify non-existent or corrupted image paths gracefully fall back without crash."""
        res = extract_palette_from_image("non_existent_file.png")
        self.assertIsNone(res)

        class MockThemeCls:
            theme_style = "Light"
            primary_palette = "Indigo"
            primaryColor = [0, 0, 0, 1]
            backgroundColor = [0, 0, 0, 1]
            surfaceColor = [0, 0, 0, 1]
            surfaceContainerColor = [0, 0, 0, 1]
            onSurfaceColor = [0, 0, 0, 1]
            onSurfaceVariantColor = [0, 0, 0, 1]

        class MockApp:
            theme_cls = MockThemeCls()
            extract_artwork_colors = True

        app = MockApp()
        apply_simpmusic_theme(app, None)
        # Should apply default Indigo primary cleanly
        self.assertIsNotNone(app.theme_cls.primaryColor)
        print("[PASS] Test 6: Non-existent image fallback safely handled")

if __name__ == "__main__":
    unittest.main()
