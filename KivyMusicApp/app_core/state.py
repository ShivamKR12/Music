"""Application State Schema, Presets & Persisted Settings Hydration."""

from __future__ import annotations

from typing import Any, Dict

from models.database import get_setting
from services.autoeq_service import get_autoeq_curve


EQ_PRESETS: Dict[str, list[float]] = {
    "Flat": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Bass Boost": [7.0, 6.0, 4.5, 2.5, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Vocal Booster": [-2.0, -1.0, 0.0, 2.0, 4.0, 5.0, 4.0, 2.0, 0.0, -1.0],
    "Rock": [5.0, 4.0, 2.0, -1.0, -2.0, -1.0, 1.0, 3.0, 4.5, 5.0],
    "Electronic": [6.0, 5.5, 2.0, 0.0, -2.0, 1.5, 2.0, 3.5, 5.0, 5.5],
    "Classical": [4.0, 3.5, 3.0, 2.5, -1.0, -1.0, 0.0, 2.0, 3.0, 3.5],
    "Hip-Hop": [7.0, 6.0, 3.0, 1.0, -1.0, -1.0, 1.0, 2.0, 3.0, 4.0],
    "Acoustic": [3.0, 2.5, 2.0, 1.0, 2.0, 2.5, 3.0, 3.5, 3.0, 2.0],
    "Pop": [-1.0, 1.5, 3.0, 4.0, 3.0, 1.0, -1.0, -1.5, 1.0, 2.0],
    "Treble Booster": [-2.0, -2.0, -1.0, 0.0, 1.0, 3.0, 5.0, 7.0, 8.0, 9.0],
}

HEADPHONE_PROFILES: Dict[str, list[float]] = {
    "Default Flat": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Apple AirPods Pro": [1.5, 1.0, -0.5, 0.0, 1.0, 2.0, 1.5, -1.0, 2.0, 1.0],
    "Sony WH-1000XM4/XM5": [-2.0, -1.5, 0.0, 1.5, 2.0, 2.5, 3.0, 1.5, 0.5, -1.0],
    "Sennheiser HD 650": [4.0, 3.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.5, 2.5, 3.0],
    "Bose QuietComfort 45": [0.0, -1.0, -1.5, 0.5, 1.5, 2.0, 1.0, -0.5, 1.5, 2.0],
    "Samsung Galaxy Buds Pro": [1.0, 0.5, 0.0, -0.5, 1.0, 1.5, 2.0, 1.0, 0.0, 0.5],
    "Audio-Technica ATH-M50x": [-1.5, -1.0, 0.0, 1.0, 0.5, 0.0, -1.0, 1.5, 2.5, 2.0],
    "Beyerdynamic DT 990": [2.0, 1.5, 0.5, 0.0, 0.0, 1.0, 0.5, -3.0, -4.0, -2.0],
}

PROVIDER_LABELS: Dict[str, str] = {
    "all": "Unified (All Sources)",
    "youtube": "YouTube Music",
    "spotify": "Spotify",
    "jiosaavn": "JioSaavn",
}

SEARCH_PLACEHOLDERS = [
    "Search for songs...",
    "Search for artists...",
    "Search for albums...",
    "Search for playlists...",
    "Search for podcasts...",
]

ANIMATED_BG_VARIATION_LABELS: Dict[str, str] = {
    "gradient": "Animated Gradient",
    "ripple": "Water Ripple",
    "aurora": "Soft Aurora",
    "off": "Disabled / Solid",
}

ANIMATED_BG_SPEED_LABELS: Dict[float, str] = {
    0.5: "Subtle (0.5x)",
    1.0: "Normal (1.0x)",
    1.8: "Dynamic (1.8x)",
}


class AppState:
    """Centralizes persisted settings hydration and mutable dialog/UI runtime handles."""

    def __init__(self, app: Any):
        self.app = app
        self.search_placeholder_index: int = -1

    def init_ui_handles(self) -> None:
        """Initialize transient dialog, sheet, and navigation runtime attributes on app."""
        app = self.app
        app.file_manager = None
        app.dialog = None
        app.quality_dialog = None
        app.cache_dialog = None
        app.autoeq_dialog = None
        app.auth_dialog = None
        app.bottom_sheet = None
        app.queue_sheet = None
        app.style_dialog = None
        app.listen_together_dialog = None
        app.listen_together_last_broadcast = 0.0
        app.screen_history = []
        app.active_search_provider = "all"
        app._active_spotify_dialog = None

    def hydrate_settings_from_db(self) -> None:
        """Restore persisted application settings safely from SQLite into observable app properties."""
        app = self.app

        saved_theme = get_setting("theme_style", "Light")
        if saved_theme not in ("Light", "Dark"):
            saved_theme = "Light"
        app.theme_cls.theme_style = saved_theme

        saved_extract = get_setting("extract_artwork_colors", "True")
        app.extract_artwork_colors = str(saved_extract).lower() in ("true", "1")

        saved_anim_bg = get_setting("animated_bg_enabled", "True")
        app.animated_bg_enabled = str(saved_anim_bg).lower() in ("true", "1")

        saved_variation = get_setting("animated_bg_variation", "gradient")
        app.animated_bg_variation = saved_variation
        app.animated_bg_variation_label = ANIMATED_BG_VARIATION_LABELS.get(
            saved_variation, "Animated Gradient"
        )

        saved_speed = get_setting("animated_bg_speed", "1.0")
        try:
            app.animated_bg_speed = float(saved_speed)
        except Exception:
            app.animated_bg_speed = 1.0
        app.animated_bg_speed_label = ANIMATED_BG_SPEED_LABELS.get(
            round(app.animated_bg_speed, 1), f"{app.animated_bg_speed}x"
        )

        app.selected_audio_quality = get_setting("selected_audio_quality", "High (320kbps)")

        saved_wifi = get_setting("wifi_only", "True")
        app.wifi_only = str(saved_wifi).lower() in ("true", "1")

        saved_sponsor = get_setting("sponsorblock_enabled", "True")
        app.sponsorblock_enabled = str(saved_sponsor).lower() in ("true", "1")

        saved_crossfade = get_setting("crossfade_duration", "3")
        try:
            app.crossfade_duration = float(saved_crossfade)
        except Exception:
            app.crossfade_duration = 3.0

        saved_autoeq = get_setting("autoeq_profile", "Harman In-Ear Target")
        if saved_autoeq and saved_autoeq != "None":
            app.selected_autoeq_profile = saved_autoeq
            curve = get_autoeq_curve(saved_autoeq)
            if curve:
                app.selected_eq_profile = saved_autoeq
                app.eq_bands = list(curve)

        saved_discord = get_setting("discord_rpc_enabled", "True")
        app.discord_rpc_enabled = str(saved_discord).lower() in ("true", "1")

        saved_offset = get_setting("lyrics_offset", "0.0")
        try:
            app.lyrics_timing_offset = float(saved_offset)
        except Exception:
            app.lyrics_timing_offset = 0.0

        saved_prov = get_setting("default_music_provider", "all")
        app.selected_music_provider = saved_prov
        app.selected_music_provider_label = PROVIDER_LABELS.get(saved_prov, "Unified (All Sources)")
