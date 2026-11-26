"""Application Bootstrap Coordinator (Fonts, Textures, Build, Warmup & Prewarming)."""

from __future__ import annotations

import os
import threading
import time
from typing import Any

from kivy.clock import Clock
from kivy.core.text import DEFAULT_FONT, LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.logger import Logger as kivy_logger
from kivy.metrics import dp
from kivy.utils import platform

from app_core.service_container import resolve_symbol
from app_core.state import SEARCH_PLACEHOLDERS
from models.database import set_setting
from services.logger import app_logger
from services.telemetry_service import get_telemetry
from utils import media_utils
from utils.theme_utils import apply_simpmusic_theme, get_active_palette, update_theme_from_image


def resolve_and_register_system_fonts():
    """
    Resolves and registers cross-platform Unicode fonts supporting Latin, Devanagari (Hindi),
    Gurmukhi (Punjabi), CJK, Cyrillic, and extended symbols across all target platforms.

    Resolution priority:
    1. Bundled application fonts: fonts/*.ttf inside app folder (packaged in APK via buildozer.spec)
    2. Android system fonts: /system/fonts/ (NotoSans-Regular, Roboto-Regular, DroidSansFallback, etc.)
    3. Windows system fonts: C:\\Windows\\Fonts\\ (segoeui.ttf, arialuni.ttf, arial.ttf)
    4. Linux system fonts: /usr/share/fonts/
    """
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(app_dir, "fonts", "NotoSans-Regular.ttf"),
        os.path.join(app_dir, "fonts", "Roboto-Regular.ttf"),
    ]

    if platform == "android":
        candidates.extend([
            "/system/fonts/NotoSans-Regular.ttf",
            "/system/fonts/Roboto-Regular.ttf",
            "/system/fonts/DroidSansFallback.ttf",
            "/system/fonts/NotoSansDevanagari-Regular.ttf",
            "/system/fonts/NotoSansGurmukhi-Regular.ttf",
        ])
    elif platform == "win":
        windir = os.environ.get("WINDIR", "C:\\Windows")
        candidates.extend([
            os.path.join(windir, "Fonts", "segoeui.ttf"),
            os.path.join(windir, "Fonts", "arialuni.ttf"),
            os.path.join(windir, "Fonts", "arial.ttf"),
            os.path.join(windir, "Fonts", "calibri.ttf"),
        ])
    elif platform == "linux":
        candidates.extend([
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        ])
    elif platform == "macosx":
        candidates.extend([
            "/System/Library/Fonts/SFNS.ttf",
            "/Library/Fonts/Arial Unicode.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ])

    candidates.extend([
        "/system/fonts/Roboto-Regular.ttf",
        "/system/fonts/NotoSans-Regular.ttf",
        os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "segoeui.ttf"),
        os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "arial.ttf"),
    ])

    resolved = None
    for fp in candidates:
        if fp and os.path.exists(fp):
            resolved = fp
            break

    if resolved:
        try:
            LabelBase.register(DEFAULT_FONT, fn_regular=resolved)
            LabelBase.register("Roboto", fn_regular=resolved)
            LabelBase.register("AppUnicodeFont", fn_regular=resolved)
            return resolved, "AppUnicodeFont"
        except Exception as e:
            kivy_logger.warning("Font: Registration error: %s", e)

    return None, DEFAULT_FONT


class AppBootstrap:
    """Coordinates theme styling, gradient textures, KV tree load, and cooperative startup warmup."""

    def __init__(self, app: Any):
        self.app = app
        self._search_ph_index = -1

    def refresh_home_header_texture(self, *args) -> None:
        """Rebuilds the Home header gradient texture (primaryContainer -> background)."""
        app = self.app
        try:
            from kivy.graphics.texture import Texture

            primary = list(app.theme_cls.primaryColor)
            bottom = list(app.theme_cls.backgroundColor)
            if app.theme_cls.theme_style == "Dark":
                top = [c * 0.3 for c in primary[:3]]
            else:
                top = [c * 0.15 + 0.85 for c in primary[:3]]
            steps = 192
            buf = bytearray()
            for i in range(steps - 1, -1, -1):
                t = i / (steps - 1)
                buf += bytes((
                    int(255 * max(0.0, min(1.0, top[0] + (bottom[0] - top[0]) * t))),
                    int(255 * max(0.0, min(1.0, top[1] + (bottom[1] - top[1]) * t))),
                    int(255 * max(0.0, min(1.0, top[2] + (bottom[2] - top[2]) * t))),
                    255,
                ))
            tex = Texture.create(size=(1, steps), colorfmt="rgba")
            tex.blit_buffer(bytes(buf), colorfmt="rgba", bufferfmt="ubyte")
            tex.min_filter = "linear"
            tex.mag_filter = "linear"
            app.home_header_texture = tex
        except Exception as e:
            app_logger.debug(f"home header gradient error: {e}")

    def refresh_player_background_texture(self, *args) -> None:
        """Rebuilds the Now Playing palette gradient texture (artwork dominant -> #121212)."""
        app = self.app
        try:
            from kivy.graphics.texture import Texture

            palette = get_active_palette()
            if palette and getattr(app, "extract_artwork_colors", True):
                if "dark_primary" in palette and palette["dark_primary"]:
                    top = list(palette["dark_primary"])
                elif "dominant" in palette and palette["dominant"]:
                    top = list(palette["dominant"])
                else:
                    top = [0.18, 0.20, 0.35]
            else:
                top = [0.16, 0.18, 0.32]

            lum = 0.299 * top[0] + 0.587 * top[1] + 0.114 * top[2]
            if lum > 0.65:
                top = [c * 0.65 for c in top]
            elif lum < 0.12:
                top = [min(1.0, c * 1.6 + 0.12) for c in top]

            bottom = [0.0706, 0.0706, 0.0706]
            steps = 256
            buf = bytearray()
            for i in range(steps):
                v = i / (steps - 1)
                if v <= 0.38:
                    r, g, b = bottom
                else:
                    t = (v - 0.38) / 0.62
                    smooth_t = t * t * (3.0 - 2.0 * t)
                    r = bottom[0] + (top[0] - bottom[0]) * smooth_t
                    g = bottom[1] + (top[1] - bottom[1]) * smooth_t
                    b = bottom[2] + (top[2] - bottom[2]) * smooth_t
                buf += bytes((
                    int(255 * max(0.0, min(1.0, r))),
                    int(255 * max(0.0, min(1.0, g))),
                    int(255 * max(0.0, min(1.0, b))),
                    255,
                ))

            tex = Texture.create(size=(1, steps), colorfmt="rgba")
            tex.blit_buffer(bytes(buf), colorfmt="rgba", bufferfmt="ubyte")
            tex.min_filter = "linear"
            tex.mag_filter = "linear"
            app.player_background_texture = tex
        except Exception as e:
            app_logger.debug(f"player background gradient error: {e}")

    def build_root(self):
        """Apply persisted Material 3 palette, font styles, and load the root KV tree."""
        app = self.app
        from models.database import get_setting

        saved_theme = get_setting("theme_style", "Light")
        app.theme_cls.theme_style = saved_theme
        app.theme_cls.primary_palette = "Indigo"
        apply_simpmusic_theme(app)
        self.refresh_home_header_texture()
        self.refresh_player_background_texture()

        if app.resolved_unicode_font_name:
            for cat in app.theme_cls.font_styles:
                if cat != "Icon":
                    for role in app.theme_cls.font_styles[cat]:
                        app.theme_cls.font_styles[cat][role]["font-name"] = app.resolved_unicode_font_name

        app.ui_mode = app.UI_MODE_NEW
        set_setting("ui_mode", app.UI_MODE_NEW)
        app._ui_loading_overlay = None
        app._ui_mode_switching = False

        # Register KivyMD 2.0 internal KV rules and custom screens/components before loading main.kv
        from kivymd.uix.bottomsheet import (  # noqa: F401
            MDBottomSheet,
            MDBottomSheetDragHandle,
            MDBottomSheetDragHandleButton,
            MDBottomSheetDragHandleTitle,
        )
        from kivymd.uix.button import MDButton, MDButtonText  # noqa: F401
        from kivymd.uix.dialog import (  # noqa: F401
            MDDialog,
            MDDialogButtonContainer,
            MDDialogContentContainer,
            MDDialogHeadlineText,
            MDDialogSupportingText,
        )
        from kivymd.uix.filemanager import MDFileManager  # noqa: F401
        from kivymd.uix.label import MDLabel  # noqa: F401
        from kivymd.uix.list import (  # noqa: F401
            MDList,
            MDListItem,
            MDListItemHeadlineText,
            MDListItemLeadingAvatar,
            MDListItemLeadingIcon,
            MDListItemSupportingText,
            MDListItemTrailingIcon,
        )
        from kivymd.uix.navigationbar import (  # noqa: F401
            MDNavigationBar,
            MDNavigationItem,
            MDNavigationItemIcon,
            MDNavigationItemLabel,
        )
        from kivymd.uix.scrollview import MDScrollView  # noqa: F401
        import views.components  # noqa: F401
        import views.screens  # noqa: F401

        root = Builder.load_file(os.path.join("views", "main.kv"))
        Window.bind(on_keyboard=app.on_keyboard)
        Window.bind(on_request_close=app.on_request_close)
        get_telemetry().record_startup_stage("build_done")
        return root

    def on_start(self) -> None:
        """Start telemetry observers (non-headless) and cooperative splash warmup pipeline."""
        app = self.app
        get_telemetry().record_startup_stage("on_start")
        get_telemetry().sample_memory(min_interval_seconds=0.0)
        if os.environ.get("KIVY_HEADLESS") != "1" or os.environ.get("KYM_FORCE_TELEMETRY") == "1":
            Clock.schedule_interval(app._telemetry_sample_frame, 0)
            Clock.schedule_interval(app._telemetry_sample_memory, 2.0)
        if os.environ.get("KIVY_HEADLESS") != "1":
            if platform in ("win", "macosx", "linux"):
                Window.size = (360, 640)
        Clock.schedule_once(lambda dt: app.start_warmup_pipeline(), 0.02)

    def start_warmup_pipeline(self) -> None:
        """Progressive cooperative pre-warm pipeline from Splash to interactive Home."""
        app = self.app
        if not hasattr(app, "root") or not app.root or not hasattr(app.root, "ids") or "screen_manager" not in app.root.ids:
            Clock.schedule_once(lambda dt: app.start_warmup_pipeline(), 0.05)
            return
        sm = app.root.ids.screen_manager
        if os.environ.get("KIVY_HEADLESS") == "1":
            app._stage_1_populate_home(0)
            app._stage_2_populate_library_and_history(0)
            app._stage_3_apply_initial_theme(0)
            if sm.has_screen("splash"):
                sm.get_screen("splash").opacity = 0.0
            app._splash_completed = True
            sm.current = "home"
            app.sync_nav_bar("home")
            get_telemetry().mark_cold_startup_complete()
            return

        if not sm.has_screen("splash"):
            app._stage_1_populate_home(0)
            app._stage_2_populate_library_and_history(0)
            app._stage_3_apply_initial_theme(0)
            app._stage_4_background_tasks(0)
            sm.current = "home"
            return

        splash = sm.get_screen("splash")
        progress = getattr(splash.ids, "splash_progress", None)
        status = getattr(splash.ids, "splash_status_label", None)
        logo_card = getattr(splash.ids, "logo_card", None)

        from kivy.animation import Animation

        if logo_card:
            pulse = (
                Animation(size=(dp(116), dp(116)), radius=[dp(58)] * 4, duration=0.6, t="in_out_quad")
                + Animation(size=(dp(108), dp(108)), radius=[dp(54)] * 4, duration=0.6, t="in_out_quad")
            )
            pulse.repeat = True
            pulse.start(logo_card)
            app._splash_pulse_anim = pulse

        def set_status(val, text):
            if progress:
                progress.value = val
            if status:
                status.text = text

        def step_1(dt):
            set_status(15, "Initializing audio engine...")
            Clock.schedule_once(step_2, 0.08)

        def step_2(dt):
            set_status(35, "Indexing music library...")
            app.load_search_history_from_db()
            Clock.schedule_once(step_3, 0.06)

        def step_3(dt):
            set_status(55, "Preparing interface...")
            app.populate_home_screen_data()
            if sm.has_screen("library"):
                lib_screen = sm.get_screen("library")
                if "library_list" in lib_screen.ids:
                    lib_screen.ids.library_list.data = [
                        {
                            "title": track.title,
                            "artist": track.artist,
                            "artwork": track.album_art,
                            "track_obj": track,
                        }
                        for track in app.playlist_model.tracks[:20]
                    ]
            Clock.schedule_once(step_4, 0.10)

        def step_4(dt):
            set_status(75, "Warming up music player...")
            try:
                sm.get_screen("player")
                app.ensure_player_carousel()
            except Exception as e:
                app_logger.debug(f"Player warmup error: {e}")
            Clock.schedule_once(step_5, 0.10)

        def step_5(dt):
            set_status(90, "Preparing screens...")
            Clock.schedule_once(step_6, 0.05)

        def step_6(dt):
            set_status(100, "Ready!")
            Clock.schedule_once(step_7_finish, 0.12)

        def step_7_finish(dt):
            if hasattr(app, "_splash_pulse_anim") and app._splash_pulse_anim and logo_card:
                try:
                    app._splash_pulse_anim.stop(logo_card)
                    Animation.stop_all(logo_card)
                except Exception:
                    pass
                app._splash_pulse_anim = None

            app._stage_3_apply_initial_theme(0)
            get_telemetry().record_startup_stage("splash_ready")

            fade_anim = Animation(opacity=0.0, duration=0.3, t="out_quad")

            def _on_fade_complete(*args):
                try:
                    Animation.stop_all(splash)
                except Exception:
                    pass
                app._splash_completed = True
                get_telemetry().mark_cold_startup_complete()
                if sm.current == "splash":
                    from kivy.uix.screenmanager import NoTransition

                    prev_trans = sm.transition
                    sm.transition = NoTransition()
                    sm.current = "home"
                    sm.transition = prev_trans
                    app.sync_nav_bar("home")
                    Clock.schedule_once(app._stage_4_background_tasks, 0.2)
                    self.deferred_screen_prewarm(sm)

            fade_anim.bind(on_complete=lambda *args: Clock.schedule_once(_on_fade_complete, 0))
            fade_anim.start(splash)

        Clock.schedule_once(step_1, 0.05)

    def deferred_screen_prewarm(self, sm, names=None, index: int = 0) -> None:
        """Instantiates one non-critical screen per idle tick after splash dismissal."""
        if names is None:
            names = [
                "settings", "favorites", "notifications", "playlist", "artist",
                "album", "analytics", "recently_played", "browse", "podcasts",
                "mood", "equalizer", "listen_together",
            ]
        if index >= len(names):
            return
        try:
            if not sm.has_screen(names[index]):
                sm.get_screen(names[index])
        except Exception as e:
            app_logger.debug(f"Deferred screen warmup {names[index]}: {e}")
        Clock.schedule_once(lambda dt: self.deferred_screen_prewarm(sm, names, index + 1), 1.5)

    def stage_1_populate_home(self, dt=None) -> None:
        self.app.populate_home_screen_data()

    def stage_2_populate_library_and_history(self, dt=None) -> None:
        self.app.load_search_history_from_db()
        self.app.refresh_library_data()
        Clock.schedule_interval(self.cycle_search_placeholder, 3.0)

    def cycle_search_placeholder(self, *args) -> None:
        app = self.app
        try:
            if hasattr(app, "root") and app.root and "screen_manager" in app.root.ids:
                if app.root.ids.screen_manager.current != "search":
                    return
            self._search_ph_index = (self._search_ph_index + 1) % len(SEARCH_PLACEHOLDERS)
            app.search_placeholder = SEARCH_PLACEHOLDERS[self._search_ph_index]
        except Exception:
            pass

    def start_idle_prewarming(self, dt=None) -> None:
        self._prewarm_queue = [
            "player", "settings", "playlist", "album", "artist", "equalizer",
            "notifications", "recently_played", "analytics", "listen_together",
            "podcasts", "browse", "mood", "auth", "favorites", "wrapped",
        ]
        Clock.schedule_once(self.prewarm_next_screen, 0.1)

    def prewarm_next_screen(self, dt=None) -> None:
        app = self.app
        if not getattr(self, "_prewarm_queue", None):
            return
        if hasattr(app, "root") and app.root and hasattr(app.root, "ids") and "screen_manager" in app.root.ids:
            sm = app.root.ids.screen_manager
            next_name = self._prewarm_queue.pop(0)
            if not sm.has_screen(next_name):
                try:
                    sm.get_screen(next_name)
                except Exception as e:
                    app_logger.debug(f"Pre-warm skipped for '{next_name}': {e}")
            if self._prewarm_queue:
                Clock.schedule_once(self.prewarm_next_screen, 0.12)

    def stage_3_apply_initial_theme(self, dt=None) -> None:
        app = self.app
        updater = resolve_symbol("update_theme_from_image", update_theme_from_image)
        if (
            app.extract_artwork_colors
            and app.player_controller.active_track
            and getattr(app.player_controller.active_track, "album_art", None)
        ):
            updater(app.player_controller.active_track.album_art)
        else:
            apply_simpmusic_theme(app)
        app.update_player_animated_bg()

    def stage_4_background_tasks(self, dt=None) -> None:
        app = self.app
        if os.environ.get("KIVY_HEADLESS") == "1":
            return
        ensure_dl = resolve_symbol("ensure_artworks_downloaded", media_utils.ensure_artworks_downloaded)
        ensure_dl(app.playlist_model.tracks, on_track_updated=app.on_artwork_downloaded)

        def _bg_scan():
            time.sleep(0.5)
            app.scan_and_load_offline_songs(auto_play=False, show_screen=False)

        threading.Thread(target=_bg_scan, daemon=True).start()

        if len(app.playlist_model.tracks) < 15:
            def _bg_trending():
                time.sleep(1.0)
                app._fetch_trending_tracks()

            threading.Thread(target=_bg_trending, daemon=True).start()

        def _bg_cache_limit():
            time.sleep(3.0)
            enforce = resolve_symbol("enforce_max_cache_size", media_utils.enforce_max_cache_size)
            enforce(max_size_mb=5000)

        threading.Thread(target=_bg_cache_limit, daemon=True).start()

        def _bg_podcasts_warmup():
            time.sleep(2.0)
            Clock.schedule_once(lambda _dt: app.load_podcasts_data(), 0)

        threading.Thread(target=_bg_podcasts_warmup, daemon=True).start()
