"""Settings, Audio Calibration, Storage Cache, Logging & Preference Dialogs Coordinator."""

from __future__ import annotations

import os
from typing import Any

from kivy.clock import Clock
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogHeadlineText,
    MDDialogSupportingText,
)
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemHeadlineText,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
    MDListItemTrailingIcon,
)
from kivymd.uix.scrollview import MDScrollView

from app_core.service_container import resolve_symbol
from models.database import set_setting
from services.autoeq_service import get_autoeq_curve
from services.logger import (
    app_logger,
    get_current_log_level_name,
    log_file,
    set_log_level,
)
from utils import theme_utils as theme_mod


class SettingsCoordinator:
    """Manages persisted app settings, theme toggles, equalizer curves, sleep timer & maintenance dialogs."""

    def __init__(self, app: Any):
        self.app = app

    def toggle_wifi_only(self) -> None:
        self.app.wifi_only = not self.app.wifi_only
        set_setting("wifi_only", str(self.app.wifi_only))

    def set_wifi_only(self, is_enabled: bool) -> None:
        self.app.wifi_only = is_enabled
        set_setting("wifi_only", str(self.app.wifi_only))

    def toggle_dark_mode(self) -> None:
        app = self.app
        new_style = "Dark" if app.theme_cls.theme_style == "Light" else "Light"
        app.theme_cls.theme_style = new_style
        set_setting("theme_style", new_style)
        theme_mod.apply_simpmusic_theme(app)
        app._refresh_home_header_texture()
        app._refresh_player_background_texture()
        app.update_player_animated_bg()

    def toggle_theme_style(self, is_dark: bool) -> None:
        app = self.app
        app.theme_cls.theme_style = "Dark" if is_dark else "Light"
        set_setting("theme_style", app.theme_cls.theme_style)
        theme_mod.apply_simpmusic_theme(app)
        app._refresh_home_header_texture()
        app._refresh_player_background_texture()
        app.update_player_animated_bg()

    def toggle_extract_artwork_colors(self, is_enabled=None) -> None:
        app = self.app
        app.extract_artwork_colors = (not app.extract_artwork_colors) if is_enabled is None else bool(is_enabled)
        set_setting("extract_artwork_colors", str(app.extract_artwork_colors))
        updater = resolve_symbol("update_theme_from_image", theme_mod.update_theme_from_image)
        if not app.extract_artwork_colors:
            theme_mod.clear_palette()
            app._refresh_player_background_texture()
        elif app.player_controller.active_track and getattr(app.player_controller.active_track, "album_art", None):
            updater(app.player_controller.active_track.album_art)
        app.update_player_animated_bg()

    def toggle_animated_bg(self, is_enabled=None) -> None:
        app = self.app
        app.animated_bg_enabled = (not app.animated_bg_enabled) if is_enabled is None else bool(is_enabled)
        set_setting("animated_bg_enabled", str(app.animated_bg_enabled))
        app.update_player_animated_bg()

    def toggle_sponsorblock(self) -> None:
        self.app.sponsorblock_enabled = not self.app.sponsorblock_enabled
        set_setting("sponsorblock_enabled", str(self.app.sponsorblock_enabled))

    def set_sponsorblock_enabled(self, is_enabled: bool) -> None:
        self.app.sponsorblock_enabled = is_enabled
        set_setting("sponsorblock_enabled", str(self.app.sponsorblock_enabled))

    def toggle_discord_rpc(self) -> None:
        app = self.app
        app.discord_rpc_enabled = not app.discord_rpc_enabled
        set_setting("discord_rpc_enabled", str(app.discord_rpc_enabled))
        if hasattr(app, "player_controller") and hasattr(app.player_controller, "discord_rpc"):
            if not app.discord_rpc_enabled:
                app.player_controller.discord_rpc.clear()
            else:
                track = app.player_controller.active_track
                if track and app.player_controller.is_playing:
                    app.player_controller.discord_rpc.update_track(
                        track.title, track.artist,
                        app.player_controller.current_time,
                        app.player_controller.duration,
                        True,
                    )
        app.show_toast(f"Discord RPC {'enabled' if app.discord_rpc_enabled else 'disabled'}")

    def show_crossfade_dialog(self) -> None:
        app = self.app
        options = [
            (0.0, "Off (Gapless)", "Standard immediate transition between tracks"),
            (3.0, "3 Seconds", "Recommended smooth audio overlap"),
            (5.0, "5 Seconds", "Extended gradual crossfade transition"),
            (8.0, "8 Seconds", "DJ-style long atmospheric mix"),
            (12.0, "12 Seconds", "Continuous ambient club mixing"),
        ]
        list_container = MDList()
        for sec, title, desc in options:
            def on_sel(inst, s=sec):
                app.set_crossfade_duration(s)
                if hasattr(app, "crossfade_dialog") and app.crossfade_dialog:
                    app.crossfade_dialog.dismiss()

            item = MDListItem(
                MDListItemHeadlineText(text=title),
                MDListItemSupportingText(text=desc),
                on_release=on_sel,
            )
            if abs(app.crossfade_duration - sec) < 0.1:
                item.add_widget(MDListItemTrailingIcon(icon="check"))
            list_container.add_widget(item)

        app.crossfade_dialog = MDDialog(
            MDDialogHeadlineText(text="Audio Crossfade Duration"),
            MDDialogContentContainer(list_container, orientation="vertical"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: app.crossfade_dialog.dismiss()),
            ),
        )
        app.crossfade_dialog.open()

    def set_crossfade_duration(self, seconds: float) -> None:
        app = self.app
        app.crossfade_duration = max(0.0, float(seconds))
        set_setting("crossfade_duration", str(int(app.crossfade_duration)))
        if hasattr(app, "player_controller") and app.player_controller:
            app.player_controller.set_crossfade_duration(app.crossfade_duration)
        lbl = f"{int(app.crossfade_duration)}s" if app.crossfade_duration > 0 else "Off"
        app.show_toast(f"Audio crossfade set to {lbl}")

    def apply_autoeq_profile(self, profile_name: str) -> None:
        app = self.app
        curve = get_autoeq_curve(profile_name)
        if curve:
            app.selected_autoeq_profile = profile_name
            app.selected_eq_profile = profile_name
            app.eq_bands = list(curve)
            set_setting("autoeq_profile", profile_name)
            app.apply_audio_eq()
            app.show_toast(f"Calibrated for {profile_name}")

    def adjust_lyrics_offset(self, delta: float) -> None:
        app = self.app
        app.lyrics_timing_offset = 0.0 if delta == 0.0 else round(app.lyrics_timing_offset + delta, 2)
        set_setting("lyrics_offset", str(app.lyrics_timing_offset))
        sm = app.root.ids.get("screen_manager") if (hasattr(app, "root") and app.root and hasattr(app.root, "ids")) else None
        if (sm and sm.current == "lyrics") or (hasattr(app, "lyrics_sheet") and app.lyrics_sheet):
            app.reload_lyrics_for_active_track()
        if hasattr(app, "player_controller") and app.player_controller:
            app._current_inline_lyric_index = -1
            app.on_player_time_change(None, app.player_controller.current_time)
        lbl = f"{app.lyrics_timing_offset:+.1f}s" if app.lyrics_timing_offset != 0.0 else "Synced (0.0s)"
        app.show_toast(f"Lyrics timing offset: {lbl}")

    def update_player_animated_bg(self) -> None:
        app = self.app
        try:
            if hasattr(app, "root") and app.root and hasattr(app.root, "ids"):
                sm = app.root.ids.get("screen_manager")
                if sm:
                    for sname, bg_id in (("player", "player_animated_bg"), ("lyrics", "lyrics_animated_bg")):
                        if sm.has_screen(sname):
                            scr = sm.get_screen(sname)
                            bg = scr.ids.get(bg_id)
                            if bg:
                                bg.is_active = app.animated_bg_enabled
                                bg.variation = app.animated_bg_variation
                                bg.speed = app.animated_bg_speed
                                bg.update_colors_from_theme(app)
        except Exception as e:
            app_logger.debug(f"Animated background update notice: {e}")

    def show_animated_bg_style_dialog(self) -> None:
        app = self.app
        options = [
            ("gradient", "Animated Gradient", "Continuous chromatic color flow"),
            ("ripple", "Water Ripple", "Gentle liquid ripples spreading outward"),
            ("aurora", "Soft Aurora", "Smooth harmonic drifting color waves"),
            ("off", "Disabled / Solid", "Clean static theme backdrop"),
        ]
        list_container = MDList()
        for key, title, desc in options:
            def on_select(instance, k=key, t=title):
                app.animated_bg_variation = k
                app.animated_bg_variation_label = t
                app.animated_bg_enabled = (k != "off")
                set_setting("animated_bg_variation", app.animated_bg_variation)
                set_setting("animated_bg_enabled", str(app.animated_bg_enabled))
                app.update_player_animated_bg()
                if hasattr(app, "style_dialog") and app.style_dialog:
                    app.style_dialog.dismiss()

            item = MDListItem(
                MDListItemHeadlineText(text=title),
                MDListItemSupportingText(text=desc),
                on_release=on_select,
            )
            if key == app.animated_bg_variation:
                item.add_widget(MDListItemTrailingIcon(icon="check"))
            list_container.add_widget(item)

        app.style_dialog = MDDialog(
            MDDialogHeadlineText(text="Background Animation Style"),
            MDDialogContentContainer(list_container, orientation="vertical"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: app.style_dialog.dismiss()),
            ),
        )
        app.style_dialog.open()

    def cycle_animated_bg_speed(self) -> None:
        app = self.app
        speeds = [(0.5, "Subtle (0.5x)"), (1.0, "Normal (1.0x)"), (1.8, "Dynamic (1.8x)")]
        current_idx = 1
        for i, (spd, _) in enumerate(speeds):
            if abs(app.animated_bg_speed - spd) < 0.1:
                current_idx = i
                break
        next_idx = (current_idx + 1) % len(speeds)
        app.animated_bg_speed, app.animated_bg_speed_label = speeds[next_idx]
        set_setting("animated_bg_speed", str(app.animated_bg_speed))
        app.update_player_animated_bg()
        app.show_toast(f"Animation Speed: {app.animated_bg_speed_label}")

    def show_audio_quality_dialog(self) -> None:
        app = self.app
        options = [
            ("Low (96kbps)", "Data saver"),
            ("Normal (160kbps)", "Standard quality"),
            ("High (320kbps)", "Best MP3 quality"),
            ("Lossless (FLAC)", "Highest fidelity"),
        ]
        list_container = MDList()
        for title, desc in options:
            def on_select(instance, t=title):
                app.selected_audio_quality = t
                set_setting("selected_audio_quality", app.selected_audio_quality)
                if hasattr(app, "quality_dialog") and app.quality_dialog:
                    app.quality_dialog.dismiss()

            item = MDListItem(
                MDListItemHeadlineText(text=title),
                MDListItemSupportingText(text=desc),
                on_release=on_select,
            )
            if title == app.selected_audio_quality:
                item.add_widget(MDListItemTrailingIcon(icon="check"))
            list_container.add_widget(item)

        app.quality_dialog = MDDialog(
            MDDialogHeadlineText(text="Select Audio Quality"),
            MDDialogContentContainer(list_container, orientation="vertical"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: app.quality_dialog.dismiss()),
            ),
        )
        app.quality_dialog.open()

    def show_toast(self, msg: str) -> None:
        try:
            from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

            MDSnackbar(
                MDSnackbarText(text=msg),
                y="24dp",
                pos_hint={"center_x": 0.5},
                size_hint_x=0.85,
                duration=2.5,
            ).open()
        except Exception:
            app_logger.info("Toast: %s", msg)
            print(f"[Toast] {msg}")

    def refresh_cache_size(self) -> None:
        try:
            from utils.media_utils import get_cache_size_mb

            mb = get_cache_size_mb(self.app.cache_dir)
            self.app.cache_size_label = f"{mb:.1f} MB cached • Tap to clear"
        except Exception:
            self.app.cache_size_label = "Tap to clear cache"

    def show_clear_cache_dialog(self) -> None:
        app = self.app
        app.cache_dialog = MDDialog(
            MDDialogHeadlineText(text="Clear Temporary Cache?"),
            MDDialogSupportingText(
                text="This will delete temporary stream chunks and thumbnail caches to free storage.\n"
                     "Your downloaded offline songs will be safely preserved."
            ),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: app.cache_dialog.dismiss()),
                MDButton(MDButtonText(text="CLEAR"), style="text", on_release=lambda x: (app.cache_dialog.dismiss(), app.execute_clear_cache())),
            ),
        )
        app.cache_dialog.open()

    def execute_clear_cache(self) -> None:
        app = self.app
        try:
            from utils.media_utils import clear_cache_files

            removed, bytes_freed = clear_cache_files(app.cache_dir)
            freed_mb = bytes_freed / (1024 * 1024)
            app.refresh_cache_size()
            app.show_toast(f"Cleared {removed} files ({freed_mb:.1f} MB freed)")
        except Exception as e:
            app_logger.error(f"[execute_clear_cache error]: {e}")
            app.show_toast("Cache cleared")

    def show_provider_selector_dialog(self) -> None:
        app = self.app
        items = [
            ("all", "Unified (All Sources)", "Smart arbitration across all platforms"),
            ("youtube", "YouTube Music", "Direct YouTube audio extraction"),
            ("spotify", "Spotify", "Spotify search metadata & track matches"),
            ("jiosaavn", "JioSaavn", "Direct JioSaavn high-fidelity Indian music streams"),
        ]
        dlist = MDList()
        sheet = None

        def select_prov(prov_key, prov_label):
            app.selected_music_provider = prov_key
            app.selected_music_provider_label = prov_label
            set_setting("default_music_provider", prov_key)
            app.show_toast(f"Default provider: {prov_label}")
            if sheet:
                sheet.dismiss()

        for key, label, sub in items:
            is_active = (key == app.selected_music_provider)
            dlist.add_widget(
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="check-circle" if is_active else "radiobox-blank",
                        theme_icon_color="Custom",
                        icon_color=app.theme_cls.primaryColor if is_active else app.theme_cls.onSurfaceVariantColor,
                    ),
                    MDListItemHeadlineText(text=label),
                    MDListItemSupportingText(text=sub),
                    on_release=lambda x, k=key, l=label: select_prov(k, l),
                )
            )

        scroll = MDScrollView(size_hint_y=None, height="240dp")
        scroll.add_widget(dlist)
        sheet = MDDialog(
            MDDialogHeadlineText(text="Default Music Provider"),
            MDDialogContentContainer(scroll),
            MDDialogButtonContainer(MDButton(MDButtonText(text="CLOSE"), style="text", on_release=lambda x: sheet.dismiss())),
        )
        sheet.open()

    def resync_offline_library_action(self) -> None:
        self.app.scan_and_load_offline_songs(auto_play=False, show_screen=True)

    def show_about_dialog(self) -> None:
        dialog = MDDialog(
            MDDialogHeadlineText(text="About Melodify"),
            MDDialogSupportingText(
                text="Melodify v2.4.0 (SimpMusic Engine v0.7.0 Parity)\n\n"
                     "An open-source, Material 3 mobile music player featuring unified YouTube, "
                     "Spotify, and JioSaavn multi-source streaming, offline library indexing, "
                     "AutoEq frequency compensation, and synchronized LRCLIB lyrics.\n\n"
                     "Built with Python, Kivy & KivyMD 2.0."
            ),
            MDDialogButtonContainer(MDButton(MDButtonText(text="CLOSE"), style="text", on_release=lambda x: dialog.dismiss())),
        )
        dialog.open()

    def show_logs_dialog(self) -> None:
        lines = []
        if os.path.exists(log_file):
            try:
                with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()[-30:]
            except Exception:
                pass
        text_content = "".join(lines) if lines else "No session logs recorded yet."
        if len(text_content) > 1800:
            text_content = text_content[-1800:]

        scroll = MDScrollView(size_hint_y=None, height="240dp")
        scroll.add_widget(
            MDLabel(
                text=text_content,
                font_style="Body",
                role="small",
                adaptive_height=True,
                padding=["8dp", "8dp", "8dp", "8dp"],
            )
        )
        dialog = MDDialog(
            MDDialogHeadlineText(text="Application Logs"),
            MDDialogContentContainer(scroll),
            MDDialogButtonContainer(MDButton(MDButtonText(text="CLOSE"), style="text", on_release=lambda x: dialog.dismiss())),
        )
        dialog.open()

    def show_log_level_dialog(self) -> None:
        app = self.app
        cur_level = get_current_log_level_name()
        levels = [
            ("DEBUG", "Verbose diagnostic tracing for deep troubleshooting"),
            ("INFO", "Standard operational events and state milestones"),
            ("WARNING", "Recoverable non-fatal anomalies and warnings"),
            ("ERROR", "Operation failures and caught exceptions"),
            ("CRITICAL", "Fatal errors and application crash events only"),
        ]
        dlist = MDList()
        dialog = None

        def select_level(lvl_name):
            set_log_level(lvl_name)
            set_setting("log_level", lvl_name)
            app.show_toast(f"Log level: {lvl_name}")
            app_logger.info("Switched active 5-level log threshold to: %s", lvl_name)
            if dialog:
                dialog.dismiss()

        for lvl_name, desc in levels:
            is_active = (lvl_name == cur_level)
            dlist.add_widget(
                MDListItem(
                    MDListItemHeadlineText(text=f"{lvl_name} {'(Active)' if is_active else ''}"),
                    MDListItemSupportingText(text=desc),
                    on_release=lambda x, l=lvl_name: select_level(l),
                )
            )

        dialog = MDDialog(
            MDDialogHeadlineText(text="Logging Severity Level"),
            MDDialogSupportingText(text="Configure minimum severity level for application logs:"),
            MDDialogContentContainer(dlist),
            MDDialogButtonContainer(MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: dialog.dismiss())),
        )
        dialog.open()

    def show_sleep_timer_dialog(self) -> None:
        app = self.app
        options = [
            (0, "Off", "Cancel active timer"),
            (15, "15 minutes", "Stop playback in 15 minutes"),
            (30, "30 minutes", "Stop playback in 30 minutes"),
            (45, "45 minutes", "Stop playback in 45 minutes"),
            (60, "1 hour", "Stop playback in 60 minutes"),
            (-1, "End of track", "Stop when current track finishes"),
        ]
        dlist = MDList()
        dialog = None

        def select_timer(mins, label):
            if hasattr(app, "_sleep_timer_event") and app._sleep_timer_event:
                app._sleep_timer_event.cancel()
                app._sleep_timer_event = None
            app._sleep_timer_end_of_track = False

            if mins == 0:
                app.show_toast("Sleep timer turned off")
            elif mins == -1:
                app._sleep_timer_end_of_track = True
                app.show_toast("Playback will stop at end of track")
            else:
                app._sleep_timer_event = Clock.schedule_once(lambda dt: app.player_controller.pause(), mins * 60)
                app.show_toast(f"Sleep timer set for {label}")
            if dialog:
                dialog.dismiss()

        for mins, label, sub in options:
            dlist.add_widget(
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="timer-outline",
                        theme_icon_color="Custom",
                        icon_color=app.theme_cls.primaryColor,
                    ),
                    MDListItemHeadlineText(text=label),
                    MDListItemSupportingText(text=sub),
                    on_release=lambda x, m=mins, l=label: select_timer(m, l),
                )
            )

        scroll = MDScrollView(size_hint_y=None, height="240dp")
        scroll.add_widget(dlist)
        dialog = MDDialog(
            MDDialogHeadlineText(text="Sleep Timer"),
            MDDialogContentContainer(scroll),
            MDDialogButtonContainer(MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: dialog.dismiss())),
        )
        dialog.open()

    def show_reset_settings_dialog(self) -> None:
        app = self.app
        dialog = None

        def do_reset():
            app.theme_cls.theme_style = "Light"
            set_setting("theme_style", "Light")
            app.wifi_only = True
            set_setting("wifi_only", "True")
            app.selected_audio_quality = "High (320kbps)"
            set_setting("selected_audio_quality", "High (320kbps)")
            app.sponsorblock_enabled = True
            set_setting("sponsorblock_enabled", "True")
            app.crossfade_duration = 3.0
            set_setting("crossfade_duration", "3")
            app.player_controller.set_crossfade_duration(3.0)
            app.animated_bg_enabled = True
            set_setting("animated_bg_enabled", "True")
            app.extract_artwork_colors = True
            set_setting("extract_artwork_colors", "True")
            app.discord_rpc_enabled = True
            set_setting("discord_rpc_enabled", "True")
            app.selected_music_provider = "all"
            app.selected_music_provider_label = "Unified (All Sources)"
            set_setting("default_music_provider", "all")
            app.show_toast("Settings restored to defaults")
            dialog.dismiss()

        dialog = MDDialog(
            MDDialogHeadlineText(text="Reset Settings?"),
            MDDialogSupportingText(
                text="This will reset theme style to Light, streaming quality to 320kbps, crossfade to 3s, and re-enable Wi-Fi and SponsorBlock defaults."
            ),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: dialog.dismiss()),
                MDButton(MDButtonText(text="RESET"), style="text", on_release=lambda x: do_reset()),
            ),
        )
        dialog.open()

    def apply_eq_profile(self, profile_name: str) -> None:
        app = self.app
        app.selected_eq_profile = profile_name
        if profile_name in app.EQ_PRESETS:
            app.eq_bands = list(app.EQ_PRESETS[profile_name])
        elif profile_name in app.HEADPHONE_PROFILES:
            app.eq_bands = list(app.HEADPHONE_PROFILES[profile_name])
        app.apply_audio_eq()
        app.show_toast(f"Applied '{profile_name}' EQ")

    def on_eq_slider_change(self, band_index: int, value: float) -> None:
        app = self.app
        val = round(float(value), 1)
        if 0 <= band_index < len(app.eq_bands) and abs(app.eq_bands[band_index] - val) >= 0.1:
            new_bands = list(app.eq_bands)
            new_bands[band_index] = val
            app.eq_bands = new_bands
            if app.selected_eq_profile in app.EQ_PRESETS and app.EQ_PRESETS[app.selected_eq_profile] != new_bands:
                app.selected_eq_profile = "Custom"
            elif app.selected_eq_profile in app.HEADPHONE_PROFILES and app.HEADPHONE_PROFILES[app.selected_eq_profile] != new_bands:
                app.selected_eq_profile = "Custom"
            app.apply_audio_eq()

    def reset_eq(self) -> None:
        app = self.app
        app.selected_eq_profile = "Flat"
        app.eq_bands = [0.0] * 10
        app.eq_reverb = False
        app.apply_audio_eq()
        app.show_toast("Equalizer reset to Flat (0 dB)")

    def toggle_eq_reverb(self, active: bool) -> None:
        app = self.app
        app.eq_reverb = active
        app.apply_audio_eq()
        app.show_toast(f"Reverb {'enabled' if active else 'disabled'}")

    def apply_audio_eq(self) -> None:
        app = self.app
        if hasattr(app, "player_controller") and app.player_controller:
            app.player_controller.set_equalizer(app.eq_bands, app.eq_reverb)

    def show_autoeq_profile_dialog(self) -> None:
        app = self.app
        scroll = MDScrollView(size_hint_y=None, height="320dp")
        list_container = MDList()

        for p in app.EQ_PRESETS.keys():
            def on_sel(instance, prof=p):
                app.apply_eq_profile(prof)
                if app.autoeq_dialog:
                    app.autoeq_dialog.dismiss()

            item = MDListItem(
                MDListItemLeadingIcon(icon="tune-vertical"),
                MDListItemHeadlineText(text=p),
                MDListItemSupportingText(text="Genre Sound Preset"),
                on_release=on_sel,
            )
            if p == app.selected_eq_profile:
                item.add_widget(MDListItemTrailingIcon(icon="check"))
            list_container.add_widget(item)

        for h in app.HEADPHONE_PROFILES.keys():
            if h == "Default Flat":
                continue

            def on_h_sel(instance, prof=h):
                app.apply_eq_profile(prof)
                if app.autoeq_dialog:
                    app.autoeq_dialog.dismiss()

            item = MDListItem(
                MDListItemLeadingIcon(icon="headphones"),
                MDListItemHeadlineText(text=h),
                MDListItemSupportingText(text="Headphone Calibration Curve"),
                on_release=on_h_sel,
            )
            if h == app.selected_eq_profile:
                item.add_widget(MDListItemTrailingIcon(icon="check"))
            list_container.add_widget(item)

        scroll.add_widget(list_container)
        app.autoeq_dialog = MDDialog(
            MDDialogHeadlineText(text="Select Equalizer Profile"),
            MDDialogContentContainer(scroll, orientation="vertical"),
            MDDialogButtonContainer(MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: app.autoeq_dialog.dismiss())),
        )
        app.autoeq_dialog.open()

    def show_auth_dialog(self, provider: str) -> None:
        app = self.app
        app.auth_dialog = MDDialog(
            MDDialogHeadlineText(text=f"Connect {provider}"),
            MDDialogSupportingText(text=f"Would you like to authenticate with {provider} to sync your music and playlists?"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: app.auth_dialog.dismiss()),
                MDButton(MDButtonText(text="CONNECT"), style="text", on_release=lambda x: app.auth_dialog.dismiss()),
            ),
        )
        app.auth_dialog.open()
