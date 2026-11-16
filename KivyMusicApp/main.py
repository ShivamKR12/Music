import os
import sys
from kivy.config import Config
from kivy.utils import platform

is_headless = os.environ.get("KIVY_HEADLESS") == "1"
if platform in ('win', 'macosx', 'linux'):
    if is_headless:
        Config.set('graphics', 'width', '360')
        Config.set('graphics', 'height', '640')
        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'fullscreen', False)
    else:
        Config.set('graphics', 'width', '1024')
        Config.set('graphics', 'height', '720')
        Config.set('graphics', 'resizable', True)
        Config.set('graphics', 'fullscreen', False)

# Cross-platform Unicode font resolver for Android, Windows, Linux, and macOS
from kivy.core.text import LabelBase, DEFAULT_FONT

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
    app_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        # 1. Bundled app fonts
        os.path.join(app_dir, "fonts", "NotoSans-Regular.ttf"),
        os.path.join(app_dir, "fonts", "Roboto-Regular.ttf"),
    ]

    # 2. Operating System specifics
    if platform == 'android':
        candidates.extend([
            "/system/fonts/NotoSans-Regular.ttf",
            "/system/fonts/Roboto-Regular.ttf",
            "/system/fonts/DroidSansFallback.ttf",
            "/system/fonts/NotoSansDevanagari-Regular.ttf",
            "/system/fonts/NotoSansGurmukhi-Regular.ttf",
        ])
    elif platform == 'win':
        windir = os.environ.get("WINDIR", "C:\\Windows")
        candidates.extend([
            os.path.join(windir, "Fonts", "segoeui.ttf"),
            os.path.join(windir, "Fonts", "arialuni.ttf"),
            os.path.join(windir, "Fonts", "arial.ttf"),
            os.path.join(windir, "Fonts", "calibri.ttf"),
        ])
    elif platform == 'linux':
        candidates.extend([
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        ])
    elif platform == 'macosx':
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
            print(f"[Font registration error]: {e}")
            
    return None, DEFAULT_FONT

RESOLVED_FONT_PATH, RESOLVED_FONT_NAME = resolve_and_register_system_fonts()
import re
import time
import threading
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation

# Thread-safe & re-entrancy safe Animation._update patch for Python 3.12+ (prevents 'dictionary changed size during iteration')
def _update(self, dt):
    widgets = self._widgets
    transition = self._transition
    calculate = self._calculate
    for uid in list(widgets.keys()):
        if uid not in widgets:
            continue
        anim_data = widgets[uid]
        widget = anim_data.get('widget')

        from kivy.weakproxy import WeakProxy
        if isinstance(widget, WeakProxy) and not len(dir(widget)):
            widgets.pop(uid, None)
            self._clock_uninstall()
            if not widgets:
                self._unregister()
            continue

        if anim_data.get('time') is None:
            anim_data['time'] = 0.
        else:
            anim_data['time'] += dt

        if self._duration:
            progress = min(1., anim_data['time'] / self._duration)
        else:
            progress = 1
        t = transition(progress)

        for key, values in list(anim_data.get('properties', {}).items()):
            if uid not in widgets or key not in anim_data.get('properties', {}):
                continue
            a, b = values
            value = calculate(a, b, t)
            try:
                setattr(widget, key, value)
            except Exception:
                pass

        try:
            self.dispatch('on_progress', widget, progress)
        except Exception:
            pass

        if progress >= 1.:
            try:
                self.stop(widget)
            except Exception:
                pass

Animation._update = _update
Animation._safe_anim_update = _update

def _anim_getattr(self, name):
    if name in ('_update', '_safe_anim_update', 'safe_update'):
        return self._update
    raise AttributeError(f"'Animation' object has no attribute '{name}'")

Animation.__getattr__ = _anim_getattr
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import (
    MDDialog, 
    MDDialogHeadlineText, 
    MDDialogSupportingText, 
    MDDialogContentContainer,
    MDDialogButtonContainer
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.bottomsheet import (
    MDBottomSheet, 
    MDBottomSheetDragHandle, 
    MDBottomSheetDragHandleTitle, 
    MDBottomSheetDragHandleButton
)
from kivymd.uix.navigationbar import (
    MDNavigationBar, 
    MDNavigationItem, 
    MDNavigationItemIcon, 
    MDNavigationItemLabel
)
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import (
    MDList, 
    MDListItem, 
    MDListItemLeadingIcon,
    MDListItemLeadingAvatar,
    MDListItemHeadlineText,
    MDListItemSupportingText,
    MDListItemTrailingIcon
)
from kivymd.icon_definitions import md_icons
# Register Discord icon fallback to gamepad/controller symbol if missing in Material font
if "discord" not in md_icons:
    md_icons["discord"] = md_icons.get("controller", md_icons.get("gamepad", "chat"))

from models.database import (
    init_db,
    add_track,
    get_all_tracks,
    get_playlist_tracks,
    get_dynamic_playlist_tracks,
    get_on_repeat,
    get_heavy_rotation,
    get_forgotten_favorites,
    get_daily_mix,
    add_playlist,
    get_all_playlists,
    delete_playlist,
    add_track_to_playlist,
    remove_track_from_playlist,
    is_favorite,
    toggle_favorite,
    add_search_history,
    get_search_history,
    clear_search_history,
    get_continue_listening,
    get_recently_added,
    update_track_artwork,
    update_local_track_path,
    get_setting,
    set_setting,
    get_all_settings,
    save_cache_payload,
    load_cache_payload,
)
from services.autoeq_service import get_autoeq_curve, get_all_autoeq_profiles
from services.lyrics_service import fetch_lyrics_async, get_cached_lyrics
from services.listen_together_service import ListenTogetherService
from models.track_model import TrackModel, PlaylistModel
from controllers.player_controller import PlayerController
from views.screens import (
    HomeScreen, 
    SearchScreen, 
    LibraryScreen, 
    SettingsScreen, 
    PlayerScreen, 
    FavoritesScreen
)
from views.components import (
    TrackListItem,
    DirectionalHorizontalScrollView,
    DirectionalHorizontalRecycleView,
    ArtistAlbumCard,
    MarqueeLabel,
)
from utils.theme_utils import update_theme_from_image
from services.logger import app_logger, init_logging
logger = app_logger
from utils.media_utils import (
    enforce_max_cache_size,
    extract_video_id,
    fetch_youtube_metadata,
    get_thumbnail_path,
    download_artwork,
    ensure_artworks_downloaded,
)

class MusicApp(MDApp):
    player_controller = ObjectProperty(None)
    selected_audio_quality = StringProperty("High (320kbps)")
    selected_eq_profile = StringProperty("Flat")
    active_playlist_name = StringProperty("Favorites")
    active_playlist_artwork = StringProperty("album_art2.png")
    active_playlist_info = StringProperty("0 tracks")
    active_playlist_tracks = ListProperty([])

    # 10-Band Equalizer & Calibration properties
    eq_bands = ListProperty([0.0] * 10)
    eq_reverb = BooleanProperty(False)
    eq_bass_boost = NumericProperty(0.0)

    # Listen Together Real-Time Sync properties
    listen_together_active = BooleanProperty(False)
    listen_together_room_id = StringProperty("")
    listen_together_role = StringProperty("idle")
    listen_together_status = StringProperty("Disconnected")
    listen_together_members = ListProperty([])

    # Presets & Calibration Models
    EQ_PRESETS = {
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

    HEADPHONE_PROFILES = {
        "Default Flat": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Apple AirPods Pro": [1.5, 1.0, -0.5, 0.0, 1.0, 2.0, 1.5, -1.0, 2.0, 1.0],
        "Sony WH-1000XM4/XM5": [-2.0, -1.5, 0.0, 1.5, 2.0, 2.5, 3.0, 1.5, 0.5, -1.0],
        "Sennheiser HD 650": [4.0, 3.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.5, 2.5, 3.0],
        "Bose QuietComfort 45": [0.0, -1.0, -1.5, 0.5, 1.5, 2.0, 1.0, -0.5, 1.5, 2.0],
        "Samsung Galaxy Buds Pro": [1.0, 0.5, 0.0, -0.5, 1.0, 1.5, 2.0, 1.0, 0.0, 0.5],
        "Audio-Technica ATH-M50x": [-1.5, -1.0, 0.0, 1.0, 0.5, 0.0, -1.0, 1.5, 2.5, 2.0],
        "Beyerdynamic DT 990": [2.0, 1.5, 0.5, 0.0, 0.0, 1.0, 0.5, -3.0, -4.0, -2.0],
    }

    # Dynamic theme, font and background customization properties
    resolved_unicode_font_name = StringProperty(RESOLVED_FONT_NAME)
    resolved_unicode_font_path = StringProperty(RESOLVED_FONT_PATH or "")
    extract_artwork_colors = BooleanProperty(True)
    animated_bg_enabled = BooleanProperty(True)
    animated_bg_variation = StringProperty("gradient")
    animated_bg_variation_label = StringProperty("Animated Gradient")
    animated_bg_speed = NumericProperty(1.0)
    animated_bg_speed_label = StringProperty("Normal (1.0x)")
    wifi_only = BooleanProperty(True)
    sponsorblock_enabled = BooleanProperty(True)
    selected_autoeq_profile = StringProperty("Harman In-Ear Target")
    crossfade_duration = NumericProperty(3.0)
    discord_rpc_enabled = BooleanProperty(True)
    lyrics_timing_offset = NumericProperty(0.0)

    # Dynamic Artist, Album, Podcasts & Favorites Screen Properties
    active_artist_name = StringProperty("Artist Profile")
    active_artist_art = StringProperty("album_art.png")
    active_artist_info = StringProperty("Artist Collection")
    active_artist_tracks = ListProperty([])

    active_album_name = StringProperty("Trending Hits")
    active_album_artist = StringProperty("Popular Artists")
    active_album_art = StringProperty("album_art.png")
    active_album_info = StringProperty("Album Collection")
    active_album_tracks = ListProperty([])

    podcast_featured_title = StringProperty("Huberman Lab")
    podcast_featured_desc = StringProperty("Science & science-based tools for everyday life and high performance.")
    podcast_featured_art = StringProperty("album_art.png")
    podcast_featured_track = ObjectProperty(None, allownone=True)
    podcast_tracks = ListProperty([])

    favorites_info = StringProperty("0 tracks • 0 min")
    favorites_top_art = StringProperty("album_art.png")

    # Responsive Desktop Layout & Ergonomics
    is_desktop_layout = BooleanProperty(False)
    desktop_panel_open = BooleanProperty(False)
    desktop_panel_tab = StringProperty("lyrics")
    active_tab_name = StringProperty("home")
    current_volume = NumericProperty(1.0)

    @property
    def cache_dir(self):
        from utils.media_utils import get_cache_dir
        return get_cache_dir()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        init_logging()
        app_logger.info("Initializing MusicApp components...")
        self.file_manager = None
        self.dialog = None
        self.quality_dialog = None
        self.cache_dialog = None
        self.autoeq_dialog = None
        self.auth_dialog = None
        self.bottom_sheet = None
        self.queue_sheet = None
        self.style_dialog = None
        self.listen_together_dialog = None
        self.listen_together_last_broadcast = 0.0
        self.screen_history = []
        self.active_search_provider = "all"
        self._active_spotify_dialog = None
        
        # Listen Together Synchronization Service
        self.listen_together_service = ListenTogetherService()
        self.listen_together_service.on_state_changed = self.on_listen_together_state_changed
        self.listen_together_service.on_members_updated = self.on_listen_together_members_updated
        self.listen_together_service.on_playback_sync_received = self.on_listen_together_playback_sync
        self.listen_together_service.on_toast_requested = self.show_toast

        # MVC Initialization
        init_db()

        # Restore user settings from SQLite database
        saved_theme = get_setting("theme_style", "Light")
        if saved_theme not in ("Light", "Dark"):
            saved_theme = "Light"
        self.theme_cls.theme_style = saved_theme
        
        saved_extract = get_setting("extract_artwork_colors", "True")
        self.extract_artwork_colors = (str(saved_extract).lower() in ("true", "1"))
        
        saved_anim_bg = get_setting("animated_bg_enabled", "True")
        self.animated_bg_enabled = (str(saved_anim_bg).lower() in ("true", "1"))
        
        saved_variation = get_setting("animated_bg_variation", "gradient")
        self.animated_bg_variation = saved_variation
        var_labels = {
            "gradient": "Animated Gradient",
            "ripple": "Water Ripple",
            "aurora": "Soft Aurora",
            "off": "Disabled / Solid"
        }
        self.animated_bg_variation_label = var_labels.get(saved_variation, "Animated Gradient")
        
        saved_speed = get_setting("animated_bg_speed", "1.0")
        try:
            self.animated_bg_speed = float(saved_speed)
        except Exception:
            self.animated_bg_speed = 1.0
        spd_labels = {0.5: "Subtle (0.5x)", 1.0: "Normal (1.0x)", 1.8: "Dynamic (1.8x)"}
        self.animated_bg_speed_label = spd_labels.get(round(self.animated_bg_speed, 1), f"{self.animated_bg_speed}x")
        
        saved_quality = get_setting("selected_audio_quality", "High (320kbps)")
        self.selected_audio_quality = saved_quality
        
        saved_wifi = get_setting("wifi_only", "True")
        self.wifi_only = (str(saved_wifi).lower() in ("true", "1"))
        
        saved_sponsor = get_setting("sponsorblock_enabled", "True")
        self.sponsorblock_enabled = (str(saved_sponsor).lower() in ("true", "1"))

        saved_crossfade = get_setting("crossfade_duration", "3")
        try:
            self.crossfade_duration = float(saved_crossfade)
        except Exception:
            self.crossfade_duration = 3.0

        saved_autoeq = get_setting("autoeq_profile", "Harman In-Ear Target")
        if saved_autoeq and saved_autoeq != "None":
            self.selected_autoeq_profile = saved_autoeq

        saved_discord = get_setting("discord_rpc_enabled", "True")
        self.discord_rpc_enabled = (str(saved_discord).lower() in ("true", "1"))

        saved_offset = get_setting("lyrics_offset", "0.0")
        try:
            self.lyrics_timing_offset = float(saved_offset)
        except Exception:
            self.lyrics_timing_offset = 0.0

        self.playlist_model = PlaylistModel()
        self.player_controller = PlayerController()
        self.player_controller.set_playlist(self.playlist_model)
        self.player_controller.set_crossfade_duration(self.crossfade_duration)
        
        # Set default track
        if self.playlist_model.tracks:
            self.player_controller.set_track(self.playlist_model.tracks[0])
            
        self.player_controller.bind(active_track=self.on_active_track_change)
        self.player_controller.bind(is_playing=self.on_player_playing_change)

    def on_player_playing_change(self, instance, is_playing):
        """Broadcast state to Listen Together room if hosting."""
        if hasattr(self, "listen_together_service") and self.listen_together_service.is_host and self.listen_together_service.is_connected:
            self.broadcast_listen_together_state()

    def on_active_track_change(self, instance, track):
        """Automatically harmonize Material You palette with new track album art, sync room, and update lyrics sheet if open."""
        if track and hasattr(track, "album_art") and track.album_art:
            if self.extract_artwork_colors:
                update_theme_from_image(track.album_art)
        self.update_player_animated_bg()
        if hasattr(self, "lyrics_sheet") and self.lyrics_sheet and (self.lyrics_sheet.state == "open" or getattr(self.lyrics_sheet, "status", None) == "opening_with_animation"):
            self.reload_lyrics_for_active_track()
        if hasattr(self, "listen_together_service") and self.listen_together_service.is_host and self.listen_together_service.is_connected:
            self.broadcast_listen_together_state()

    def toggle_wifi_only(self):
        """Toggle download over Wi-Fi only and persist."""
        self.wifi_only = not self.wifi_only
        set_setting("wifi_only", str(self.wifi_only))

    def set_wifi_only(self, is_enabled: bool):
        """Set download over Wi-Fi only and persist."""
        self.wifi_only = is_enabled
        set_setting("wifi_only", str(self.wifi_only))

    def toggle_dark_mode(self):
        """Toggle between Light and Dark Material Design 3 theme styles and persist."""
        new_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        self.theme_cls.theme_style = new_style
        set_setting("theme_style", new_style)
        if self.extract_artwork_colors and self.player_controller.active_track:
            update_theme_from_image(self.player_controller.active_track.album_art)
        self.update_player_animated_bg()

    def toggle_theme_style(self, is_dark: bool):
        """Explicitly set theme style from boolean and persist."""
        self.theme_cls.theme_style = "Dark" if is_dark else "Light"
        set_setting("theme_style", self.theme_cls.theme_style)
        if self.extract_artwork_colors and self.player_controller.active_track:
            update_theme_from_image(self.player_controller.active_track.album_art)
        self.update_player_animated_bg()

    def toggle_extract_artwork_colors(self, is_enabled=None):
        """Toggle dynamic color extraction from album artwork and persist."""
        if is_enabled is None:
            self.extract_artwork_colors = not self.extract_artwork_colors
        else:
            self.extract_artwork_colors = bool(is_enabled)
        set_setting("extract_artwork_colors", str(self.extract_artwork_colors))
        if not self.extract_artwork_colors:
            self.theme_cls.path_to_wallpaper = ""
            self.theme_cls.primary_palette = "Indigo"
        elif self.player_controller.active_track and getattr(self.player_controller.active_track, "album_art", None):
            update_theme_from_image(self.player_controller.active_track.album_art)
        self.update_player_animated_bg()

    def toggle_animated_bg(self, is_enabled=None):
        """Toggle animated background presence in Player screen and persist."""
        if is_enabled is None:
            self.animated_bg_enabled = not self.animated_bg_enabled
        else:
            self.animated_bg_enabled = bool(is_enabled)
        set_setting("animated_bg_enabled", str(self.animated_bg_enabled))
        self.update_player_animated_bg()

    def toggle_sponsorblock(self):
        """Toggle SponsorBlock skip non-music segments and persist."""
        self.sponsorblock_enabled = not self.sponsorblock_enabled
        set_setting("sponsorblock_enabled", str(self.sponsorblock_enabled))

    def set_sponsorblock_enabled(self, is_enabled: bool):
        """Set SponsorBlock skip non-music segments and persist."""
        self.sponsorblock_enabled = is_enabled
        set_setting("sponsorblock_enabled", str(self.sponsorblock_enabled))

    def toggle_discord_rpc(self):
        """Toggle Discord Rich Presence broadcasting and persist."""
        self.discord_rpc_enabled = not self.discord_rpc_enabled
        set_setting("discord_rpc_enabled", str(self.discord_rpc_enabled))
        if hasattr(self, "player_controller") and hasattr(self.player_controller, "discord_rpc"):
            if not self.discord_rpc_enabled:
                self.player_controller.discord_rpc.clear()
            else:
                track = self.player_controller.active_track
                if track and self.player_controller.is_playing:
                    self.player_controller.discord_rpc.update_track(
                        track.title, track.artist,
                        self.player_controller.current_time,
                        self.player_controller.duration,
                        True
                    )
        self.show_toast(f"Discord RPC {'enabled' if self.discord_rpc_enabled else 'disabled'}")

    def show_crossfade_dialog(self):
        """Displays dialog to select DJ-style crossfade duration between tracks."""
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
                self.set_crossfade_duration(s)
                if hasattr(self, "crossfade_dialog") and self.crossfade_dialog:
                    self.crossfade_dialog.dismiss()
            is_sel = (abs(self.crossfade_duration - sec) < 0.1)
            item = MDListItem(
                MDListItemHeadlineText(text=title),
                MDListItemSupportingText(text=desc),
                on_release=on_sel
            )
            if is_sel:
                item.add_widget(MDListItemTrailingIcon(icon="check"))
            list_container.add_widget(item)

        self.crossfade_dialog = MDDialog(
            MDDialogHeadlineText(text="Audio Crossfade Duration"),
            MDDialogContentContainer(
                list_container,
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="CANCEL"),
                    style="text",
                    on_release=lambda x: self.crossfade_dialog.dismiss(),
                ),
            ),
        )
        self.crossfade_dialog.open()

    def set_crossfade_duration(self, seconds: float):
        """Sets crossfade duration in seconds, applies to audio engine, and persists."""
        self.crossfade_duration = max(0.0, float(seconds))
        set_setting("crossfade_duration", str(int(self.crossfade_duration)))
        if hasattr(self, "player_controller") and self.player_controller:
            self.player_controller.set_crossfade_duration(self.crossfade_duration)
        lbl = f"{int(self.crossfade_duration)}s" if self.crossfade_duration > 0 else "Off"
        self.show_toast(f"Audio crossfade set to {lbl}")

    def apply_autoeq_profile(self, profile_name: str):
        """Applies an AutoEq headphone calibration curve to the 10-band equalizer."""
        curve = get_autoeq_curve(profile_name)
        if curve:
            self.selected_autoeq_profile = profile_name
            self.selected_eq_profile = profile_name
            self.eq_bands = list(curve)
            set_setting("autoeq_profile", profile_name)
            self.apply_audio_eq()
            self.show_toast(f"Calibrated for {profile_name}")

    def adjust_lyrics_offset(self, delta: float):
        """Adjusts synchronized lyrics timing offset in seconds (+/-) and persists."""
        if delta == 0.0:
            self.lyrics_timing_offset = 0.0
        else:
            self.lyrics_timing_offset = round(self.lyrics_timing_offset + delta, 2)
        set_setting("lyrics_offset", str(self.lyrics_timing_offset))
        if hasattr(self, "lyrics_sheet") and self.lyrics_sheet:
            self.reload_lyrics_for_active_track()
        lbl = f"{self.lyrics_timing_offset:+.1f}s" if self.lyrics_timing_offset != 0.0 else "Synced (0.0s)"
        self.show_toast(f"Lyrics timing offset: {lbl}")

    def update_player_animated_bg(self):
        """Synchronize animated background state and theme colors across views."""
        try:
            if hasattr(self, "root") and self.root and hasattr(self.root, "ids"):
                sm = self.root.ids.get("screen_manager")
                if sm and sm.has_screen("player"):
                    player_screen = sm.get_screen("player")
                    bg = player_screen.ids.get("player_animated_bg")
                    if bg:
                        bg.is_active = self.animated_bg_enabled
                        bg.variation = self.animated_bg_variation
                        bg.speed = self.animated_bg_speed
                        bg.update_colors_from_theme(self)
        except Exception as e:
            app_logger.debug(f"Animated background update notice: {e}")

    def show_animated_bg_style_dialog(self):
        """Display dialog to select animated background visual style and persist choice."""
        options = [
            ("gradient", "Animated Gradient", "Continuous chromatic color flow"),
            ("ripple", "Water Ripple", "Gentle liquid ripples spreading outward"),
            ("aurora", "Soft Aurora", "Smooth harmonic drifting color waves"),
            ("off", "Disabled / Solid", "Clean static theme backdrop"),
        ]
        
        list_container = MDList()
        for key, title, desc in options:
            def on_select(instance, k=key, t=title):
                self.animated_bg_variation = k
                self.animated_bg_variation_label = t
                if k == "off":
                    self.animated_bg_enabled = False
                else:
                    self.animated_bg_enabled = True
                set_setting("animated_bg_variation", self.animated_bg_variation)
                set_setting("animated_bg_enabled", str(self.animated_bg_enabled))
                self.update_player_animated_bg()
                if hasattr(self, "style_dialog") and self.style_dialog:
                    self.style_dialog.dismiss()
                
            is_selected = (key == self.animated_bg_variation)
            item = MDListItem(
                MDListItemHeadlineText(text=title),
                MDListItemSupportingText(text=desc),
                on_release=on_select
            )
            if is_selected:
                item.add_widget(MDListItemTrailingIcon(icon="check"))
            list_container.add_widget(item)
            
        self.style_dialog = MDDialog(
            MDDialogHeadlineText(text="Background Animation Style"),
            MDDialogContentContainer(
                list_container,
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="CANCEL"),
                    style="text",
                    on_release=lambda x: self.style_dialog.dismiss(),
                ),
            ),
        )
        self.style_dialog.open()

    def cycle_animated_bg_speed(self):
        """Cycle animation speed between Subtle (0.5x), Normal (1.0x), and Dynamic (1.8x)."""
        speeds = [
            (0.5, "Subtle (0.5x)"),
            (1.0, "Normal (1.0x)"),
            (1.8, "Dynamic (1.8x)"),
        ]
        current_idx = 1
        for i, (spd, _) in enumerate(speeds):
            if abs(self.animated_bg_speed - spd) < 0.1:
                current_idx = i
                break
        next_idx = (current_idx + 1) % len(speeds)
        self.animated_bg_speed, self.animated_bg_speed_label = speeds[next_idx]
        set_setting("animated_bg_speed", str(self.animated_bg_speed))
        self.update_player_animated_bg()
        self.show_toast(f"Animation Speed: {self.animated_bg_speed_label}")

    def clear_search_input(self):
        """Clears text field in search screen and resets search results."""
        try:
            if hasattr(self, "root") and self.root:
                sm = self.root.ids.get("screen_manager")
                if sm and sm.has_screen("search"):
                    screen = sm.get_screen("search")
                    if "search_input" in screen.ids:
                        screen.ids.search_input.text = ""
            self.clear_search_results()
        except Exception as e:
            app_logger.debug(f"clear_search_input error: {e}")

    def get_greeting(self) -> str:
        """Context-aware greeting for the Home Screen header."""
        from datetime import datetime
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Good morning"
        elif 12 <= hour < 17:
            return "Good afternoon"
        else:
            return "Good evening"

    def build(self):
        saved_theme = get_setting("theme_style", "Light")
        self.theme_cls.theme_style = saved_theme
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.dynamic_color = True

        # Apply resolved unicode font across all KivyMD typography styles
        if self.resolved_unicode_font_name:
            for cat in self.theme_cls.font_styles:
                if cat != "Icon":
                    for role in self.theme_cls.font_styles[cat]:
                        self.theme_cls.font_styles[cat][role]["font-name"] = self.resolved_unicode_font_name

        root = Builder.load_file(os.path.join("views", "main.kv"))
        Window.bind(on_keyboard=self.on_keyboard)
        Window.bind(on_request_close=self.on_request_close)
        return root

    def on_request_close(self, *args):
        """Intercept window close requests to perform smooth exit sequence."""
        if not getattr(self, "_is_exiting", False):
            self.smooth_exit()
            return True
        return False

    def smooth_exit(self):
        """Gracefully fade out audio and UI before stopping the application."""
        if getattr(self, "_is_exiting", False):
            return
        self._is_exiting = True

        # 1. Smoothly fade out audio playback
        if hasattr(self, "player_controller") and self.player_controller:
            try:
                self.player_controller.fade_out_and_stop(duration=0.25)
            except Exception as e:
                app_logger.debug(f"Audio fadeout error: {e}")

        # 2. Smoothly fade out window / UI opacity
        from kivy.animation import Animation
        if hasattr(self, "root") and self.root:
            anim = Animation(opacity=0.0, duration=0.25, t="out_quad")
            def _finish_exit(*args):
                Clock.schedule_once(lambda dt: self.stop(), 0)
            anim.bind(on_complete=_finish_exit)
            anim.start(self.root)
            Clock.schedule_once(lambda dt: self.stop(), 0.35)
        else:
            self.stop()

    def switch_screen(self, screen_name: str):
        """Navigate to screen, lazy-instantiating on demand, and push to navigation stack."""
        if hasattr(self, "root") and self.root and hasattr(self.root, "ids") and "screen_manager" in self.root.ids:
            sm = self.root.ids.screen_manager
            # Ensure target screen is instantiated on-demand via LazyScreenManager
            if not sm.has_screen(screen_name):
                try:
                    sm.get_screen(screen_name)
                except Exception as e:
                    app_logger.error(f"Failed to instantiate screen '{screen_name}': {e}")
                    return
            if sm.has_screen(screen_name) and sm.current != screen_name:
                self.screen_history.append(sm.current)
                if sm.width == 0 or sm.height == 0:
                    from kivy.uix.screenmanager import NoTransition
                    prev_trans = sm.transition
                    sm.transition = NoTransition()
                    sm.current = screen_name
                    sm.transition = prev_trans
                else:
                    sm.current = screen_name
                self.sync_nav_bar(screen_name)
                if screen_name == "player":
                    self.ensure_player_carousel()
                elif screen_name == "recently_played":
                    self.load_recently_played_data()
                elif screen_name == "analytics":
                    self.load_analytics_data()
                elif screen_name == "podcasts":
                    self.load_podcasts_data()

    def go_back(self, target=None):
        """Unified back action for UI back buttons and Android hardware back key."""
        if hasattr(self, "lyrics_sheet") and self.lyrics_sheet and (self.lyrics_sheet.state == "open" or getattr(self.lyrics_sheet, "status", None) == "opening_with_animation"):
            if hasattr(self, "_lyrics_event") and self._lyrics_event:
                self._lyrics_event.cancel()
                self._lyrics_event = None
            if hasattr(self, "_lyrics_scroll_anim") and self._lyrics_scroll_anim:
                try:
                    self._lyrics_scroll_anim.stop(self._lyrics_scroll_view)
                except Exception:
                    pass
                self._lyrics_scroll_anim = None
            self.lyrics_sheet.set_state("close")
            return
        if hasattr(self, "queue_sheet") and self.queue_sheet and (self.queue_sheet.state == "open" or getattr(self.queue_sheet, "status", None) == "opening_with_animation"):
            self.queue_sheet.set_state("close")
            return
        if hasattr(self, "bottom_sheet") and self.bottom_sheet and (self.bottom_sheet.state == "open" or getattr(self.bottom_sheet, "status", None) == "opening_with_animation"):
            self.bottom_sheet.set_state("close")
            return
        if hasattr(self, "dialog") and self.dialog and getattr(self.dialog, "_is_open", False):
            self.dialog.dismiss()
            return
        if hasattr(self, "quality_dialog") and self.quality_dialog and getattr(self.quality_dialog, "_is_open", False):
            self.quality_dialog.dismiss()
            return
        if hasattr(self, "cache_dialog") and self.cache_dialog and getattr(self.cache_dialog, "_is_open", False):
            self.cache_dialog.dismiss()
            return
        if hasattr(self, "autoeq_dialog") and self.autoeq_dialog and getattr(self.autoeq_dialog, "_is_open", False):
            self.autoeq_dialog.dismiss()
            return
        if hasattr(self, "auth_dialog") and self.auth_dialog and getattr(self.auth_dialog, "_is_open", False):
            self.auth_dialog.dismiss()
            return
        if hasattr(self, "root") and self.root and hasattr(self.root, "ids") and "screen_manager" in self.root.ids:
            sm = self.root.ids.screen_manager
            dest = target
            if not dest:
                if self.screen_history:
                    dest = self.screen_history.pop()
                    while dest == "splash" and self.screen_history:
                        dest = self.screen_history.pop()
                    if dest == "splash":
                        dest = "home"
                else:
                    dest = "home"
            sm.current = dest
            self.sync_nav_bar(dest)

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Handle hardware keys, including Android back button (Key 27 / Escape)."""
        if key == 27:
            if hasattr(self, "root") and self.root and hasattr(self.root, "ids") and "screen_manager" in self.root.ids:
                sm = self.root.ids.screen_manager
                has_overlay = (
                    (hasattr(self, "lyrics_sheet") and self.lyrics_sheet and (self.lyrics_sheet.state == "open" or getattr(self.lyrics_sheet, "status", None) == "opening_with_animation")) or
                    (hasattr(self, "queue_sheet") and self.queue_sheet and (self.queue_sheet.state == "open" or getattr(self.queue_sheet, "status", None) == "opening_with_animation")) or
                    (hasattr(self, "bottom_sheet") and self.bottom_sheet and (self.bottom_sheet.state == "open" or getattr(self.bottom_sheet, "status", None) == "opening_with_animation")) or
                    (hasattr(self, "dialog") and self.dialog and getattr(self.dialog, "_is_open", False)) or
                    (hasattr(self, "quality_dialog") and self.quality_dialog and getattr(self.quality_dialog, "_is_open", False)) or
                    (hasattr(self, "cache_dialog") and self.cache_dialog and getattr(self.cache_dialog, "_is_open", False)) or
                    (hasattr(self, "autoeq_dialog") and self.autoeq_dialog and getattr(self.autoeq_dialog, "_is_open", False)) or
                    (hasattr(self, "auth_dialog") and self.auth_dialog and getattr(self.auth_dialog, "_is_open", False))
                )
                if has_overlay or sm.current != "home":
                    self.go_back()
                    return True
            return False

    def on_switch_tabs(
        self,
        bar,
        item,
        item_icon: str,
        item_text: str,
    ):
        """Handle tab transitions from the Material 3 Navigation Bar."""
        mapping = {
            "Home": "home",
            "Search": "search",
            "Library": "library",
        }
        target = mapping.get(item_text, item_text.lower())
        if hasattr(self, "root") and self.root and hasattr(self.root, "ids") and "screen_manager" in self.root.ids:
            self.switch_screen(target)

    def sync_nav_bar(self, screen_name: str):
        """Keep the MDNavigationBar active indicator in sync with the ScreenManager."""
        self.active_tab_name = screen_name
        mapping = {
            "home": "Home",
            "search": "Search",
            "library": "Library",
        }
        target_text = mapping.get(screen_name, screen_name.capitalize())
        if hasattr(self, "root") and self.root and hasattr(self.root, "ids") and "bottom_nav" in self.root.ids:
            nav = self.root.ids.bottom_nav
            for item in nav.children:
                if hasattr(item, "text") and item.text == target_text:
                    nav.set_active_item(item)
                    return
        
    def on_start(self):
        """Cooperative pre-warm pipeline: animates splash screen while pre-rendering all screens."""
        from kivy.clock import Clock
        from kivy.core.window import Window
        if os.environ.get("KIVY_HEADLESS") != "1":
            Window.bind(on_resize=lambda win, w, h: self.check_responsive_layout(w))
            if platform not in ('android', 'ios'):
                from utils.desktop_utils import DesktopKeyboardManager, setup_desktop_window
                self.keyboard_manager = DesktopKeyboardManager(self)
                setup_desktop_window(self)
            self.check_responsive_layout(Window.width)
        Clock.schedule_once(lambda dt: self.start_warmup_pipeline(), 0.02)

    def start_warmup_pipeline(self):
        """
        Progressive, frame-budgeted cooperative pre-warm pipeline:
        - Displays animated splash screen immediately on launch with dynamic status.
        - Spreads screen instantiation, carousel setup, and background tasks across animation frames.
        - Pre-warms 100% of application screens in memory so all user interactions are 0ms instant.
        - Fades smoothly into Home screen once initialization is complete.
        """
        from kivy.clock import Clock
        if not hasattr(self, "root") or not self.root or not hasattr(self.root, "ids") or "screen_manager" not in self.root.ids:
            Clock.schedule_once(lambda dt: self.start_warmup_pipeline(), 0.05)
            return
        sm = self.root.ids.screen_manager
        self.check_responsive_layout()
        if os.environ.get("KIVY_HEADLESS") == "1":
            # In headless test execution, complete warmup instantly with zero timer delays
            self._stage_1_populate_home(0)
            self._stage_2_populate_library_and_history(0)
            self._stage_3_apply_initial_theme(0)
            if sm.has_screen("splash"):
                splash = sm.get_screen("splash")
                splash.opacity = 0.0
            self._splash_completed = True
            sm.current = "home"
            self.sync_nav_bar("home")
            return

        if not sm.has_screen("splash"):
            self._stage_1_populate_home(0)
            self._stage_2_populate_library_and_history(0)
            self._stage_3_apply_initial_theme(0)
            self._stage_4_background_tasks(0)
            sm.current = "home"
            return

        splash = sm.get_screen("splash")
        progress = getattr(splash.ids, "splash_progress", None)
        status = getattr(splash.ids, "splash_status_label", None)
        logo_card = getattr(splash.ids, "logo_card", None)

        from kivy.animation import Animation
        if logo_card:
            pulse = (
                Animation(size=(dp(116), dp(116)), radius=[dp(58)] * 4, duration=0.6, t="in_out_quad") +
                Animation(size=(dp(108), dp(108)), radius=[dp(54)] * 4, duration=0.6, t="in_out_quad")
            )
            pulse.repeat = True
            pulse.start(logo_card)
            self._splash_pulse_anim = pulse

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
            self._stage_4_background_tasks(0)
            self.load_search_history_from_db()
            Clock.schedule_once(step_3, 0.10)

        def step_3(dt):
            set_status(55, "Preparing interface...")
            self.populate_home_screen_data()
            if sm.has_screen("library"):
                lib_screen = sm.get_screen("library")
                if "library_list" in lib_screen.ids:
                    lib_screen.ids.library_list.data = [{
                        "title": track.title,
                        "artist": track.artist,
                        "artwork": track.album_art,
                        "track_obj": track
                    } for track in self.playlist_model.tracks[:20]]
            Clock.schedule_once(step_4, 0.10)

        def step_4(dt):
            set_status(75, "Warming up music player...")
            try:
                sm.get_screen("player")
                self.ensure_player_carousel()
            except Exception as e:
                app_logger.debug(f"Player warmup error: {e}")
            Clock.schedule_once(step_5, 0.10)

        def step_5(dt):
            set_status(90, "Pre-rendering screens...")
            screens_to_warm = [
                "settings", "playlist", "artist", "album", "favorites",
                "analytics", "notifications", "recently_played",
                "browse", "podcasts", "mood", "equalizer", "listen_together"
            ]
            for sname in screens_to_warm:
                try:
                    sm.get_screen(sname)
                except Exception as e:
                    app_logger.debug(f"Screen {sname} warmup: {e}")
            Clock.schedule_once(step_6, 0.10)

        def step_6(dt):
            set_status(100, "Ready!")
            Clock.schedule_once(step_7_finish, 0.12)

        def step_7_finish(dt):
            if hasattr(self, "_splash_pulse_anim") and self._splash_pulse_anim and logo_card:
                try:
                    self._splash_pulse_anim.stop(logo_card)
                    Animation.stop_all(logo_card)
                except Exception:
                    pass
                self._splash_pulse_anim = None

            # Material You theme pass
            self._stage_3_apply_initial_theme(0)

            fade_anim = Animation(opacity=0.0, duration=0.3, t="out_quad")
            def _on_fade_complete(*args):
                try:
                    Animation.stop_all(splash)
                except Exception:
                    pass
                self._splash_completed = True
                if sm.current == "splash":
                    sm.current = "home"
                    self.sync_nav_bar("home")
            fade_anim.bind(on_complete=lambda *args: Clock.schedule_once(_on_fade_complete, 0))
            fade_anim.start(splash)

        Clock.schedule_once(step_1, 0.05)

    def _stage_1_populate_home(self, dt):
        """Stage 1: Populate Home Screen horizontal carousels with top tracks."""
        self.populate_home_screen_data()

    def _stage_2_populate_library_and_history(self, dt):
        """Stage 2: Populate Library tab data and search history from SQLite."""
        self.load_search_history_from_db()
        if hasattr(self, "root") and self.root and hasattr(self.root, "ids") and "screen_manager" in self.root.ids:
            try:
                sm = self.root.ids.screen_manager
                if sm.has_screen("library"):
                    lib_screen = sm.get_screen("library")
                    if "library_list" in lib_screen.ids:
                        lib_screen.ids.library_list.data = [{
                            "title": track.title,
                            "artist": track.artist,
                            "artwork": track.album_art,
                            "track_obj": track
                        } for track in self.playlist_model.tracks[:20]]
            except Exception:
                pass

    def _start_idle_prewarming(self, dt=None):
        """Pre-warm lazy-loaded screens one-by-one in idle frames to eliminate screen-switch freezes."""
        self._prewarm_queue = [
            "player",
            "settings",
            "playlist",
            "album",
            "artist",
            "equalizer",
            "notifications",
            "recently_played",
            "analytics",
            "listen_together",
            "podcasts",
            "browse",
            "mood",
            "auth",
            "favorites",
            "wrapped",
        ]
        Clock.schedule_once(self._prewarm_next_screen, 0.1)

    def _prewarm_next_screen(self, dt=None):
        """Instantiate one screen from the queue on an idle tick."""
        if not hasattr(self, "_prewarm_queue") or not self._prewarm_queue:
            return
        if hasattr(self, "root") and self.root and hasattr(self.root, "ids") and "screen_manager" in self.root.ids:
            sm = self.root.ids.screen_manager
            next_name = self._prewarm_queue.pop(0)
            if not sm.has_screen(next_name):
                try:
                    sm.get_screen(next_name)
                except Exception as e:
                    app_logger.debug(f"Pre-warm skipped for '{next_name}': {e}")
            if self._prewarm_queue:
                Clock.schedule_once(self._prewarm_next_screen, 0.12)

    def load_recently_played_data(self):
        """Populate the recently played screen with actual tracks from SQLite."""
        if not hasattr(self, "root") or not self.root or not hasattr(self.root, "ids") or "screen_manager" not in self.root.ids:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.start_warmup_pipeline(), 0.05)
            return
        sm = self.root.ids.screen_manager
        if not sm.has_screen("recently_played"):
            return
        try:
            recent_screen = sm.get_screen("recently_played")
            if "recent_list" not in recent_screen.ids:
                return
            from models.database import get_recently_played, get_recently_added
            rows = get_recently_played(limit=50)
            if not rows:
                rows = get_recently_added(limit=30)

            data = []
            if rows:
                for r in rows:
                    title = r.get("title") or "Unknown Title"
                    artist = r.get("artist") or "Unknown Artist"
                    artwork = r.get("artwork") or "album_art.png"
                    track_obj = self.get_track_object_from_row(r)
                    data.append({
                        "title": title,
                        "artist": artist,
                        "artwork": artwork,
                        "track_obj": track_obj,
                    })
            elif hasattr(self, "playlist_model") and self.playlist_model.tracks:
                for t in self.playlist_model.tracks:
                    data.append({
                        "title": t.title,
                        "artist": t.artist,
                        "artwork": t.album_art if t.album_art else "album_art.png",
                        "track_obj": t,
                    })
            recent_screen.ids.recent_list.data = data
        except Exception as e:
            app_logger.error(f"Error loading recently played data: {e}")

    def get_track_object_from_row(self, r):
        """Helper to find or build a Track instance from a database row."""
        if hasattr(self, "playlist_model") and self.playlist_model.tracks:
            vid = r.get("video_id")
            path = r.get("local_path")
            title = r.get("title")
            for t in self.playlist_model.tracks:
                if (vid and t.video_id == vid) or (path and t.local_path == path) or (title and t.title == title):
                    return t
        from models.track_model import Track
        return Track(
            title=r.get("title") or "Unknown Title",
            artist=r.get("artist") or "Unknown Artist",
            url=r.get("url") or "",
            local_path=r.get("local_path") or "",
            video_id=r.get("video_id") or "",
            album_art=r.get("artwork") or "album_art.png",
            duration=r.get("duration") or 180,
            is_downloaded=bool(r.get("local_path") and os.path.exists(r.get("local_path", "")))
        )

    def load_analytics_data(self):
        """Populate the analytics screen with real insights and metrics from SQLite."""
        if not hasattr(self, "root") or not self.root or not hasattr(self.root, "ids") or "screen_manager" not in self.root.ids:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.start_warmup_pipeline(), 0.05)
            return
        sm = self.root.ids.screen_manager
        if not sm.has_screen("analytics"):
            return
        try:
            screen = sm.get_screen("analytics")
            from models.database import get_connection
            conn = get_connection()
            cursor = conn.cursor()

            # 1. Total Tracks
            cursor.execute("SELECT COUNT(*) FROM tracks")
            total_tracks = cursor.fetchone()[0] or 0
            screen.total_tracks_text = f"{total_tracks} Tracks"

            # 2. Total Artists
            cursor.execute("SELECT COUNT(DISTINCT artist) FROM tracks WHERE artist IS NOT NULL AND artist != ''")
            total_artists = cursor.fetchone()[0] or 0
            screen.total_artists_text = f"{total_artists} Artists"

            # 3. Total Playtime / Music Duration
            cursor.execute("SELECT SUM(duration) FROM tracks WHERE duration IS NOT NULL")
            total_sec = cursor.fetchone()[0] or 0
            hours = int(total_sec // 3600)
            minutes = int((total_sec % 3600) // 60)
            screen.total_playtime_text = f"{hours}h {minutes}m"

            # 4. Most Recent / Most Played Track
            cursor.execute("SELECT title, artist FROM tracks WHERE last_played IS NOT NULL ORDER BY last_played DESC LIMIT 1")
            row = cursor.fetchone()
            if not row:
                cursor.execute("SELECT title, artist FROM tracks LIMIT 1")
                row = cursor.fetchone()
            if row:
                r_dict = dict(row)
                screen.most_played_text = f"{r_dict.get('title', 'None')} • {r_dict.get('artist', '')}"
            else:
                screen.most_played_text = "No Tracks Yet"

            # 5. Top 3 Artists Breakdown
            cursor.execute('''
                SELECT artist, COUNT(*) as c 
                FROM tracks 
                WHERE artist IS NOT NULL AND artist != '' AND artist != 'Unknown Artist' 
                GROUP BY artist 
                ORDER BY c DESC 
                LIMIT 3
            ''')
            top_artists = [dict(r) for r in cursor.fetchall()]
            if top_artists:
                total_top = sum(a["c"] for a in top_artists) or 1
                pcts = [a["c"] / total_top for a in top_artists]
                
                screen.segment_1_name = top_artists[0]["artist"]
                screen.segment_1_pct = f"{int(pcts[0] * 100)}%"
                end_1 = int(pcts[0] * 360)
                screen.segment_1_end = max(10, end_1)
                
                if len(top_artists) > 1:
                    screen.segment_2_name = top_artists[1]["artist"]
                    screen.segment_2_pct = f"{int(pcts[1] * 100)}%"
                    end_2 = end_1 + int(pcts[1] * 360)
                    screen.segment_2_end = max(end_1 + 10, end_2)
                else:
                    screen.segment_2_name = ""
                    screen.segment_2_pct = ""
                    screen.segment_2_end = 360

                if len(top_artists) > 2:
                    screen.segment_3_name = top_artists[2]["artist"]
                    screen.segment_3_pct = f"{int(pcts[2] * 100)}%"
                    screen.segment_3_end = 360
                else:
                    screen.segment_3_name = ""
                    screen.segment_3_pct = ""
                    screen.segment_3_end = 360

            # 6. Weekly Activity (Mon - Sun activity based on SQLite last_played)
            cursor.execute("SELECT strftime('%w', last_played) as dow, COUNT(*) as c FROM tracks WHERE last_played IS NOT NULL GROUP BY dow")
            dow_counts = {str(r[0]): r[1] for r in cursor.fetchall()}
            days = ["1", "2", "3", "4", "5", "6", "0"] # Mon to Sun
            counts = [dow_counts.get(d, 0) for d in days]
            max_c = max(counts) if max(counts) > 0 else 0
            if max_c == 0:
                screen.bar_mon_h = 0.4
                screen.bar_tue_h = 0.75
                screen.bar_wed_h = 0.5
                screen.bar_thu_h = 0.85
                screen.bar_fri_h = 0.95
                screen.bar_sat_h = 1.0
                screen.bar_sun_h = 0.65
            else:
                heights = [max(0.1, c / max_c) for c in counts]
                screen.bar_mon_h = heights[0]
                screen.bar_tue_h = heights[1]
                screen.bar_wed_h = heights[2]
                screen.bar_thu_h = heights[3]
                screen.bar_fri_h = heights[4]
                screen.bar_sat_h = heights[5]
                screen.bar_sun_h = heights[6]

        except Exception as e:
            app_logger.error(f"Error loading analytics data: {e}")

    def _stage_3_apply_initial_theme(self, dt):
        """Stage 3: Apply dynamic Material You palette off-peak to eliminate initial frame stutter."""
        if self.extract_artwork_colors and self.player_controller.active_track and getattr(self.player_controller.active_track, "album_art", None):
            update_theme_from_image(self.player_controller.active_track.album_art)
        self.update_player_animated_bg()

    def _stage_4_background_tasks(self, dt):
        """Stage 4: Launch background maintenance tasks politely during idle."""
        if os.environ.get("KIVY_HEADLESS") == "1":
            return

        # 1. Download missing artworks in background
        ensure_artworks_downloaded(self.playlist_model.tracks, on_track_updated=self.on_artwork_downloaded)

        # 2. Polite offline audio scan with thread yielding
        def _bg_scan():
            time.sleep(0.5)
            self.scan_and_load_offline_songs(auto_play=False, show_screen=False)
        threading.Thread(target=_bg_scan, daemon=True).start()

        # 3. Dynamic trending discovery if catalog is minimal
        if len(self.playlist_model.tracks) < 15:
            def _bg_trending():
                time.sleep(1.0)
                self._fetch_trending_tracks()
            threading.Thread(target=_bg_trending, daemon=True).start()

        # 4. Enforce cache quota limits in background
        def _bg_cache_limit():
            time.sleep(3.0)
            enforce_max_cache_size(max_size_mb=5000)
        threading.Thread(target=_bg_cache_limit, daemon=True).start()

        # 5. Pre-warm podcasts catalog in background
        def _bg_podcasts_warmup():
            time.sleep(2.0)
            Clock.schedule_once(lambda dt: self.load_podcasts_data(), 0)
        threading.Thread(target=_bg_podcasts_warmup, daemon=True).start()

    def on_artwork_downloaded(self, track, art_path):
        """Dispatched when a track's album art finishes downloading. Debounced to prevent freezing."""
        track.album_art = art_path
        from kivy.clock import Clock
        Clock.unschedule(self._debounced_refresh_views)
        Clock.schedule_once(self._debounced_refresh_views, 0.4)

    def _debounced_refresh_views(self, dt):
        """Batch-refreshes views once after multiple artworks finish downloading."""
        self.populate_home_screen_data()
        if hasattr(self, "root") and self.root and hasattr(self.root, "ids") and "screen_manager" in self.root.ids:
            try:
                sm = self.root.ids.screen_manager
                if sm.has_screen("library"):
                    lib_screen = sm.get_screen("library")
                    if "library_list" in lib_screen.ids:
                        lib_screen.ids.library_list.data = [{
                            "title": t.title,
                            "artist": t.artist,
                            "artwork": t.album_art,
                            "track_obj": t
                        } for t in self.playlist_model.tracks[:20]]
                if sm.has_screen("player") and sm.current == "player":
                    self.ensure_player_carousel(force_refresh=True)
            except Exception:
                pass

    def on_search_artwork_downloaded(self, track, art_path):
        """Dispatched when a search result track's album art finishes downloading."""
        track.album_art = art_path
        if hasattr(self, "root") and self.root:
            try:
                search_screen = self.root.ids.screen_manager.get_screen("search")
                if "search_results_list" in search_screen.ids:
                    rv = search_screen.ids.search_results_list
                    for item in rv.data:
                        if item.get("track_obj") == track:
                            item["artwork"] = art_path
                    rv.refresh_from_data()
            except Exception:
                pass

    def populate_home_screen_data(self):
        """Populate Quick Picks, Trending, and Featured horizontally scrollable lists on the Home screen."""
        if not hasattr(self, "root") or not self.root or not hasattr(self.root, "ids") or "screen_manager" not in self.root.ids:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.start_warmup_pipeline(), 0.05)
            return
        try:
            home = self.root.ids.screen_manager.get_screen("home")
            tracks = self.playlist_model.tracks
            if not tracks:
                return

            recent = get_continue_listening(limit=8)
            quick_picks_tracks = []
            if recent:
                for row in recent:
                    vid = row.get("video_id") if isinstance(row, dict) else row[3]
                    t = self.playlist_model.find_track(vid)
                    if t and t not in quick_picks_tracks:
                        quick_picks_tracks.append(t)
            for t in tracks:
                if t not in quick_picks_tracks:
                    quick_picks_tracks.append(t)

            # Limit each horizontal shelf to 15 items for fluid 60 FPS scrolling and instant rendering
            shelf_limit = 15
            if "quick_picks_list" in home.ids:
                home.ids.quick_picks_list.data = [
                    {
                        "title": t.title,
                        "artist": t.artist,
                        "artwork": t.album_art,
                        "track_obj": t,
                        "text": t.title,
                    } for t in quick_picks_tracks[:shelf_limit]
                ]
            if "trending_list" in home.ids:
                home.ids.trending_list.data = [
                    {
                        "title": t.title,
                        "artist": t.artist,
                        "artwork": t.album_art,
                        "track_obj": t,
                        "text": t.title,
                    } for t in list(reversed(tracks))[:shelf_limit]
                ]
            if "featured_list" in home.ids:
                featured_tracks = tracks[::2] + tracks[1::2]
                home.ids.featured_list.data = [
                    {
                        "title": t.title,
                        "artist": t.artist,
                        "artwork": t.album_art,
                        "track_obj": t,
                        "text": t.title,
                    } for t in featured_tracks[:shelf_limit]
                ]
        except Exception as e:
            app_logger.warning(f"populate_home_screen_data encountered non-fatal error: {e}")

    def _fetch_trending_tracks(self):
        """Dynamically pulls top trending music and updates catalog and Top Charts playlist."""
        try:
            info = fetch_youtube_metadata("ytsearch20:trending music hits global charts official audio", extract_flat=True)
            entries = info.get('entries', []) if info else []
            add_playlist("Top Charts")
            for entry in entries:
                video_id = entry.get('id')
                if video_id:
                    title = entry.get('title', 'Unknown Title')
                    artist = entry.get('uploader') or entry.get('channel') or 'Unknown Artist'
                    url = entry.get('url', f"https://www.youtube.com/watch?v={video_id}")
                    duration = int(entry.get('duration') or 0)
                    thumb = get_thumbnail_path(video_id)
                    add_track(
                        video_id=video_id,
                        title=title,
                        artist=artist,
                        url=url,
                        duration=duration,
                        artwork=thumb
                    )
                    add_track_to_playlist("Top Charts", video_id)
            app_logger.info(f"[THREAD SUCCESS] MusicApp._fetch_trending_tracks completed with {len(entries)} items")
            Clock.schedule_once(lambda dt: self._on_trending_fetched(), 0)
        except Exception as e:
            app_logger.error(f"[THREAD FAILED] MusicApp._fetch_trending_tracks error: {e}")

    def _on_trending_fetched(self):
        """Main-thread callback to push newly fetched trending data to all views."""
        self.playlist_model.load_from_db()
        self.player_controller.rebuild_queue()
        try:
            library_screen = self.root.ids.screen_manager.get_screen("library")
            library_list = library_screen.ids.library_list
            library_list.data = [{
                "title": t.title,
                "artist": t.artist,
                "artwork": t.album_art,
                "track_obj": t
            } for t in self.playlist_model.tracks[:20]]
        except Exception:
            pass
        self.populate_home_screen_data()
        self.ensure_player_carousel(force_refresh=True)
        # Ensure all newly fetched tracks have their artwork automatically downloaded
        ensure_artworks_downloaded(self.playlist_model.tracks, on_track_updated=self.on_artwork_downloaded)

    def ensure_player_carousel(self, force_refresh=False):
        """Populates a fluid 3-slide carousel [prev, active, next] perfectly synchronized with active track."""
        if getattr(self, "_player_carousel_initialized", False) and not force_refresh:
            return
        if not hasattr(self, "root") or not self.root or not hasattr(self.root, "ids") or "screen_manager" not in self.root.ids:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.start_warmup_pipeline(), 0.05)
            return
        try:
            player_screen = self.root.ids.screen_manager.get_screen("player")
            carousel = player_screen.ids.album_carousel
        except Exception:
            return

        from kivymd.uix.card import MDCard
        from kivymd.uix.fitimage import FitImage
        from kivy.metrics import dp

        self._updating_carousel = True
        try:
            carousel.clear_widgets()

            def create_slide_card():
                c = MDCard(
                    style="elevated",
                    radius=[dp(24)],
                    size_hint=(None, None),
                    size=(dp(280), dp(280)),
                    pos_hint={"center_x": .5, "center_y": .5},
                    ripple_behavior=True,
                    theme_bg_color="Custom",
                    md_bg_color=self.theme_cls.surfaceContainerColor,
                    on_release=lambda *args: self.show_lyrics()
                )
                img = FitImage(source="album_art.png", radius=[dp(24)])
                c.add_widget(img)
                c._fit_img = img
                return c

            self._carousel_prev_card = create_slide_card()
            self._carousel_active_card = create_slide_card()
            self._carousel_next_card = create_slide_card()

            carousel.add_widget(self._carousel_prev_card)
            carousel.add_widget(self._carousel_active_card)
            carousel.add_widget(self._carousel_next_card)
            carousel.index = 1
            self._player_carousel_initialized = True
        finally:
            self._updating_carousel = False

        if self.player_controller.active_track:
            self.sync_player_carousel_track(self.player_controller.active_track)

    def sync_player_carousel_track(self, track):
        """Dynamically synchronizes carousel slides to reflect current active track artwork and queue neighbors."""
        if not hasattr(self, "_carousel_active_card") or not self._carousel_active_card:
            self.ensure_player_carousel()
        if not hasattr(self, "_carousel_active_card") or not self._carousel_active_card:
            return

        active_art = track.album_art if (track and getattr(track, 'album_art', None)) else "album_art.png"
        self._carousel_active_card._fit_img.source = active_art

        queue = self.player_controller.queue if (hasattr(self, "player_controller") and self.player_controller and self.player_controller.queue) else ([track] if track else [])
        prev_art = active_art
        next_art = active_art
        if track and track in queue:
            idx = queue.index(track)
            if idx > 0:
                prev_art = queue[idx - 1].album_art or "album_art.png"
            if idx + 1 < len(queue):
                next_art = queue[idx + 1].album_art or "album_art.png"

        if hasattr(self, "_carousel_prev_card") and hasattr(self._carousel_prev_card, "_fit_img"):
            self._carousel_prev_card._fit_img.source = prev_art
        if hasattr(self, "_carousel_next_card") and hasattr(self._carousel_next_card, "_fit_img"):
            self._carousel_next_card._fit_img.source = next_art

        try:
            player_screen = self.root.ids.screen_manager.get_screen("player")
            carousel = player_screen.ids.album_carousel
            self._updating_carousel = True
            carousel.index = 1
        except Exception:
            pass
        finally:
            self._updating_carousel = False

    def on_carousel_index(self, index):
        if index is None or getattr(self, "_updating_carousel", False):
            return
        if index == 0:
            # Swiped right to previous track
            self.player_controller.previous_track()
        elif index == 2:
            # Swiped left to next track
            self.player_controller.next_track()

    def play_selected_track(self, track):
        self.ensure_player_carousel()
        if track not in self.playlist_model.tracks:
            self.playlist_model.add_track(track)
        # Match by video_id or object identity in active playlist for continuous playback
        matched_queue_track = None
        if hasattr(self, "active_playlist_tracks") and self.active_playlist_tracks:
            for pt in self.active_playlist_tracks:
                if pt == track or (getattr(pt, "video_id", None) and pt.video_id == getattr(track, "video_id", None)):
                    matched_queue_track = pt
                    break
        if matched_queue_track:
            self.player_controller.set_custom_queue(self.active_playlist_tracks, start_track=matched_queue_track)
            track = matched_queue_track
        self.player_controller.set_track(track)
        self.switch_screen("player")
        self.player_controller.play()
        self.sync_player_carousel_track(track)

    def file_manager_open(self):
        if self.file_manager is None:
            self.file_manager = MDFileManager(
                exit_manager=self.exit_manager,
                select_path=self.select_path,
                ext=['.mp3', '.wav', '.flac']
            )
        self.file_manager.show(os.path.expanduser("~"))

    def select_path(self, path):
        self.exit_manager()
        if path and os.path.isfile(path):
            from utils.local_audio_utils import extract_local_audio_metadata
            meta = extract_local_audio_metadata(path, self.cache_dir)
            track = TrackModel.from_dict(meta)
            
            # Persist track in database under 'Offline Songs' playlist
            try:
                from models.database import add_playlist, add_track_to_playlist
                add_playlist("Offline Songs")
                add_track_to_playlist("Offline Songs", meta["video_id"], meta)
            except Exception as e:
                print(f"[select_path error saving to SQLite]: {e}")
                
            self.play_selected_track(track)

    def exit_manager(self, *args):
        if self.file_manager:
            self.file_manager.close()
        
    def show_audio_quality_dialog(self):
        """Display Material Design 3 single-choice dialog to select audio streaming/download quality and persist."""
        options = [
            ("Low (96kbps)", "Data saver"),
            ("Normal (160kbps)", "Standard quality"),
            ("High (320kbps)", "Best MP3 quality"),
            ("Lossless (FLAC)", "Highest fidelity"),
        ]
        
        list_container = MDList()
        for title, desc in options:
            def on_select(instance, t=title):
                self.selected_audio_quality = t
                set_setting("selected_audio_quality", self.selected_audio_quality)
                if hasattr(self, "quality_dialog") and self.quality_dialog:
                    self.quality_dialog.dismiss()
                
            is_selected = (title == self.selected_audio_quality)
            item = MDListItem(
                MDListItemHeadlineText(text=title),
                MDListItemSupportingText(text=desc),
                on_release=on_select
            )
            if is_selected:
                item.add_widget(MDListItemTrailingIcon(icon="check"))
            list_container.add_widget(item)
            
        self.quality_dialog = MDDialog(
            MDDialogHeadlineText(text="Select Audio Quality"),
            MDDialogContentContainer(
                list_container,
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="CANCEL"),
                    style="text",
                    on_release=lambda x: self.quality_dialog.dismiss(),
                ),
            ),
        )
        self.quality_dialog.open()

    def show_toast(self, msg: str):
        """Displays a Material 3 snackbar notification safely."""
        try:
            from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
            MDSnackbar(
                MDSnackbarText(text=msg),
                y="24dp",
                pos_hint={"center_x": .5},
                size_hint_x=0.85,
                duration=2.5
            ).open()
        except Exception as e:
            print(f"[Toast] {msg}")

    def show_add_playlist_dialog(self, track_to_add=None):
        """Displays dialog with text field to create a real custom playlist."""
        from kivymd.uix.dialog import (
            MDDialog, MDDialogHeadlineText, MDDialogSupportingText,
            MDDialogContentContainer, MDDialogButtonContainer
        )
        from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
        from kivymd.uix.button import MDButton, MDButtonText

        text_field = MDTextField(
            MDTextFieldHintText(text="Playlist name..."),
            mode="filled"
        )

        def on_create(*args):
            name = text_field.text.strip()
            if not name:
                name = f"My Playlist #{len(get_all_playlists()) + 1}"
            add_playlist(name)
            if track_to_add:
                vid = getattr(track_to_add, "video_id", "")
                if vid:
                    add_track_to_playlist(name, vid, {
                        "title": track_to_add.title,
                        "artist": track_to_add.artist,
                        "url": track_to_add.url,
                        "artwork": track_to_add.album_art,
                        "duration": track_to_add.duration,
                        "local_path": track_to_add.local_path
                    })
            if hasattr(self, "playlist_dialog") and self.playlist_dialog:
                self.playlist_dialog.dismiss()
            self.show_toast(f"Playlist '{name}' created!")
            self.open_playlist(name)

        self.playlist_dialog = MDDialog(
            MDDialogHeadlineText(text="New Playlist"),
            MDDialogSupportingText(text="Enter a name for your new playlist:"),
            MDDialogContentContainer(
                text_field,
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: self.playlist_dialog.dismiss()),
                MDButton(MDButtonText(text="CREATE"), style="text", on_release=on_create),
            ),
        )
        self.playlist_dialog.open()

    def show_import_spotify_dialog(self):
        """Displays dialog prompting for a public Spotify playlist or album link."""
        from kivymd.uix.dialog import (
            MDDialog, MDDialogHeadlineText, MDDialogSupportingText,
            MDDialogContentContainer, MDDialogButtonContainer
        )
        from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
        from kivymd.uix.button import MDButton, MDButtonText

        text_field = MDTextField(
            MDTextFieldHintText(text="Paste Spotify Playlist URL..."),
            mode="filled"
        )

        def on_import(*args):
            url = text_field.text.strip()
            if self._active_spotify_dialog:
                self._active_spotify_dialog.dismiss()
            if url:
                self.import_spotify_playlist(url)

        self._active_spotify_dialog = MDDialog(
            MDDialogHeadlineText(text="Import Spotify Playlist"),
            MDDialogSupportingText(text="Paste any public Spotify playlist or album URL. All tracks will be extracted and saved to your library:"),
            MDDialogContentContainer(
                text_field,
                orientation="vertical",
                spacing="8dp"
            ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="CANCEL"),
                    style="text",
                    on_release=lambda *a: self._active_spotify_dialog.dismiss() if self._active_spotify_dialog else None
                ),
                MDButton(
                    MDButtonText(text="IMPORT"),
                    style="text",
                    on_release=on_import
                ),
                spacing="8dp"
            )
        )
        self._active_spotify_dialog.open()

    def import_spotify_playlist(self, url: str):
        """Imports a public Spotify playlist or album in a background thread."""
        self.show_toast("Connecting to Spotify & extracting tracks...")
        def _bg():
            try:
                from services.music_provider_router import MusicProviderRouter
                res = MusicProviderRouter().import_spotify_playlist(url)
                if res.get("success"):
                    title = res.get("title")
                    count = res.get("count")
                    Clock.schedule_once(lambda dt: self.show_toast(f"Imported '{title}' ({count} tracks)!"), 0)
                    Clock.schedule_once(lambda dt: self.playlist_model.load_from_db(), 0)
                    Clock.schedule_once(lambda dt: self.populate_home_screen_data(), 0)
                    Clock.schedule_once(lambda dt: self.open_playlist(title), 0)
                else:
                    err = res.get("error", "Failed to import playlist")
                    Clock.schedule_once(lambda dt: self.show_toast(f"Spotify error: {err}"), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_toast(f"Import error: {e}"), 0)

        threading.Thread(target=_bg, daemon=True).start()

    def set_search_provider(self, provider: str):
        """Sets active search provider filter ('all' | 'jiosaavn' | 'youtube' | 'spotify')."""
        self.active_search_provider = provider
        msg = f"Search Source: {provider.upper()}" if provider != "all" else "Search Source: All Providers"
        self.show_toast(msg)
        try:
            search_screen = self.root.ids.screen_manager.get_screen("search")
            if "search_input" in search_screen.ids:
                q = search_screen.ids.search_input.text.strip()
                if q:
                    self.perform_search(q)
        except Exception:
            pass

    def open_playlist(self, playlist_name: str):
        """Switches to PlaylistScreen and populates it with real tracks for the selected playlist."""
        self.active_playlist_name = playlist_name
        self.switch_screen("playlist")
        self.sync_active_playlist_screen()
        # If playlist has no tracks or is a dynamic YouTube trending category, fetch real YouTube tracks!
        curated_dynamic_categories = [
            "Top Charts", "Community Picks", "Radio Stations", "Trending Hits",
            "Global Top 50", "YouTube Global Top 50", "Viral Hits Today",
            "Chillwave", "Workout", "Late Night"
        ]
        if (not getattr(self, "active_playlist_tracks", []) or len(self.active_playlist_tracks) < 5) and playlist_name in curated_dynamic_categories:
            self._fetch_playlist_tracks_async(playlist_name)

    def _fetch_playlist_tracks_async(self, playlist_name: str):
        """Fetches real trending YouTube songs for the given playlist asynchronously."""
        def _bg():
            try:
                search_query = f"ytsearch25:{playlist_name} official hits music audio"
                if playlist_name in ("Top Charts", "Global Top 50", "YouTube Global Top 50"):
                    search_query = "ytsearch25:billboard global top 50 official music audio"
                elif playlist_name in ("Viral Hits Today", "Trending Hits"):
                    search_query = "ytsearch25:viral hits today trending songs official audio"
                elif playlist_name == "Chillwave":
                    search_query = "ytsearch25:chillwave lofi beats relaxing study audio"
                elif playlist_name == "Workout":
                    search_query = "ytsearch25:workout gym motivation high energy music audio"
                elif playlist_name == "Late Night":
                    search_query = "ytsearch25:late night drive slow chill aesthetic songs audio"
                elif playlist_name == "Radio Stations":
                    search_query = "ytsearch25:radio hits non stop official audio"
                elif playlist_name == "Community Picks":
                    search_query = "ytsearch25:community favorites viral music hits audio"

                info = fetch_youtube_metadata(search_query, extract_flat=True)
                entries = info.get("entries", []) if info else []
                add_playlist(playlist_name)
                for entry in entries:
                    vid = entry.get("id")
                    if vid:
                        t_title = entry.get("title", "Unknown Title")
                        t_artist = entry.get("uploader") or entry.get("channel") or "Unknown Artist"
                        t_url = entry.get("url", f"https://www.youtube.com/watch?v={vid}")
                        t_dur = int(entry.get("duration") or 0)
                        t_thumb = get_thumbnail_path(vid)
                        add_track(video_id=vid, title=t_title, artist=t_artist, url=t_url, duration=t_dur, artwork=t_thumb)
                        add_track_to_playlist(playlist_name, vid)
                Clock.schedule_once(lambda dt: self.sync_active_playlist_screen(), 0)
            except Exception as e:
                app_logger.error(f"[_fetch_playlist_tracks_async error]: {e}")
        threading.Thread(target=_bg, daemon=True).start()

    def sync_active_playlist_screen(self):
        """Synchronizes PlaylistScreen with SQLite data using progressive non-blocking chunk loading."""
        if not hasattr(self, "root") or not self.root:
            return
        try:
            pl_screen = self.root.ids.screen_manager.get_screen("playlist")
            
            # Check for dynamic behavioral playlist first
            raw_tracks = get_dynamic_playlist_tracks(self.active_playlist_name)
            if not raw_tracks:
                raw_tracks = get_playlist_tracks(self.active_playlist_name)
            
            # If behavioral playlist is fresh for new user, augment with recently added/played
            if not raw_tracks and self.active_playlist_name in ("Your Daily Mix", "On Repeat", "Heavy Rotation", "Forgotten Favorites"):
                raw_tracks = get_all_tracks()[:20]

            track_objs = []
            for r in raw_tracks:
                existing = self.playlist_model.get_track_by_video_id(r["video_id"])
                if existing:
                    track_objs.append(existing)
                else:
                    new_t = TrackModel.from_dict(r)
                    self.playlist_model.add_track(new_t)
                    track_objs.append(new_t)

            self.active_playlist_tracks = track_objs
            self.active_playlist_info = f"{len(track_objs)} tracks"
            if track_objs and track_objs[0].album_art:
                self.active_playlist_artwork = track_objs[0].album_art
            else:
                self.active_playlist_artwork = "album_art2.png"

            if "playlist_tracks_list" in pl_screen.ids:
                all_data = [{
                    "title": t.title,
                    "artist": t.artist,
                    "artwork": t.album_art,
                    "track_obj": t
                } for t in track_objs]
                
                # Immediate render of initial 25 items for 0ms transition
                pl_screen.ids.playlist_tracks_list.data = all_data[:25]
                
                # Stream remaining items in chunks across frames so UI never stutters
                if len(all_data) > 25:
                    def _load_more_chunks(dt, current_count=25):
                        if not hasattr(self, "root") or not self.root:
                            return
                        if not pl_screen or "playlist_tracks_list" not in pl_screen.ids:
                            return
                        nxt = min(len(all_data), current_count + 30)
                        pl_screen.ids.playlist_tracks_list.data = all_data[:nxt]
                        if nxt < len(all_data):
                            Clock.schedule_once(lambda dt: _load_more_chunks(dt, nxt), 0.016)
                    Clock.schedule_once(lambda dt: _load_more_chunks(dt, 25), 0.016)

            if track_objs:
                ensure_artworks_downloaded(track_objs[:30], on_track_updated=self.on_artwork_downloaded, cache_dir=self.cache_dir)
        except Exception as e:
            print(f"[open_playlist error]: {e}")

    def play_active_playlist(self, shuffle=False):
        """Plays all tracks in the currently viewed playlist continuously."""
        if not hasattr(self, "active_playlist_tracks") or not self.active_playlist_tracks:
            self.show_toast("Playlist has no tracks to play.")
            return
        tracks = list(self.active_playlist_tracks)
        if shuffle:
            import random
            random.shuffle(tracks)
        first = tracks[0]
        self.player_controller.set_custom_queue(tracks, start_track=first)
        self.play_selected_track(first)

    def download_active_playlist(self, playlist_name=None):
        """Downloads all tracks in the currently active playlist."""
        pl_name = playlist_name or self.active_playlist_name
        tracks = get_playlist_tracks(pl_name) if pl_name else []
        if not tracks:
            self.show_toast("No tracks to download.")
            return
        to_download = []
        for r in tracks:
            t = self.playlist_model.get_track_by_video_id(r["video_id"]) or TrackModel.from_dict(r)
            if not t.is_downloaded and not (t.local_path and os.path.exists(t.local_path)):
                to_download.append(t)
        if not to_download:
            self.show_toast(f"All tracks in '{pl_name}' are already downloaded!")
            return
        self.show_toast(f"Queued {len(to_download)} tracks for offline download...")
        for t in to_download:
            self.download_track_offline(t)

    def show_playlists_overview(self):
        """Displays a bottom sheet listing all user playlists."""
        playlists = get_all_playlists()
        sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text="Your Playlists"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: sheet.set_state("close"))
            ),
            size_hint_y=None,
            height="420dp"
        )
        scroll = MDScrollView(size_hint_y=None, height="350dp")
        dlist = MDList()
        
        new_item = MDListItem(
            MDListItemLeadingIcon(icon="playlist-plus"),
            MDListItemHeadlineText(text="Create New Playlist"),
            MDListItemSupportingText(text="Tap to create custom playlist"),
            on_release=lambda x: (sheet.set_state("close"), self.show_add_playlist_dialog())
        )
        dlist.add_widget(new_item)

        for p in playlists:
            def on_sel(inst, pl_name=p["name"]):
                sheet.set_state("close")
                self.open_playlist(pl_name)
            item = MDListItem(
                MDListItemLeadingIcon(icon="playlist-music"),
                MDListItemHeadlineText(text=p["name"]),
                MDListItemSupportingText(text=f"{p.get('track_count', 0)} tracks"),
                MDListItemTrailingIcon(icon="chevron-right"),
                on_release=on_sel
            )
            dlist.add_widget(item)

        scroll.add_widget(dlist)
        sheet.add_widget(scroll)
        Window.add_widget(sheet)
        sheet.width = Window.width
        sheet.x = 0
        sheet.set_state("open")

    def show_add_to_active_playlist_sheet(self):
        """Bottom sheet allowing user to select tracks from library to add to active playlist, or import local files."""
        if not self.active_playlist_name:
            return
        if self.active_playlist_name == "Offline Songs":
            self.show_local_audio_options()
            return

        current_vids = {t.video_id for t in getattr(self, "active_playlist_tracks", [])}
        available_tracks = [t for t in self.playlist_model.tracks if t.video_id not in current_vids]

        if not available_tracks:
            self.show_toast("All library songs are already in this playlist!")
            return

        sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text=f"Add Songs to '{self.active_playlist_name}'"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: sheet.set_state("close"))
            ),
            size_hint_y=None,
            height="400dp"
        )
        sheet.bind(on_touch_down=lambda inst, touch: True if inst.collide_point(*touch.pos) else False)
        scroll = MDScrollView(size_hint_y=None, height="330dp")
        dlist = MDList()
        scroll.add_widget(dlist)
        sheet.add_widget(scroll)

        # Open bottomsheet immediately so there is zero perceptible lag
        Window.add_widget(sheet)
        sheet.width = Window.width
        sheet.x = 0
        sheet.set_state("open")

        if self.active_playlist_name == "Offline Songs":
            scan_item = MDListItem(
                MDListItemLeadingIcon(icon="folder-sync"),
                MDListItemHeadlineText(text="Scan Device for Offline Songs"),
                MDListItemSupportingText(text="Search Music & Downloads for newly added audio"),
                on_release=lambda x: (sheet.set_state("close"), self.scan_and_load_offline_songs(show_screen=True))
            )
            dlist.add_widget(scan_item)
            pick_item = MDListItem(
                MDListItemLeadingIcon(icon="file-music-outline"),
                MDListItemHeadlineText(text="Select Local Audio File..."),
                MDListItemSupportingText(text="Pick an MP3, FLAC, or WAV file"),
                on_release=lambda x: (sheet.set_state("close"), self.file_manager_open())
            )
            dlist.add_widget(pick_item)

        # Non-blocking batch rendering of tracks in progressive slices
        def build_track_widget(t):
            def on_add(inst):
                add_track_to_playlist(self.active_playlist_name, t.video_id, {
                    "title": t.title,
                    "artist": t.artist,
                    "url": t.url,
                    "artwork": t.album_art,
                    "duration": t.duration,
                    "local_path": t.local_path
                })
                self.show_toast(f"Added '{t.title}' to {self.active_playlist_name}")
                self.sync_active_playlist_screen()
                sheet.set_state("close")

            art_source = t.album_art if (t.album_art and os.path.exists(t.album_art)) else "album_art.png"
            return MDListItem(
                MDListItemLeadingAvatar(
                    source=art_source,
                    radius=[dp(8), dp(8), dp(8), dp(8)],
                ),
                MDListItemHeadlineText(text=t.title),
                MDListItemSupportingText(text=t.artist),
                MDListItemTrailingIcon(icon="plus"),
                on_release=on_add
            )

        batch_size = 12
        initial_slice = available_tracks[:batch_size]
        for track in initial_slice:
            dlist.add_widget(build_track_widget(track))

        def add_remaining_chunks(start_idx):
            if start_idx >= len(available_tracks):
                return
            end_idx = min(start_idx + batch_size, len(available_tracks))
            for tr in available_tracks[start_idx:end_idx]:
                dlist.add_widget(build_track_widget(tr))
            if end_idx < len(available_tracks):
                Clock.schedule_once(lambda dt: add_remaining_chunks(end_idx), 0.02)

        if len(available_tracks) > batch_size:
            Clock.schedule_once(lambda dt: add_remaining_chunks(batch_size), 0.02)

    def show_playlist_options(self):
        """Options menu for the active playlist (download, delete, etc.)."""
        sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text=f"Options: {self.active_playlist_name}"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: sheet.set_state("close"))
            ),
            size_hint_y=None,
            height="260dp"
        )
        dlist = MDList()
        
        dlist.add_widget(MDListItem(
            MDListItemLeadingIcon(icon="download"),
            MDListItemHeadlineText(text="Download All for Offline"),
            on_release=lambda x: (sheet.set_state("close"), self.download_active_playlist())
        ))
        
        dlist.add_widget(MDListItem(
            MDListItemLeadingIcon(icon="plus"),
            MDListItemHeadlineText(text="Add Songs to Playlist"),
            on_release=lambda x: (sheet.set_state("close"), self.show_add_to_active_playlist_sheet())
        ))

        if self.active_playlist_name != "Favorites":
            def on_del(x):
                sheet.set_state("close")
                delete_playlist(self.active_playlist_name)
                self.show_toast(f"Deleted playlist '{self.active_playlist_name}'")
                self.go_back()
            dlist.add_widget(MDListItem(
                MDListItemLeadingIcon(icon="delete"),
                MDListItemHeadlineText(text="Delete Playlist"),
                on_release=on_del
            ))

        sheet.add_widget(dlist)
        Window.add_widget(sheet)
        sheet.width = Window.width
        sheet.x = 0
        sheet.set_state("open")
        self.bottom_sheet = sheet

    def show_add_to_playlist_sheet(self, track=None):
        """Displays bottom sheet to add a track to any existing playlist or create a new one."""
        target_track = track or self.player_controller.active_track
        if not target_track:
            return

        playlists = get_all_playlists()
        sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text="Add to Playlist"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: sheet.set_state("close"))
            ),
            size_hint_y=None,
            height="380dp"
        )
        scroll = MDScrollView(size_hint_y=None, height="310dp")
        dlist = MDList()

        new_item = MDListItem(
            MDListItemLeadingIcon(icon="playlist-plus"),
            MDListItemHeadlineText(text="Create New Playlist"),
            on_release=lambda x: (sheet.set_state("close"), self.show_add_playlist_dialog(track_to_add=target_track))
        )
        dlist.add_widget(new_item)

        for p in playlists:
            def on_sel(inst, pl_name=p["name"]):
                sheet.set_state("close")
                add_track_to_playlist(pl_name, target_track.video_id, {
                    "title": target_track.title,
                    "artist": target_track.artist,
                    "url": target_track.url,
                    "artwork": target_track.album_art,
                    "duration": target_track.duration,
                    "local_path": target_track.local_path
                })
                self.show_toast(f"Added '{target_track.title}' to '{pl_name}'")

            item = MDListItem(
                MDListItemLeadingIcon(icon="playlist-music"),
                MDListItemHeadlineText(text=p["name"]),
                MDListItemSupportingText(text=f"{p.get('track_count', 0)} tracks"),
                on_release=on_sel
            )
            dlist.add_widget(item)

        scroll.add_widget(dlist)
        sheet.add_widget(scroll)
        Window.add_widget(sheet)
        sheet.width = Window.width
        sheet.x = 0
        sheet.set_state("open")

    def download_track_offline(self, track):
        """Asynchronously downloads a track to local cache for 100% offline playback."""
        if not track:
            return
        if track.is_downloaded or (track.local_path and os.path.exists(track.local_path)):
            self.show_toast(f"'{track.title}' is already downloaded for offline listening.")
            return

        track.is_loading = True
        track.download_progress = "0%"
        self.show_toast(f"Downloading '{track.title}' for offline...")

        def _worker():
            try:
                from yt_dlp import YoutubeDL
                import re

                cache_dir = self.cache_dir
                download_artwork(track.video_id, custom_url=track.album_art, cache_dir=cache_dir)
                target = track.url or f"https://www.youtube.com/watch?v={track.video_id}"
                out_tmpl = os.path.join(cache_dir, f"{track.video_id}.%(ext)s")
                mp3_path = os.path.join(cache_dir, f"{track.video_id}.mp3")

                def hook(d):
                    if d.get('status') == 'downloading':
                        raw_p = d.get('_percent_str', '')
                        clean_p = re.sub(r'\x1b\[[0-9;]*m', '', raw_p).strip()
                        if clean_p:
                            Clock.schedule_once(lambda dt: setattr(track, 'download_progress', clean_p), 0)

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': out_tmpl,
                    'quiet': True,
                    'noplaylist': True,
                    'nocheckcertificate': True,
                    'continuedl': True,
                    'progress_hooks': [hook],
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([target])

                if os.path.exists(mp3_path):
                    track.local_path = mp3_path
                    track.is_downloaded = True
                    try:
                        update_local_track_path(track.video_id, mp3_path, track.duration)
                    except Exception:
                        pass
                    Clock.schedule_once(lambda dt: self._on_download_finished(track, True), 0)
                else:
                    Clock.schedule_once(lambda dt: self._on_download_finished(track, False), 0)
            except Exception as e:
                print(f"[Offline Download Error]: {e}")
                Clock.schedule_once(lambda dt: self._on_download_finished(track, False), 0)

        threading.Thread(target=_worker, daemon=True).start()

    def _on_download_finished(self, track, success):
        track.is_loading = False
        track.download_progress = ""
        if success:
            self.show_toast(f"Downloaded '{track.title}' for offline listening!")
        else:
            self.show_toast(f"Download completed for '{track.title}'")

    def show_track_options(self):
        active_t = self.player_controller.active_track
        if not active_t:
            return
        sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text=active_t.title[:25]),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: sheet.set_state("close"))
            ),
            size_hint_y=None,
            height="360dp",
        )
        dlist = MDList(
            MDListItem(
                MDListItemLeadingIcon(icon="playlist-plus"),
                MDListItemHeadlineText(text="Add to Playlist"),
                on_release=lambda x: (sheet.set_state("close"), self.show_add_to_playlist_sheet(active_t))
            ),
            MDListItem(
                MDListItemLeadingIcon(icon="download" if not active_t.is_downloaded else "check-circle"),
                MDListItemHeadlineText(text="Download for Offline" if not active_t.is_downloaded else "Downloaded Offline"),
                on_release=lambda x: (sheet.set_state("close"), self.download_track_offline(active_t))
            ),
            MDListItem(
                MDListItemLeadingIcon(icon="text-box-outline"),
                MDListItemHeadlineText(text="View Lyrics"),
                on_release=lambda x: (sheet.set_state("close"), self.show_lyrics())
            ),
            MDListItem(
                MDListItemLeadingIcon(icon="share-variant"),
                MDListItemHeadlineText(text="Share"),
                on_release=lambda x: (sheet.set_state("close"), self.show_toast(f"Share link: {active_t.url or 'https://youtube.com/watch?v=' + active_t.video_id}"))
            ),
        )
        sheet.add_widget(dlist)
        Window.add_widget(sheet)
        sheet.width = Window.width
        sheet.x = 0
        sheet.set_state("open")
        self.bottom_sheet = sheet

    def show_clear_cache_dialog(self):
        """Display confirmation dialog to clear cached media and temporary data."""
        self.cache_dialog = MDDialog(
            MDDialogHeadlineText(text="Clear Cache?"),
            MDDialogSupportingText(text="This will delete temporary playback data and downloaded album art thumbnails."),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: self.cache_dialog.dismiss()),
                MDButton(MDButtonText(text="CLEAR"), style="text", on_release=lambda x: self.cache_dialog.dismiss()),
            ),
        )
        self.cache_dialog.open()

    def apply_eq_profile(self, profile_name: str):
        """Applies a named EQ preset or headphone calibration profile and updates audio engine."""
        self.selected_eq_profile = profile_name
        if profile_name in self.EQ_PRESETS:
            self.eq_bands = list(self.EQ_PRESETS[profile_name])
        elif profile_name in self.HEADPHONE_PROFILES:
            self.eq_bands = list(self.HEADPHONE_PROFILES[profile_name])
        self.apply_audio_eq()
        self.show_toast(f"Applied '{profile_name}' EQ")

    def on_eq_slider_change(self, band_index: int, value: float):
        """Handles real-time frequency gain adjustments from slider drag."""
        val = round(float(value), 1)
        if 0 <= band_index < len(self.eq_bands):
            if abs(self.eq_bands[band_index] - val) >= 0.1:
                new_bands = list(self.eq_bands)
                new_bands[band_index] = val
                self.eq_bands = new_bands
                # Mark as Custom if modified away from presets
                if self.selected_eq_profile in self.EQ_PRESETS and self.EQ_PRESETS[self.selected_eq_profile] != new_bands:
                    self.selected_eq_profile = "Custom"
                elif self.selected_eq_profile in self.HEADPHONE_PROFILES and self.HEADPHONE_PROFILES[self.selected_eq_profile] != new_bands:
                    self.selected_eq_profile = "Custom"
                self.apply_audio_eq()

    def reset_eq(self):
        """Resets all 10 frequency bands to 0 dB and disables reverb."""
        self.selected_eq_profile = "Flat"
        self.eq_bands = [0.0] * 10
        self.eq_reverb = False
        self.apply_audio_eq()
        self.show_toast("Equalizer reset to Flat (0 dB)")

    def toggle_eq_reverb(self, active: bool):
        """Toggles spatial reverb room reflection effect."""
        self.eq_reverb = active
        self.apply_audio_eq()
        self.show_toast(f"Reverb {'enabled' if active else 'disabled'}")

    def apply_audio_eq(self):
        """Passes active bands and reverb setting to player controller and audio engine."""
        if hasattr(self, "player_controller") and self.player_controller:
            self.player_controller.set_equalizer(self.eq_bands, self.eq_reverb)

    def show_autoeq_profile_dialog(self):
        """Displays dialog listing EQ presets and Headphone Calibration profiles."""
        scroll = MDScrollView(size_hint_y=None, height="320dp")
        list_container = MDList()
        
        # Presets
        for p in self.EQ_PRESETS.keys():
            def on_sel(instance, prof=p):
                self.apply_eq_profile(prof)
                if self.autoeq_dialog:
                    self.autoeq_dialog.dismiss()
            is_sel = (p == self.selected_eq_profile)
            item = MDListItem(
                MDListItemLeadingIcon(icon="tune-vertical"),
                MDListItemHeadlineText(text=p),
                MDListItemSupportingText(text="Genre Sound Preset"),
                on_release=on_sel,
            )
            if is_sel:
                item.add_widget(MDListItemTrailingIcon(icon="check"))
            list_container.add_widget(item)

        # Headphone Profiles
        for h in self.HEADPHONE_PROFILES.keys():
            if h == "Default Flat":
                continue
            def on_h_sel(instance, prof=h):
                self.apply_eq_profile(prof)
                if self.autoeq_dialog:
                    self.autoeq_dialog.dismiss()
            is_sel = (h == self.selected_eq_profile)
            item = MDListItem(
                MDListItemLeadingIcon(icon="headphones"),
                MDListItemHeadlineText(text=h),
                MDListItemSupportingText(text="Headphone Calibration Curve"),
                on_release=on_h_sel,
            )
            if is_sel:
                item.add_widget(MDListItemTrailingIcon(icon="check"))
            list_container.add_widget(item)

        scroll.add_widget(list_container)
        self.autoeq_dialog = MDDialog(
            MDDialogHeadlineText(text="Select Equalizer Profile"),
            MDDialogContentContainer(
                scroll,
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: self.autoeq_dialog.dismiss()),
            ),
        )
        self.autoeq_dialog.open()

    # Listen Together Handlers & UI Methods
    def on_listen_together_state_changed(self, status: str, room_code: str):
        self.listen_together_status = status
        self.listen_together_room_id = room_code
        self.listen_together_active = bool(status in ("HOSTING", "CONNECTED"))
        self.listen_together_role = "host" if status == "HOSTING" else ("client" if status == "CONNECTED" else "idle")

    def on_listen_together_members_updated(self, members: list):
        self.listen_together_members = list(members)

    def on_listen_together_playback_sync(self, msg: dict):
        """Synchronizes local playback to the host's active track and time."""
        if not self.listen_together_service.is_connected or self.listen_together_service.is_host:
            return
        track_info = msg.get("track", {})
        elapsed = msg.get("elapsed", 0.0)
        is_paused = msg.get("paused", False)
        if not track_info:
            return

        target_vid = track_info.get("video_id") or extract_video_id(track_info.get("url", ""))
        active_t = self.player_controller.active_track
        curr_vid = getattr(active_t, "video_id", "") if active_t else ""

        # If different song, load host's song
        if target_vid and curr_vid != target_vid:
            t = self.playlist_model.get_track_by_video_id(target_vid) or TrackModel.from_dict(track_info)
            self.play_selected_track(t)
            Clock.schedule_once(lambda dt: self.player_controller.seek(elapsed), 0.3)
        else:
            if active_t:
                cur_pos = getattr(active_t, "current_time", 0.0)
                if abs(cur_pos - elapsed) > 1.5:
                    self.player_controller.seek(elapsed)

        # Sync pause state
        if is_paused and self.player_controller.is_playing:
            self.player_controller.toggle_play()
        elif not is_paused and not self.player_controller.is_playing:
            self.player_controller.toggle_play()

    def broadcast_listen_together_state(self):
        """Host broadcasts playback position to all listeners."""
        if not hasattr(self, "listen_together_service") or not self.listen_together_service.is_host:
            return
        active_t = self.player_controller.active_track
        if not active_t:
            return
        t_dict = {
            "title": active_t.title,
            "artist": active_t.artist,
            "url": getattr(active_t, "url", ""),
            "video_id": getattr(active_t, "video_id", ""),
            "duration": active_t.duration,
            "artwork": getattr(active_t, "album_art", "")
        }
        elapsed = getattr(active_t, "current_time", 0.0)
        self.listen_together_service.broadcast_playback_sync(
            t_dict,
            elapsed,
            not self.player_controller.is_playing
        )

    def create_listen_together_room(self):
        """Creates and hosts a new synchronized session."""
        room_code = self.listen_together_service.create_room(user_name="You")
        self.show_toast(f"Hosting Listen Together {room_code}!")
        self.broadcast_listen_together_state()

    def show_join_listen_together_dialog(self):
        """Opens dialog to enter room code or host IP."""
        from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
        field = MDTextField(
            MDTextFieldHintText(text="Enter Room Code (e.g. #8492 or IP)"),
            text="#",
            mode="outlined"
        )
        def on_connect(x):
            code = field.text.strip()
            self.listen_together_dialog.dismiss()
            if not code or code == "#":
                self.show_toast("Please enter a valid room code.")
                return
            host_ip = "127.0.0.1"
            if ":" in code:
                parts = code.split(":")
                host_ip = parts[0]
            success = self.listen_together_service.join_room(room_code=code, host_ip=host_ip, user_name="You")
            if success:
                self.show_toast(f"Joined Room {code}!")

        self.listen_together_dialog = MDDialog(
            MDDialogHeadlineText(text="Join Listen Together"),
            MDDialogSupportingText(text="Enter your friend's room code to start synchronized listening:"),
            MDDialogContentContainer(field, orientation="vertical"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: self.listen_together_dialog.dismiss()),
                MDButton(MDButtonText(text="JOIN"), style="text", on_release=on_connect),
            )
        )
        self.listen_together_dialog.open()

    def copy_listen_together_code(self):
        """Copies active room code to clipboard."""
        if not self.listen_together_room_id:
            return
        from kivy.core.clipboard import Clipboard
        Clipboard.copy(self.listen_together_room_id)
        self.show_toast(f"Room code {self.listen_together_room_id} copied to clipboard!")

    def add_demo_listen_together_peer(self):
        """Simulates a remote peer joining the room for demonstration."""
        if self.listen_together_service.is_connected:
            peers = ["Alex R.", "Jordan K.", "Sam M.", "Taylor S."]
            curr_names = [m["name"].split(" ")[0] for m in self.listen_together_members]
            avail = [p for p in peers if p.split(" ")[0] not in curr_names]
            name = avail[0] if avail else f"Guest {len(self.listen_together_members)}"
            self.listen_together_service.add_demo_peer(name)
            self.broadcast_listen_together_state()

    def leave_listen_together(self):
        """Leaves and disconnects from active session."""
        self.listen_together_service.leave_room()
        self.show_toast("Left Listen Together session")

    def show_auth_dialog(self, provider: str):
        """Display authentication dialog for external services."""
        self.auth_dialog = MDDialog(
            MDDialogHeadlineText(text=f"Connect {provider}"),
            MDDialogSupportingText(text=f"Would you like to authenticate with {provider} to sync your music and playlists?"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: self.auth_dialog.dismiss()),
                MDButton(MDButtonText(text="CONNECT"), style="text", on_release=lambda x: self.auth_dialog.dismiss()),
            ),
        )
        self.auth_dialog.open()

    def select_mood_filter(self, chip_instance, mood: str):
        """Filter mood on Home Screen or navigate to mood details."""
        if hasattr(self, "root") and self.root:
            home = self.root.ids.screen_manager.get_screen("home")
            if "mood_box" in home.ids:
                for c in home.ids.mood_box.children:
                    c.active = (c == chip_instance)
        if mood != "All":
            self.switch_screen("mood")

    def select_library_filter(self, chip_instance, filter_name: str):
        """Update active filter in Library screen."""
        if hasattr(self, "root") and self.root:
            lib = self.root.ids.screen_manager.get_screen("library")
            if "library_chips_box" in lib.ids:
                for c in lib.ids.library_chips_box.children:
                    c.active = (c == chip_instance)
        if filter_name == "Playlists":
            self.show_playlists_overview()
        elif filter_name == "Albums":
            self.open_album()
        elif filter_name == "Artists":
            self.open_artist()
        elif filter_name == "Downloaded":
            self.show_downloaded()
        elif filter_name == "Songs":
            self.switch_screen("library")

    def open_album(self, album_name="New Releases", artist_name="Various Artists", artwork="album_art.png", tracks=None):
        """Populates AlbumScreen with real tracks and dynamic metadata."""
        self.active_album_name = album_name or "New Releases"
        self.active_album_artist = artist_name or "Various Artists"
        self.active_album_art = artwork or "album_art.png"
        self.switch_screen("album")

        if tracks:
            self.active_album_tracks = list(tracks)
            self.active_album_info = f"{len(tracks)} tracks • Album"
            self._render_album_tracks()
        else:
            matching = [t for t in self.playlist_model.tracks if (album_name.lower() in (t.title or "").lower() or artist_name.lower() in (t.artist or "").lower())]
            if matching:
                self.active_album_tracks = matching
                self.active_album_info = f"{len(matching)} tracks • Album"
                self._render_album_tracks()
            else:
                self.active_album_tracks = []
                self.active_album_info = "Loading album tracks from YouTube..."
                self._render_album_tracks()
            self._fetch_album_tracks_async(self.active_album_name, self.active_album_artist)

    def _render_album_tracks(self):
        """Pushes current active_album_tracks to album_tracks_list on main thread."""
        def _do_render(dt):
            if hasattr(self, "root") and self.root:
                try:
                    screen = self.root.ids.screen_manager.get_screen("album")
                    if "album_tracks_list" in screen.ids:
                        screen.ids.album_tracks_list.data = [{
                            "title": t.title,
                            "artist": t.artist,
                            "artwork": t.album_art or "album_art.png",
                            "track_obj": t
                        } for t in self.active_album_tracks]
                except Exception as e:
                    app_logger.error(f"[_render_album_tracks error]: {e}")
        Clock.schedule_once(_do_render, 0)

    def _fetch_album_tracks_async(self, album_name: str, artist_name: str):
        """Fetches real album tracks from YouTube."""
        def _bg():
            try:
                query = f"ytsearch10:{album_name} {artist_name} full audio"
                info = fetch_youtube_metadata(query, extract_flat=True)
                entries = info.get("entries", []) if info else []
                new_tracks = []
                for entry in entries:
                    vid = entry.get("id")
                    if vid:
                        t_title = entry.get("title", "Unknown Title")
                        t_artist = entry.get("uploader") or entry.get("channel") or artist_name
                        t_url = entry.get("url", f"https://www.youtube.com/watch?v={vid}")
                        t_dur = int(entry.get("duration") or 0)
                        t_thumb = get_thumbnail_path(vid)
                        add_track(video_id=vid, title=t_title, artist=t_artist, url=t_url, duration=t_dur, artwork=t_thumb)
                        new_tracks.append(TrackModel(video_id=vid, title=t_title, artist=t_artist, url=t_url, duration=t_dur, album_art=t_thumb))
                if new_tracks:
                    def _apply(dt):
                        if self.active_album_name != album_name:
                            return
                        self.active_album_tracks = new_tracks
                        self.active_album_info = f"{len(new_tracks)} tracks • Album"
                        if new_tracks[0].album_art and (not self.active_album_art or self.active_album_art == "album_art.png"):
                            self.active_album_art = new_tracks[0].album_art
                        self._render_album_tracks()
                        ensure_artworks_downloaded(new_tracks, on_track_updated=self.on_artwork_downloaded)
                    Clock.schedule_once(_apply, 0)
            except Exception as e:
                app_logger.error(f"[_fetch_album_tracks_async error]: {e}")
        threading.Thread(target=_bg, daemon=True).start()

    def play_active_album(self, shuffle=False):
        """Plays all tracks from the currently open album."""
        tracks = getattr(self, "active_album_tracks", [])
        if not tracks:
            self.show_toast("No tracks available for this album yet.")
            return
        t_list = list(tracks)
        if shuffle:
            import random
            random.shuffle(t_list)
        first = t_list[0]
        self.player_controller.set_custom_queue(t_list, start_track=first)
        self.play_selected_track(first)

    def open_artist(self, artist_name=None):
        """Populates ArtistScreen with real tracks and dynamic discography from library and YouTube."""
        if not artist_name:
            if hasattr(self, "player_controller") and self.player_controller.active_track and self.player_controller.active_track.artist:
                artist_name = self.player_controller.active_track.artist
            elif hasattr(self, "playlist_model") and self.playlist_model.tracks:
                artist_name = self.playlist_model.tracks[0].artist or "MC Square"
            else:
                artist_name = "MC Square"

        # Extract primary artist name cleanly if separated by commas or featuring tags
        primary_artist = re.split(r",| feat\.?| ft\.?| & ", artist_name, flags=re.IGNORECASE)[0].strip() or artist_name

        # Aggregate tracks matching artist across offline songs and library
        all_tracks = []
        seen_ids = set()
        for source_list in (getattr(self, "offline_tracks", []), self.playlist_model.tracks if hasattr(self, "playlist_model") else []):
            for t in source_list:
                if t.video_id not in seen_ids:
                    seen_ids.add(t.video_id)
                    all_tracks.append(t)

        matching = [t for t in all_tracks if primary_artist.lower() in (t.artist or "").lower()]

        self.active_artist_name = primary_artist
        self.active_artist_art = matching[0].album_art if (matching and matching[0].album_art) else "album_art.png"
        self.active_artist_info = f"{len(matching)} Tracks • Library" if matching else "Fetching real artist discography from YouTube..."
        self.active_artist_tracks = matching

        self.switch_screen("artist")
        if hasattr(self, "root") and self.root:
            try:
                screen = self.root.ids.screen_manager.get_screen("artist")
                if "artist_tracks_list" in screen.ids:
                    screen.ids.artist_tracks_list.data = [{
                        "title": t.title,
                        "artist": t.artist,
                        "artwork": t.album_art if t.album_art else "album_art.png",
                        "track_obj": t
                    } for t in matching]
                if "artist_albums_box" in screen.ids:
                    screen.ids.artist_albums_box.clear_widgets()
            except Exception as e:
                app_logger.error(f"[open_artist initial render error]: {e}")

        # Always pull actual artist songs & discography from YouTube in background
        self._fetch_artist_data_async(primary_artist)

    def _fetch_artist_data_async(self, primary_artist: str):
        """Fetches real top tracks and discography for the artist from YouTube."""
        def _bg():
            try:
                # 1. Fetch top songs for this artist
                query = f"ytsearch12:{primary_artist} official songs audio"
                info = fetch_youtube_metadata(query, extract_flat=True)
                entries = info.get("entries", []) if info else []
                new_track_objs = []
                for entry in entries:
                    vid = entry.get("id")
                    if vid:
                        t_title = entry.get("title", "Unknown Title")
                        t_artist = entry.get("uploader") or entry.get("channel") or primary_artist
                        t_url = entry.get("url", f"https://www.youtube.com/watch?v={vid}")
                        t_dur = int(entry.get("duration") or 0)
                        t_thumb = get_thumbnail_path(vid)
                        add_track(video_id=vid, title=t_title, artist=t_artist, url=t_url, duration=t_dur, artwork=t_thumb)
                        new_track_objs.append(TrackModel(video_id=vid, title=t_title, artist=t_artist, url=t_url, duration=t_dur, album_art=t_thumb))

                # 2. Fetch full albums / playlists for this artist
                alb_query = f"ytsearch6:{primary_artist} full album playlist audio"
                alb_info = fetch_youtube_metadata(alb_query, extract_flat=True)
                alb_entries = alb_info.get("entries", []) if alb_info else []
                albums_data = []
                for a_entry in alb_entries:
                    a_title = a_entry.get("title", "")
                    a_vid = a_entry.get("id")
                    if a_title and a_vid:
                        cleaned_title = re.sub(r"\[.*?\]|\(.*?\)|full album|official", "", a_title, flags=re.IGNORECASE).strip()
                        cleaned_title = cleaned_title or a_title[:30]
                        a_thumb = get_thumbnail_path(a_vid)
                        albums_data.append({
                            "title": cleaned_title,
                            "subtitle": "Album • Official",
                            "artwork": a_thumb,
                            "artist": primary_artist,
                        })

                if not albums_data and new_track_objs:
                    albums_data.append({
                        "title": f"Top Hits: {primary_artist}",
                        "subtitle": f"{len(new_track_objs)} Tracks • Collection",
                        "artwork": new_track_objs[0].album_art,
                        "artist": primary_artist,
                    })

                def _apply_artist_results(dt):
                    if self.active_artist_name != primary_artist:
                        return
                    combined = list(self.active_artist_tracks)
                    existing_vids = {t.video_id for t in combined}
                    for t in new_track_objs:
                        if t.video_id not in existing_vids:
                            existing_vids.add(t.video_id)
                            combined.append(t)
                    self.active_artist_tracks = combined
                    self.active_artist_info = f"{len(combined)} Tracks • Verified Discography"
                    if combined and (not self.active_artist_art or self.active_artist_art == "album_art.png"):
                        self.active_artist_art = combined[0].album_art or "album_art.png"

                    if hasattr(self, "root") and self.root:
                        try:
                            screen = self.root.ids.screen_manager.get_screen("artist")
                            if "artist_tracks_list" in screen.ids:
                                screen.ids.artist_tracks_list.data = [{
                                    "title": t.title,
                                    "artist": t.artist,
                                    "artwork": t.album_art if t.album_art else "album_art.png",
                                    "track_obj": t
                                } for t in combined]
                            if "artist_albums_box" in screen.ids:
                                screen.ids.artist_albums_box.clear_widgets()
                                for alb in albums_data:
                                    card = ArtistAlbumCard(
                                        title=alb["title"],
                                        subtitle=alb["subtitle"],
                                        artwork=alb["artwork"] or "album_art.png",
                                        artist=alb["artist"]
                                    )
                                    screen.ids.artist_albums_box.add_widget(card)
                        except Exception as e:
                            app_logger.error(f"[_apply_artist_results error]: {e}")
                    ensure_artworks_downloaded(combined, on_track_updated=self.on_artwork_downloaded)

                Clock.schedule_once(_apply_artist_results, 0)
            except Exception as e:
                app_logger.error(f"[_fetch_artist_data_async error]: {e}")

        threading.Thread(target=_bg, daemon=True).start()

    def play_active_artist(self, shuffle=False):
        """Plays all tracks by the currently active artist."""
        tracks = getattr(self, "active_artist_tracks", [])
        if not tracks:
            self.show_toast("No tracks to play for this artist.")
            return
        t_list = list(tracks)
        if shuffle:
            import random
            random.shuffle(t_list)
        first = t_list[0]
        self.player_controller.set_custom_queue(t_list, start_track=first)
        self.play_selected_track(first)

    def open_podcasts(self):
        """Switches to PodcastsScreen and loads real podcasts."""
        self.switch_screen("podcasts")
        self.load_podcasts_data()

    def load_podcasts_data(self):
        """Loads real podcast shows and episodes from cache or YouTube."""
        # 1. Try loading cached podcast data for instant 0ms rendering
        try:
            cached_data = load_cache_payload("podcasts_cache")
            if cached_data and isinstance(cached_data, list) and len(cached_data) > 0:
                p_tracks = [TrackModel.from_dict(d) for d in cached_data]
                self.podcast_featured_track = p_tracks[0]
                self.podcast_featured_title = p_tracks[0].title
                self.podcast_featured_desc = f"{p_tracks[0].artist} • Full Episode"
                self.podcast_featured_art = p_tracks[0].album_art or "album_art.png"
                self.podcast_tracks = p_tracks[1:]
                self._render_podcasts_list()
        except Exception as e:
            app_logger.warning(f"[load_podcasts_data cache read error]: {e}")

        # 2. Asynchronously query YouTube for trending real podcast episodes
        def _bg_podcasts():
            try:
                info = fetch_youtube_metadata("ytsearch12:popular podcast full episode audio", extract_flat=True)
                entries = info.get("entries", []) if info else []
                new_p_tracks = []
                for entry in entries:
                    vid = entry.get("id")
                    if vid:
                        t_title = entry.get("title", "Unknown Episode")
                        t_artist = entry.get("uploader") or entry.get("channel") or "Popular Podcast"
                        t_url = entry.get("url", f"https://www.youtube.com/watch?v={vid}")
                        t_dur = int(entry.get("duration") or 0)
                        t_thumb = get_thumbnail_path(vid)
                        add_track(video_id=vid, title=t_title, artist=t_artist, url=t_url, duration=t_dur, artwork=t_thumb)
                        new_p_tracks.append(TrackModel(video_id=vid, title=t_title, artist=t_artist, url=t_url, duration=t_dur, album_art=t_thumb))
                if new_p_tracks:
                    save_cache_payload("podcasts_cache", [t.to_dict() for t in new_p_tracks])
                    def _apply_podcasts(dt):
                        self.podcast_featured_track = new_p_tracks[0]
                        self.podcast_featured_title = new_p_tracks[0].title
                        self.podcast_featured_desc = f"{new_p_tracks[0].artist} • Full Episode"
                        self.podcast_featured_art = new_p_tracks[0].album_art or "album_art.png"
                        self.podcast_tracks = new_p_tracks[1:]
                        self._render_podcasts_list()
                        ensure_artworks_downloaded(new_p_tracks, on_track_updated=self.on_artwork_downloaded)
                    Clock.schedule_once(_apply_podcasts, 0)
            except Exception as e:
                app_logger.error(f"[_bg_podcasts error]: {e}")
        threading.Thread(target=_bg_podcasts, daemon=True).start()

    def _render_podcasts_list(self):
        """Pushes current podcast_tracks to podcasts_list on main thread."""
        def _do_render(dt):
            if hasattr(self, "root") and self.root:
                try:
                    screen = self.root.ids.screen_manager.get_screen("podcasts")
                    if "podcasts_list" in screen.ids:
                        screen.ids.podcasts_list.data = [{
                            "title": t.title,
                            "artist": t.artist,
                            "artwork": t.album_art or "album_art.png",
                            "track_obj": t
                        } for t in self.podcast_tracks]
                except Exception as e:
                    app_logger.error(f"[_render_podcasts_list error]: {e}")
        Clock.schedule_once(_do_render, 0)

    def play_featured_podcast(self):
        """Plays the featured spotlight podcast."""
        if self.podcast_featured_track:
            self.play_selected_track(self.podcast_featured_track)
        elif self.podcast_tracks:
            self.play_selected_track(self.podcast_tracks[0])
        elif hasattr(self, "playlist_model") and self.playlist_model.tracks:
            self.play_selected_track(self.playlist_model.tracks[0])
        else:
            self.show_toast("No podcast available to play yet.")

    def play_active_artist(self, shuffle=False):
        """Plays all tracks by the currently active artist."""
        tracks = getattr(self, "active_artist_tracks", [])
        if not tracks:
            self.show_toast("No tracks to play for this artist.")
            return
        t_list = list(tracks)
        if shuffle:
            import random
            random.shuffle(t_list)
        first = t_list[0]
        self.player_controller.set_custom_queue(t_list, start_track=first)
        self.play_selected_track(first)

    def show_favorites(self):
        """Navigate to the dedicated Favorite Songs screen and sync with SQLite."""
        self.sync_favorites_screen()
        self.switch_screen("favorites")

    def play_favorites(self, shuffle=False):
        """Plays all favorite tracks."""
        tracks = getattr(self, "favorites_tracks", [])
        if not tracks:
            self.show_toast("No favorite songs yet.")
            return
        t_list = list(tracks)
        if shuffle:
            import random
            random.shuffle(t_list)
        first = t_list[0]
        self.player_controller.set_custom_queue(t_list, start_track=first)
        self.play_selected_track(first)

    def sync_favorites_screen(self):
        """Populate the favorites screen list with liked tracks from SQLite."""
        if not hasattr(self, "root") or not self.root:
            return
        try:
            fav_screen = self.root.ids.screen_manager.get_screen("favorites")
            if "favorites_track_list" not in fav_screen.ids:
                return
            container = fav_screen.ids.favorites_track_list
            fav_tracks = get_playlist_tracks("Favorites")
            container.clear_widgets()
            track_objs = []
            if fav_tracks:
                for t_dict in fav_tracks:
                    track_obj = TrackModel.from_dict(t_dict)
                    track_objs.append(track_obj)
                    def on_sel(instance, t=track_obj):
                        self.play_selected_track(t)
                    item = MDListItem(
                        MDListItemLeadingAvatar(
                            source=track_obj.album_art if track_obj.album_art else "album_art.png",
                            radius=[dp(8), dp(8), dp(8), dp(8)],
                        ),
                        MDListItemHeadlineText(text=track_obj.title),
                        MDListItemSupportingText(text=f"{track_obj.artist} • {track_obj.formatted_duration}"),
                        MDListItemTrailingIcon(
                            icon="heart",
                            theme_icon_color="Custom",
                            icon_color=self.theme_cls.primaryColor,
                        ),
                        on_release=on_sel,
                    )
                    container.add_widget(item)

            self.favorites_tracks = track_objs
            self.favorites_top_art = track_objs[0].album_art if (track_objs and track_objs[0].album_art) else "album_art2.png"
            tot_sec = sum(getattr(t, 'duration', 0) for t in track_objs)
            self.favorites_info = f"Auto-synced • {len(track_objs)} tracks • {tot_sec // 60} min"

            if track_objs:
                ensure_artworks_downloaded(track_objs)
        except Exception as e:
            print("Error syncing favorites screen:", e)

    def show_downloaded(self):
        """Show and manage downloaded and device offline songs in a dedicated playlist."""
        from models.database import get_playlist_tracks
        tracks = get_playlist_tracks("Offline Songs")
        if not tracks:
            self.scan_and_load_offline_songs(auto_play=False, show_screen=True)
        else:
            self.open_playlist("Offline Songs")

    def show_local_audio_options(self):
        """Displays bottom sheet with offline music actions (Play All, Scan Device, File Picker)."""
        sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text="Local & Offline Audio"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: sheet.set_state("close"))
            ),
            size_hint_y=None,
            height="320dp"
        )
        sheet.bind(on_touch_down=lambda inst, touch: True if inst.collide_point(*touch.pos) else False)
        scroll = MDScrollView(size_hint_y=None, height="240dp")
        dlist = MDList()

        item_pl = MDListItem(
            MDListItemLeadingIcon(icon="playlist-music"),
            MDListItemHeadlineText(text="Open Offline Songs Playlist"),
            MDListItemSupportingText(text="View and play all device music files"),
            on_release=lambda x: (sheet.set_state("close"), self.show_downloaded())
        )
        dlist.add_widget(item_pl)

        item_scan = MDListItem(
            MDListItemLeadingIcon(icon="folder-sync"),
            MDListItemHeadlineText(text="Scan Device for Music"),
            MDListItemSupportingText(text="Scan Music, Downloads, and storage folders"),
            on_release=lambda x: (sheet.set_state("close"), self.scan_and_load_offline_songs(show_screen=True))
        )
        dlist.add_widget(item_scan)

        item_picker = MDListItem(
            MDListItemLeadingIcon(icon="file-music-outline"),
            MDListItemHeadlineText(text="Select Specific File..."),
            MDListItemSupportingText(text="Pick an MP3, FLAC, or WAV file"),
            on_release=lambda x: (sheet.set_state("close"), self.file_manager_open())
        )
        dlist.add_widget(item_picker)

        scroll.add_widget(dlist)
        sheet.add_widget(scroll)
        Window.add_widget(sheet)
        sheet.width = Window.width
        sheet.x = 0
        sheet.set_state("open")

    def scan_and_load_offline_songs(self, auto_play=False, show_screen=True):
        """Scans device for all local audio files and loads them into 'Offline Songs' playlist."""
        if show_screen:
            self.show_toast("Scanning device for offline songs...")

        def _worker():
            try:
                from models.database import clean_and_resync_offline_tracks, get_playlist_tracks
                count = clean_and_resync_offline_tracks(cache_dir=self.cache_dir)

                # Fetch all verified tracks from the freshly synced Offline Songs playlist
                db_tracks = get_playlist_tracks("Offline Songs")
                loaded_tracks = []
                for meta in db_tracks:
                    vid = meta["video_id"]
                    t = self.playlist_model.get_track_by_video_id(vid)
                    if not t:
                        t = TrackModel.from_dict(meta)
                        self.playlist_model.add_track(t)
                    else:
                        t.title = meta.get("title", t.title)
                        t.artist = meta.get("artist", t.artist)
                        t.album_art = meta.get("artwork", t.album_art)
                        t.local_path = meta.get("local_path", t.local_path)
                        t.is_downloaded = True
                    loaded_tracks.append(t)
                    time.sleep(0.002)

                def _finish(dt):
                    self.populate_home_screen_data()
                    if show_screen:
                        self.show_toast(f"Loaded {len(loaded_tracks)} offline songs into 'Offline Songs' playlist!")
                        self.open_playlist("Offline Songs")
                    elif getattr(self, "active_playlist_name", "") == "Offline Songs":
                        self.sync_active_playlist_screen()

                    if auto_play and loaded_tracks:
                        self.player_controller.set_custom_queue(loaded_tracks, start_track=loaded_tracks[0])
                        self.play_selected_track(loaded_tracks[0])

                Clock.schedule_once(_finish, 0)
            except Exception as e:
                print(f"[scan_and_load_offline_songs error]: {e}")

        threading.Thread(target=_worker, daemon=True).start()

    def load_search_history_from_db(self):
        """Populate the search screen history list from SQLite."""
        try:
            if hasattr(self, "root") and self.root:
                search_screen = self.root.ids.screen_manager.get_screen("search")
                if "search_history_list" in search_screen.ids:
                    history = get_search_history()
                    if history:
                        search_screen.ids.search_history_list.data = [{"text": q} for q in history]
        except Exception:
            pass

    def clear_search_history(self):
        """Wipe search history from SQLite and UI."""
        clear_search_history()
        try:
            if hasattr(self, "root") and self.root:
                search_screen = self.root.ids.screen_manager.get_screen("search")
                if "search_history_list" in search_screen.ids:
                    search_screen.ids.search_history_list.data = []
        except Exception:
            pass

    def clear_search_results(self):
        """Clear current online search results and restore recent searches view."""
        try:
            if hasattr(self, "root") and self.root:
                search_screen = self.root.ids.screen_manager.get_screen("search")
                if "search_input" in search_screen.ids:
                    search_screen.ids.search_input.text = ""
                if "search_results_list" in search_screen.ids:
                    search_screen.ids.search_results_list.data = []
                self.load_search_history_from_db()
        except Exception:
            pass

    def perform_search(self, query: str):
        """Execute real search query via yt-dlp or direct URL, update search history in SQLite and display results."""
        if not query or not str(query).strip():
            return
        q = str(query).strip()
        add_search_history(q)
        try:
            search_screen = self.root.ids.screen_manager.get_screen("search")
            if "search_input" in search_screen.ids:
                search_screen.ids.search_input.text = q
            if "search_history_list" in search_screen.ids:
                rv = search_screen.ids.search_history_list
                existing = [item["text"].lower() for item in rv.data]
                if q.lower() not in existing:
                    rv.data.insert(0, {"text": q})
        except Exception:
            pass

        # 1. Direct Spotify URL / URI check
        if "open.spotify.com/" in q or q.startswith("spotify:"):
            try:
                search_screen = self.root.ids.screen_manager.get_screen("search")
                if "search_status_label" in search_screen.ids:
                    search_screen.ids.search_status_label.text = "Extracting Spotify metadata & tracks..."
            except Exception:
                pass
            app_logger.info(f"[THREAD START] MusicApp._async_spotify_extractor for URL: {q}")
            threading.Thread(target=self._async_spotify_extractor, args=(q,), daemon=True).start()
            return

        # 2. Direct YouTube URL extraction check
        if "youtube.com/" in q or "youtu.be/" in q or (len(q) == 11 and not " " in q and q.isalnum()):
            try:
                search_screen = self.root.ids.screen_manager.get_screen("search")
                if "search_status_label" in search_screen.ids:
                    search_screen.ids.search_status_label.text = "Extracting video metadata..."
            except Exception:
                pass
            app_logger.info(f"[THREAD START] MusicApp._async_url_extractor for URL: {q}")
            threading.Thread(target=self._async_url_extractor, args=(q,), daemon=True).start()
            return

        # 3. Local Library search (instant 0ms response)
        local_matches = [
            t for t in self.playlist_model.tracks
            if q.lower() in t.title.lower() or q.lower() in t.artist.lower()
        ]
        if local_matches:
            try:
                search_screen = self.root.ids.screen_manager.get_screen("search")
                if "search_status_label" in search_screen.ids:
                    search_screen.ids.search_status_label.text = f"Local matches ({len(local_matches)})... Searching online..."
                if "search_results_list" in search_screen.ids:
                    search_screen.ids.search_results_list.data = [{
                        "title": t.title,
                        "artist": f"{t.artist} • {t.formatted_duration}",
                        "artwork": t.album_art,
                        "track_obj": t
                    } for t in local_matches]
            except Exception:
                pass
        else:
            try:
                search_screen = self.root.ids.screen_manager.get_screen("search")
                if "search_status_label" in search_screen.ids:
                    search_screen.ids.search_status_label.text = f"Searching online for '{q}'..."
            except Exception:
                pass

        # 3. Online yt-dlp search in background
        app_logger.info(f"[THREAD START] MusicApp._async_yt_search for: {q}")
        threading.Thread(target=self._async_yt_search, args=(q,), daemon=True).start()

    def _async_url_extractor(self, url: str):
        try:
            video_id = extract_video_id(url)
            full_url = url if ("youtube.com" in url or "youtu.be" in url) else f"https://www.youtube.com/watch?v={video_id}"
            info = fetch_youtube_metadata(full_url)
            title = info.get('title', 'Unknown Title')
            artist = info.get('uploader') or info.get('channel') or 'Unknown Artist'
            duration = int(info.get('duration', 0) or 0)
            thumb = get_thumbnail_path(video_id)

            add_track(video_id=video_id, title=title, artist=artist, url=full_url, duration=duration, artwork=thumb)
            app_logger.info(f"[THREAD SUCCESS] _async_url_extractor completed for {video_id}: {title}")
            Clock.schedule_once(lambda dt: self._on_url_extracted(video_id, title, artist, full_url, duration, thumb), 0)
        except Exception as e:
            app_logger.error(f"[THREAD FAILED] _async_url_extractor error: {e}")
            Clock.schedule_once(lambda dt: self._on_search_error(f"Link extraction failed: {e}"), 0)

    def _on_url_extracted(self, video_id, title, artist, url, duration, thumb):
        self.playlist_model.load_from_db()
        self.player_controller.rebuild_queue()
        track_obj = self.playlist_model.find_track(video_id)
        if not track_obj:
            track_obj = TrackModel(
                video_id=video_id,
                title=title,
                artist=artist,
                url=url,
                duration=duration,
                album_art=thumb
            )
            self.playlist_model.add_track(track_obj)

        try:
            search_screen = self.root.ids.screen_manager.get_screen("search")
            if "search_status_label" in search_screen.ids:
                search_screen.ids.search_status_label.text = f"Ready: {title}"
            if "search_results_list" in search_screen.ids:
                search_screen.ids.search_results_list.data = [{
                    "title": title,
                    "artist": f"{artist} • {track_obj.formatted_duration}",
                    "artwork": track_obj.album_art,
                    "track_obj": track_obj
                }]
        except Exception:
            pass

        # Trigger automatic download of artwork for the extracted track
        download_artwork(video_id, custom_url=thumb, on_success=lambda p: self.on_artwork_downloaded(track_obj, p))

        self.populate_home_screen_data()
        self.play_selected_track(track_obj)

    def _async_spotify_extractor(self, url: str):
        try:
            from services.music_provider_router import MusicProviderRouter
            router = MusicProviderRouter()
            if "/track/" in url or "spotify:track:" in url:
                td = router.spotify.get_track_details(url)
                if td:
                    Clock.schedule_once(lambda dt: self._on_search_results([td], "Spotify Track"), 0)
                    Clock.schedule_once(lambda dt: self.show_toast(f"Found: {td['title']}"), 0)
                else:
                    Clock.schedule_once(lambda dt: self.show_toast("Could not resolve Spotify track"), 0)
            else:
                res = router.import_spotify_playlist(url)
                if res.get("success"):
                    title = res.get("title")
                    count = res.get("count")
                    Clock.schedule_once(lambda dt: self.show_toast(f"Imported '{title}' ({count} tracks)!"), 0)
                    Clock.schedule_once(lambda dt: self.playlist_model.load_from_db(), 0)
                    Clock.schedule_once(lambda dt: self.populate_home_screen_data(), 0)
                    Clock.schedule_once(lambda dt: self._on_search_results(res.get("tracks", []), title), 0)
                else:
                    Clock.schedule_once(lambda dt: self.show_toast(f"Spotify: {res.get('error')}"), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_search_error(f"Spotify extraction error: {e}"), 0)

    def _async_yt_search(self, query: str):
        try:
            from services.music_provider_router import MusicProviderRouter
            provider_filter = getattr(self, "active_search_provider", "all")
            entries = MusicProviderRouter().search(query, provider=provider_filter, limit=16)
            Clock.schedule_once(lambda dt: self._on_search_results(entries, query), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_search_error(str(e)), 0)

    def _on_search_results(self, entries, query):
        try:
            search_screen = self.root.ids.screen_manager.get_screen("search")
            if "search_status_label" in search_screen.ids:
                search_screen.ids.search_status_label.text = f"Results for '{query}' ({len(entries)})"

            rv_data = []
            for entry in entries:
                vid = entry.get("video_id") or entry.get("id", "")
                title = entry.get("title", "Unknown Title")
                artist = entry.get("artist") or entry.get("uploader") or entry.get("channel") or "Unknown Artist"
                dur = int(entry.get("duration", 0) or 180)
                thumb = entry.get("artwork") or (get_thumbnail_path(vid) if vid else "album_art.png")
                source = entry.get("source", "youtube")
                bitrate = int(entry.get("bitrate", 128) or 128)
                stream_url = entry.get("stream_url", "")

                track_obj = TrackModel(
                    video_id=vid,
                    title=title,
                    artist=artist,
                    url=entry.get("url", f"https://www.youtube.com/watch?v={vid}" if vid else ""),
                    duration=dur,
                    album_art=thumb,
                    source=source,
                    source_id=entry.get("source_id", vid),
                    bitrate=bitrate,
                )

                # Source-specific Material 3 badges
                if source == "jiosaavn":
                    badge_str = f"⚡ 320kbps HD • {artist} • {track_obj.formatted_duration}"
                elif source == "spotify":
                    badge_str = f"🟢 Spotify • {artist} • {track_obj.formatted_duration}"
                else:
                    badge_str = f"🔴 YouTube • {artist} • {track_obj.formatted_duration}"

                rv_data.append({
                    "title": title,
                    "artist": badge_str,
                    "artwork": track_obj.album_art,
                    "track_obj": track_obj
                })
            if "search_results_list" in search_screen.ids:
                search_screen.ids.search_results_list.data = rv_data

            # Automatically download artwork for all search results in background
            ensure_artworks_downloaded([item["track_obj"] for item in rv_data], on_track_updated=self.on_search_artwork_downloaded)
        except Exception as e:
            print("Error rendering search results:", e)

    def _on_search_error(self, err_msg):
        try:
            search_screen = self.root.ids.screen_manager.get_screen("search")
            if "search_status_label" in search_screen.ids:
                search_screen.ids.search_status_label.text = f"Search error ({err_msg[:30]})"
        except Exception:
            pass

    def show_lyrics(self):
        """Displays real fetched lyrics with interactive synchronized line centering, upward scrolling, and tap-to-seek."""
        track = self.player_controller.active_track
        if not track:
            return

        from kivymd.uix.label import MDLabel
        from kivymd.uix.boxlayout import MDBoxLayout
        from views.components import LyricsScrollView

        def close_lyrics(*args):
            if hasattr(self, "_lyrics_event") and self._lyrics_event:
                self._lyrics_event.cancel()
                self._lyrics_event = None
            if hasattr(self, "_lyrics_scroll_anim") and self._lyrics_scroll_anim:
                try:
                    self._lyrics_scroll_anim.stop(self._lyrics_scroll_view)
                except Exception:
                    pass
                self._lyrics_scroll_anim = None
            if hasattr(self, "_lyrics_scroll_view") and self._lyrics_scroll_view:
                if self._lyrics_scroll_view.resume_event:
                    self._lyrics_scroll_view.resume_event.cancel()
                    self._lyrics_scroll_view.resume_event = None
                self._lyrics_scroll_view.user_scrolling = False
            if hasattr(self, "lyrics_sheet") and self.lyrics_sheet:
                if self.lyrics_sheet.state != "close" and getattr(self.lyrics_sheet, "status", None) != "closing_with_animation":
                    self.lyrics_sheet.set_state("close")

        self._lyrics_drag_title = MDBottomSheetDragHandleTitle(text=f"Lyrics - {track.title[:22]}")
        self.lyrics_sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                self._lyrics_drag_title,
                MDBottomSheetDragHandleButton(icon="close", on_release=close_lyrics)
            ),
            size_hint_y=None,
            height="480dp"
        )

        def _on_sheet_closed(*args):
            if hasattr(self, "_lyrics_event") and self._lyrics_event:
                self._lyrics_event.cancel()
                self._lyrics_event = None
            if hasattr(self, "_lyrics_scroll_anim") and self._lyrics_scroll_anim:
                try:
                    self._lyrics_scroll_anim.stop(self._lyrics_scroll_view)
                except Exception:
                    pass
                self._lyrics_scroll_anim = None
            if hasattr(self, "_lyrics_scroll_view") and self._lyrics_scroll_view:
                if self._lyrics_scroll_view.resume_event:
                    self._lyrics_scroll_view.resume_event.cancel()
                    self._lyrics_scroll_view.resume_event = None
                self._lyrics_scroll_view.user_scrolling = False

        self.lyrics_sheet.bind(on_close=_on_sheet_closed)

        self._lyrics_scroll_view = LyricsScrollView(size_hint_y=None, height="400dp", do_scroll_x=False)
        self._lyrics_scroll_view.scroll_y = 1.0
        self._lyrics_box = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=["16dp", "180dp", "16dp", "200dp"],
            spacing="8dp"
        )
        self._lyrics_scroll_view.add_widget(self._lyrics_box)

        # Connect callback when user finishes manual scrolling (3s pause)
        self._lyrics_scroll_view.on_resume_callback = self._recenter_active_lyric
        self._lyrics_scroll_anim = None

        self.lyrics_sheet.add_widget(self._lyrics_scroll_view)
        Window.add_widget(self.lyrics_sheet)
        self.lyrics_sheet.width = Window.width
        self.lyrics_sheet.x = 0
        self.lyrics_sheet.set_state("open")

        self._populate_lyrics_content(track)

    def _recenter_active_lyric(self):
        """Smoothly re-centers the active lyric line to 50% viewport height, creating fluid upward scrolling."""
        if not hasattr(self, "_lyric_line_widgets") or not self._lyric_line_widgets:
            return
        if not hasattr(self, "_lyrics_scroll_view") or not self._lyrics_scroll_view:
            return
        idx = getattr(self, "_current_lyric_index", -1)
        if not (0 <= idx < len(self._lyric_line_widgets)):
            return
        _, active_box, _ = self._lyric_line_widgets[idx]
        scroll = self._lyrics_scroll_view
        box = self._lyrics_box
        H_view = scroll.height
        H_box = box.height

        # If layout pass has not finalized child positions or box height, defer to next frame
        if (H_box <= H_view or (idx == 0 and active_box.y == 0)) and len(self._lyric_line_widgets) > 2:
            Clock.schedule_once(lambda dt: self._recenter_active_lyric(), 0.05)
            return

        if H_box > H_view:
            y_target = active_box.y + active_box.height / 2.0
            target_scroll_y = max(0.0, min(1.0, (y_target - H_view / 2.0) / (H_box - H_view)))
            if hasattr(self, "_lyrics_scroll_anim") and self._lyrics_scroll_anim:
                try:
                    self._lyrics_scroll_anim.stop(scroll)
                except Exception:
                    pass
                self._lyrics_scroll_anim = None
            anim = Animation(scroll_y=target_scroll_y, duration=0.35, t="out_quad")
            self._lyrics_scroll_anim = anim
            Clock.schedule_once(lambda dt: anim.start(scroll) if hasattr(self, "_lyrics_scroll_view") and self._lyrics_scroll_view else None, 0)

    def _populate_lyrics_content(self, track):
        """Populates lyrics for track into self._lyrics_box and hooks up synchronized live tracking."""
        box = self._lyrics_box
        box.clear_widgets()
        if hasattr(self, "_lyrics_scroll_view") and self._lyrics_scroll_view:
            self._lyrics_scroll_view.scroll_y = 1.0
            self._lyrics_scroll_view.user_scrolling = False
            if self._lyrics_scroll_view.resume_event:
                self._lyrics_scroll_view.resume_event.cancel()
                self._lyrics_scroll_view.resume_event = None

        from kivymd.uix.label import MDLabel
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivy.uix.behaviors import ButtonBehavior
        from services.lyrics_service import parse_lrc, find_active_line_index, fetch_lyrics_async

        class ClickableLyricBox(ButtonBehavior, MDBoxLayout):
            pass

        if hasattr(self, "_lyrics_drag_title") and self._lyrics_drag_title:
            self._lyrics_drag_title.text = f"Lyrics - {track.title[:22]}"

        def populate_lyrics(synced_src, plain_src):
            box.clear_widgets()
            if hasattr(self, "_lyrics_scroll_view") and self._lyrics_scroll_view:
                self._lyrics_scroll_view.scroll_y = 1.0
                self._lyrics_scroll_view.user_scrolling = False
                if self._lyrics_scroll_view.resume_event:
                    self._lyrics_scroll_view.resume_event.cancel()
                    self._lyrics_scroll_view.resume_event = None

            title_lbl = MDLabel(
                text=f"{track.title}\n{track.artist}",
                font_style="Title",
                role="medium",
                bold=True,
                adaptive_height=True,
                halign="center",
                font_name=self.resolved_unicode_font_name,
                padding=["0dp", "8dp"]
            )
            box.add_widget(title_lbl)

            if synced_src:
                from kivymd.uix.button import MDButton, MDButtonText
                offset_bar = MDBoxLayout(
                    orientation="horizontal",
                    adaptive_size=True,
                    pos_hint={"center_x": .5},
                    spacing="8dp",
                    padding=["0dp", "4dp"]
                )
                btn_minus = MDButton(
                    MDButtonText(text="-0.5s"),
                    style="tonal",
                    height="32dp",
                    on_release=lambda x: self.adjust_lyrics_offset(-0.5)
                )
                btn_reset = MDButton(
                    MDButtonText(text=f"Sync ({self.lyrics_timing_offset:+.1f}s)" if self.lyrics_timing_offset != 0.0 else "Sync (0.0s)"),
                    style="text",
                    height="32dp",
                    on_release=lambda x: self.adjust_lyrics_offset(0.0)
                )
                btn_plus = MDButton(
                    MDButtonText(text="+0.5s"),
                    style="tonal",
                    height="32dp",
                    on_release=lambda x: self.adjust_lyrics_offset(+0.5)
                )
                offset_bar.add_widget(btn_minus)
                offset_bar.add_widget(btn_reset)
                offset_bar.add_widget(btn_plus)
                box.add_widget(offset_bar)

            parsed = parse_lrc(synced_src or plain_src, timing_offset=self.lyrics_timing_offset)
            if parsed:
                self._active_parsed_lyrics = parsed
                self._lyric_line_widgets = []
                self._current_lyric_index = -1

                for sec, line_text in parsed:
                    cbox = ClickableLyricBox(
                        orientation="vertical",
                        size_hint_y=None,
                        adaptive_height=True,
                        padding=["16dp", "8dp"],
                        radius=[dp(12)],
                        md_bg_color=[0, 0, 0, 0]
                    )
                    lbl = MDLabel(
                        text=line_text,
                        font_style="Body",
                        role="large",
                        adaptive_height=True,
                        halign="center",
                        font_name=self.resolved_unicode_font_name,
                        opacity=0.45,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.onSurfaceVariantColor
                    )
                    cbox.add_widget(lbl)

                    def _on_lyric_click(s_sec):
                        self.player_controller.seek(s_sec)
                        if hasattr(self, "_lyrics_scroll_view") and self._lyrics_scroll_view:
                            self._lyrics_scroll_view.user_scrolling = False
                            if self._lyrics_scroll_view.resume_event:
                                self._lyrics_scroll_view.resume_event.cancel()
                                self._lyrics_scroll_view.resume_event = None
                        Clock.schedule_once(lambda dt: self._recenter_active_lyric(), 0)

                    cbox.bind(on_release=lambda instance, s=sec: _on_lyric_click(s))
                    box.add_widget(cbox)
                    self._lyric_line_widgets.append((sec, cbox, lbl))

                box.do_layout()

                def _update_lyric_tracker(dt):
                    if not hasattr(self, "_active_parsed_lyrics") or not self._active_parsed_lyrics:
                        return
                    elapsed = getattr(self.player_controller, "current_time", 0.0)
                    idx = find_active_line_index(self._active_parsed_lyrics, elapsed)
                    if idx != getattr(self, "_current_lyric_index", -1) and 0 <= idx < len(self._lyric_line_widgets):
                        old_idx = getattr(self, "_current_lyric_index", -1)
                        if 0 <= old_idx < len(self._lyric_line_widgets):
                            _, old_box, old_lbl = self._lyric_line_widgets[old_idx]
                            old_lbl.font_style = "Body"
                            old_lbl.role = "large"
                            old_lbl.bold = False
                            old_lbl.opacity = 0.45
                            old_lbl.text_color = self.theme_cls.onSurfaceVariantColor
                            old_box.md_bg_color = [0, 0, 0, 0]

                        new_sec, new_box, new_lbl = self._lyric_line_widgets[idx]
                        new_lbl.font_style = "Title"
                        new_lbl.role = "medium"
                        new_lbl.bold = True
                        new_lbl.opacity = 1.0
                        new_lbl.text_color = self.theme_cls.primaryColor
                        new_box.md_bg_color = [self.theme_cls.primaryColor[0], self.theme_cls.primaryColor[1], self.theme_cls.primaryColor[2], 0.15]
                        self._current_lyric_index = idx

                        if hasattr(self, "_lyrics_scroll_view") and self._lyrics_scroll_view and not self._lyrics_scroll_view.user_scrolling:
                            self._recenter_active_lyric()

                if hasattr(self, "_lyrics_event") and self._lyrics_event:
                    self._lyrics_event.cancel()
                self._lyrics_event = Clock.schedule_interval(_update_lyric_tracker, 0.25)
                Clock.schedule_once(lambda dt: _update_lyric_tracker(0), 0.05)
            else:
                plain_text = plain_src or synced_src or "No lyrics found for this track."
                plain_lbl = MDLabel(
                    text=plain_text,
                    font_style="Body",
                    role="large",
                    adaptive_height=True,
                    halign="center",
                    font_name=self.resolved_unicode_font_name,
                    padding=["16dp", "16dp"]
                )
                box.add_widget(plain_lbl)

        synced = getattr(track, "synced_lyrics", "").strip()
        plain = getattr(track, "lyrics", "").strip()
        if synced or (plain and "dummy lyrics" not in plain.lower() and "fetching lyrics" not in plain.lower()):
            populate_lyrics(synced, plain)
        else:
            title_lbl = MDLabel(
                text=f"{track.title}\n{track.artist}",
                font_style="Title",
                role="medium",
                bold=True,
                adaptive_height=True,
                halign="center",
                font_name=self.resolved_unicode_font_name,
                padding=["0dp", "8dp"]
            )
            box.add_widget(title_lbl)
            loading_lbl = MDLabel(
                text="Fetching synchronized lyrics...",
                font_style="Body",
                role="medium",
                adaptive_height=True,
                halign="center",
                font_name=self.resolved_unicode_font_name,
                opacity=0.7
            )
            box.add_widget(loading_lbl)

            def on_fetched(res):
                track.lyrics = getattr(res, "plain", str(res))
                track.synced_lyrics = getattr(res, "synced", "")
                populate_lyrics(track.synced_lyrics, track.lyrics)

            fetch_lyrics_async(
                track.title, 
                track.artist, 
                track.video_id, 
                cache_dir=self.cache_dir, 
                on_success=on_fetched,
                local_path=getattr(track, "local_path", None)
            )

    def reload_lyrics_for_active_track(self):
        """Automatically updates and synchronizes lyrics when the active track changes while lyrics sheet is open."""
        track = self.player_controller.active_track
        if not track:
            return
        if hasattr(self, "_lyrics_event") and self._lyrics_event:
            self._lyrics_event.cancel()
            self._lyrics_event = None
        if hasattr(self, "_lyrics_scroll_anim") and self._lyrics_scroll_anim:
            try:
                self._lyrics_scroll_anim.stop(self._lyrics_scroll_view)
            except Exception:
                pass
            self._lyrics_scroll_anim = None
        if hasattr(self, "_lyrics_scroll_view") and self._lyrics_scroll_view:
            if self._lyrics_scroll_view.resume_event:
                self._lyrics_scroll_view.resume_event.cancel()
                self._lyrics_scroll_view.resume_event = None
            self._lyrics_scroll_view.user_scrolling = False
            self._lyrics_scroll_view.scroll_y = 1.0
        self._current_lyric_index = -1
        if hasattr(self, "_lyrics_box") and self._lyrics_box:
            self._populate_lyrics_content(track)

    def show_queue_sheet(self):
        """Display YouTube Music style Up Next bottom sheet with active queue (supports offline & online tracks)."""
        if not hasattr(self, "queue_sheet") or not self.queue_sheet:
            self.queue_sheet = MDBottomSheet(
                MDBottomSheetDragHandle(
                    MDBottomSheetDragHandleTitle(text="Up Next"),
                    MDBottomSheetDragHandleButton(
                        icon="close",
                        on_release=lambda x: self.queue_sheet.set_state("close"),
                    ),
                    drag_handle_color=self.theme_cls.onSurfaceVariantColor,
                ),
                size_hint_y=None,
                height="460dp",
            )
            self.queue_scroll = MDScrollView(size_hint=(1, 1), do_scroll_x=False)
            self.queue_box = MDList()
            self.queue_scroll.add_widget(self.queue_box)
            self.queue_sheet.add_widget(self.queue_scroll)
            Window.add_widget(self.queue_sheet)

        self.queue_sheet.width = Window.width
        self.queue_sheet.x = 0

        # Retrieve active playback queue (offline tracks or active playlist), falling back to library
        if hasattr(self, "player_controller") and self.player_controller and self.player_controller.queue:
            tracks = list(self.player_controller.queue)
        elif hasattr(self, "playlist_model") and self.playlist_model.tracks:
            tracks = list(self.playlist_model.tracks)
        else:
            tracks = []

        active = self.player_controller.active_track if hasattr(self, "player_controller") else None
        self.queue_box.clear_widgets()

        def build_queue_item(tr):
            is_active = (tr == active)
            art = tr.album_art if (tr.album_art and os.path.exists(tr.album_art)) else "album_art.png"
            item = MDListItem(
                MDListItemLeadingAvatar(
                    source=art,
                    radius=[dp(8), dp(8), dp(8), dp(8)],
                    disabled=True
                ),
                MDListItemHeadlineText(
                    text=f"▶  {tr.title}" if is_active else tr.title,
                    bold=is_active,
                    theme_text_color="Custom" if is_active else "Primary",
                    text_color=self.theme_cls.primaryColor if is_active else self.theme_cls.onSurfaceColor
                ),
                MDListItemSupportingText(
                    text=f"{tr.artist} • {tr.formatted_duration}"
                ),
                on_release=lambda x, t=tr: (
                    self.queue_sheet.set_state("close"),
                    self.play_selected_track(t)
                ),
                radius=[dp(12), dp(12), dp(12), dp(12)],
                md_bg_color=self.theme_cls.surfaceContainerHighestColor if is_active else self.theme_cls.surfaceContainerColor
            )
            return item

        # Progressive chunking: first 20 items instantaneous (<2ms), remainder in scheduled slices
        batch_size = 20
        initial_slice = tracks[:batch_size]
        for tr in initial_slice:
            self.queue_box.add_widget(build_queue_item(tr))

        def add_queue_chunks(start_idx):
            if start_idx >= len(tracks):
                return
            end_idx = min(start_idx + batch_size, len(tracks))
            for tr in tracks[start_idx:end_idx]:
                self.queue_box.add_widget(build_queue_item(tr))
            if end_idx < len(tracks):
                Clock.schedule_once(lambda dt: add_queue_chunks(end_idx), 0.03)

        if len(tracks) > batch_size:
            Clock.schedule_once(lambda dt: add_queue_chunks(batch_size), 0.03)

        self.queue_sheet.set_state("open")

    def check_responsive_layout(self, width=None):
        """Arbitrates between mobile phone layout and wide Windows/Desktop layout."""
        from kivy.core.window import Window
        from kivy.metrics import dp
        from kivy.utils import platform

        if platform in ('android', 'ios'):
            self.is_desktop_layout = False
            return

        if width is not None:
            should_be_desktop = (width >= dp(840))
        elif os.environ.get("KIVY_HEADLESS") == "1":
            should_be_desktop = self.is_desktop_layout
        else:
            w = Window.width
            should_be_desktop = (w >= dp(840))

        if self.is_desktop_layout != should_be_desktop:
            self.is_desktop_layout = should_be_desktop
            if not should_be_desktop and self.desktop_panel_open:
                self.desktop_panel_open = False

    def close_desktop_panel(self):
        """Closes the desktop inspector side panel."""
        self.desktop_panel_open = False
        if hasattr(self, "_desktop_lyrics_event") and self._desktop_lyrics_event:
            self._desktop_lyrics_event.cancel()
            self._desktop_lyrics_event = None

    def toggle_desktop_lyrics_panel(self):
        """Toggles the synced lyrics inspector in the desktop side panel (or mobile sheet)."""
        if not self.is_desktop_layout:
            self.show_lyrics()
            return
        if self.desktop_panel_open and self.desktop_panel_tab == "lyrics":
            self.close_desktop_panel()
        else:
            self.desktop_panel_tab = "lyrics"
            self.desktop_panel_open = True
            self.sync_desktop_side_panel()

    def toggle_desktop_queue_panel(self):
        """Toggles the Up Next queue inspector in the desktop side panel (or mobile sheet)."""
        if not self.is_desktop_layout:
            self.show_queue_sheet()
            return
        if self.desktop_panel_open and self.desktop_panel_tab == "queue":
            self.close_desktop_panel()
        else:
            self.desktop_panel_tab = "queue"
            self.desktop_panel_open = True
            self.sync_desktop_side_panel()

    def sync_desktop_side_panel(self):
        """Populates and refreshes the desktop side panel with active lyrics or queue."""
        if not hasattr(self, "root") or not self.root or not hasattr(self.root, "ids"):
            return
        side_panel = self.root.ids.get("desktop_side_panel")
        if not side_panel or "desktop_panel_content" not in side_panel.ids:
            return

        content = side_panel.ids.desktop_panel_content
        content.clear_widgets()

        if self.desktop_panel_tab == "queue":
            self._populate_desktop_queue_content(content)
        elif self.desktop_panel_tab == "lyrics":
            self._populate_desktop_lyrics_content(content)

    def _populate_desktop_queue_content(self, container):
        from kivymd.uix.scrollview import MDScrollView
        from kivymd.uix.list import MDList, MDListItem, MDListItemLeadingAvatar, MDListItemHeadlineText, MDListItemSupportingText
        from kivy.metrics import dp

        scroll = MDScrollView(size_hint=(1, 1), do_scroll_x=False)
        box = MDList(spacing="4dp")
        scroll.add_widget(box)
        container.add_widget(scroll)

        tracks = list(self.player_controller.queue) if (hasattr(self, "player_controller") and self.player_controller.queue) else []
        active = self.player_controller.active_track if hasattr(self, "player_controller") else None

        for tr in tracks:
            is_active = (tr == active)
            art = tr.album_art if (tr.album_art and os.path.exists(tr.album_art)) else "album_art.png"
            item = MDListItem(
                MDListItemLeadingAvatar(
                    source=art,
                    radius=[dp(8), dp(8), dp(8), dp(8)],
                    disabled=True
                ),
                MDListItemHeadlineText(
                    text=f"▶  {tr.title}" if is_active else tr.title,
                    bold=is_active,
                    theme_text_color="Custom" if is_active else "Primary",
                    text_color=self.theme_cls.primaryColor if is_active else self.theme_cls.onSurfaceColor
                ),
                MDListItemSupportingText(
                    text=f"{tr.artist} • {tr.formatted_duration}"
                ),
                on_release=lambda x, t=tr: self.play_selected_track(t),
                radius=[dp(12), dp(12), dp(12), dp(12)],
                md_bg_color=self.theme_cls.surfaceContainerHighestColor if is_active else self.theme_cls.surfaceContainerColor
            )
            box.add_widget(item)

    def _populate_desktop_lyrics_content(self, container):
        from views.components import LyricsScrollView
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDButton, MDButtonText
        from services.lyrics_service import parse_lrc, find_active_line_index, fetch_lyrics_async
        from kivy.metrics import dp

        track = self.player_controller.active_track if hasattr(self, "player_controller") else None
        if not track:
            lbl = MDLabel(
                text="No track playing",
                halign="center",
                font_style="Body",
                role="medium",
                pos_hint={"center_y": .5}
            )
            container.add_widget(lbl)
            return

        # Header Info Row
        header_box = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing="2dp", padding=["4dp", "4dp", "4dp", "8dp"])
        title_lbl = MDLabel(
            text=track.title,
            font_style="Title",
            role="medium",
            bold=True,
            halign="center",
            adaptive_height=True,
            font_name=self.resolved_unicode_font_name
        )
        artist_lbl = MDLabel(
            text=track.artist,
            font_style="Body",
            role="small",
            halign="center",
            adaptive_height=True,
            text_color=self.theme_cls.onSurfaceVariantColor,
            font_name=self.resolved_unicode_font_name
        )
        header_box.add_widget(title_lbl)
        header_box.add_widget(artist_lbl)

        # Timing offset row for desktop
        offset_row = MDBoxLayout(orientation="horizontal", adaptive_size=True, pos_hint={"center_x": .5}, spacing="8dp", padding=["8dp", "4dp", "8dp", "8dp"])
        btn_minus = MDButton(style="outlined", size_hint=(None, None), size=("68dp", "34dp"), on_release=lambda x: self.adjust_lyrics_offset(-0.5))
        btn_minus.add_widget(MDButtonText(text="-0.5s"))
        offset_lbl = MDLabel(text=f"Sync: {self.lyrics_timing_offset:+.1f}s", halign="center", font_style="Label", role="small", adaptive_width=True)
        btn_plus = MDButton(style="outlined", size_hint=(None, None), size=("68dp", "34dp"), on_release=lambda x: self.adjust_lyrics_offset(+0.5))
        btn_plus.add_widget(MDButtonText(text="+0.5s"))
        offset_row.add_widget(btn_minus)
        offset_row.add_widget(offset_lbl)
        offset_row.add_widget(btn_plus)

        header_box.add_widget(offset_row)
        container.add_widget(header_box)

        lyrics_scroll = LyricsScrollView(size_hint=(1, 1), do_scroll_x=False)
        lyrics_box = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=["12dp", "60dp", "12dp", "100dp"],
            spacing="10dp"
        )
        lyrics_scroll.add_widget(lyrics_box)
        container.add_widget(lyrics_scroll)

        self._desktop_lyrics_scroll = lyrics_scroll
        self._desktop_lyrics_box = lyrics_box
        self._desktop_lyric_widgets = []

        def render_desktop_lyrics(synced_src, plain_src):
            lyrics_box.clear_widgets()
            self._desktop_lyric_widgets = []
            if synced_src:
                parsed = parse_lrc(synced_src, timing_offset=self.lyrics_timing_offset)
                if parsed:
                    for sec, text in parsed:
                        lbl = MDLabel(
                            text=text,
                            font_style="Title",
                            role="medium",
                            halign="center",
                            adaptive_height=True,
                            text_color=self.theme_cls.onSurfaceVariantColor,
                            font_name=self.resolved_unicode_font_name
                        )
                        lyrics_box.add_widget(lbl)
                        self._desktop_lyric_widgets.append((sec, lbl))
                    return
            
            # Plain fallback
            text_to_show = plain_src if plain_src else "No synchronized lyrics found."
            lbl = MDLabel(
                text=text_to_show,
                font_style="Body",
                role="medium",
                halign="center",
                adaptive_height=True,
                font_name=self.resolved_unicode_font_name
            )
            lyrics_box.add_widget(lbl)

        synced = getattr(track, "synced_lyrics", "").strip()
        plain = getattr(track, "lyrics", "").strip()
        if synced or plain:
            render_desktop_lyrics(synced, plain)
        else:
            loading_lbl = MDLabel(
                text="Fetching lyrics...",
                font_style="Body",
                role="medium",
                halign="center",
                adaptive_height=True,
                opacity=0.7
            )
            lyrics_box.add_widget(loading_lbl)

            def on_fetched(res):
                track.lyrics = getattr(res, "plain", str(res))
                track.synced_lyrics = getattr(res, "synced", "")
                render_desktop_lyrics(track.synced_lyrics, track.lyrics)

            fetch_lyrics_async(track.artist, track.title, getattr(track, "duration", 0), on_success=on_fetched)

        def _update_desktop_lyrics_tick(dt):
            if not self.desktop_panel_open or self.desktop_panel_tab != "lyrics":
                return False
            if not self.player_controller:
                return True
            cur_time = self.player_controller.current_time + self.lyrics_timing_offset
            active_idx = -1
            for i, (t_sec, w) in enumerate(self._desktop_lyric_widgets):
                if t_sec <= cur_time:
                    active_idx = i
                else:
                    break
            for i, (t_sec, w) in enumerate(self._desktop_lyric_widgets):
                if i == active_idx:
                    w.text_color = self.theme_cls.primaryColor
                    w.bold = True
                else:
                    w.text_color = self.theme_cls.onSurfaceVariantColor
                    w.bold = False
            return True

        if hasattr(self, "_desktop_lyrics_event") and self._desktop_lyrics_event:
            self._desktop_lyrics_event.cancel()
        self._desktop_lyrics_event = Clock.schedule_interval(_update_desktop_lyrics_tick, 0.25)

    def toggle_fullscreen(self):
        """Toggles window fullscreen mode for immersive desktop listening."""
        from kivy.core.window import Window
        Window.fullscreen = not Window.fullscreen

    def set_volume(self, val):
        """Sets playback volume in range [0.0, 1.0]."""
        self.current_volume = max(0.0, min(1.0, float(val)))
        if hasattr(self, "player_controller") and self.player_controller:
            self.player_controller.set_volume(self.current_volume)

    def toggle_mute(self):
        """Toggles audio mute state."""
        if hasattr(self, "player_controller") and self.player_controller:
            self.player_controller.toggle_mute()
            self.current_volume = 0.0 if self.player_controller.is_muted else self.player_controller.volume

    def adjust_volume_delta(self, delta):
        """Adjusts playback volume incrementally (e.g. keyboard Up/Down arrows)."""
        if hasattr(self, "player_controller") and self.player_controller:
            self.player_controller.adjust_volume(delta)
            self.current_volume = self.player_controller.volume

    def on_stop(self):
        """Clean up audio streams, threads, and background workers on application exit."""
        if hasattr(self, "player_controller") and self.player_controller:
            self.player_controller.stop()

if __name__ == '__main__':
    MusicApp().run()
