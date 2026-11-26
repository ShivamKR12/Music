"""
KivyMusicApp Application Shell.

Bootstraps Kivy graphics configuration, system Unicode fonts, Python 3.12+
safe Animation updates, and MusicApp(MDApp) reactive Kivy properties while
delegating application state, services, navigation, lifecycle, settings,
lyrics, catalog, search, and playback UI cleanly to single-responsibility
coordinators under `app_core/`.
"""

import os
import sys

from kivy.config import Config
from kivy.utils import platform

# Hardware & mobile graphics optimizations (Mali GPU fill rate, VSync, thread pooling)
Config.set("graphics", "multisamples", "0")
Config.set("graphics", "vsync", "1")
Config.set("graphics", "maxfps", "60")
Config.set("kivy", "log_level", "info")

from kivy.loader import Loader

Loader.num_workers = 4
Loader.max_cache = 400

if platform in ("win", "macosx", "linux"):
    Config.set("graphics", "width", "360")
    Config.set("graphics", "height", "640")
    Config.set("graphics", "resizable", False)
    Config.set("graphics", "fullscreen", False)

from kivy.animation import Animation
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons

# Register Discord icon fallback if missing in active Material icon font
if "discord" not in md_icons:
    md_icons["discord"] = md_icons.get("controller", md_icons.get("gamepad", "chat"))


# Thread-safe & re-entrancy safe Animation._update patch for Python 3.12+
def _update(self, dt):
    widgets = self._widgets
    transition = self._transition
    calculate = self._calculate
    for uid in list(widgets.keys()):
        if uid not in widgets:
            continue
        anim_data = widgets[uid]
        widget = anim_data.get("widget")

        from kivy.weakproxy import WeakProxy

        if isinstance(widget, WeakProxy) and not len(dir(widget)):
            widgets.pop(uid, None)
            self._clock_uninstall()
            if not widgets:
                self._unregister()
            continue

        if anim_data.get("time") is None:
            anim_data["time"] = 0.0
        else:
            anim_data["time"] += dt

        progress = min(1.0, anim_data["time"] / self._duration) if self._duration else 1
        t = transition(progress)

        for key, values in list(anim_data.get("properties", {}).items()):
            if uid not in widgets or key not in anim_data.get("properties", {}):
                continue
            a, b = values
            value = calculate(a, b, t)
            try:
                setattr(widget, key, value)
            except Exception:
                pass

        try:
            self.dispatch("on_progress", widget, progress)
        except Exception:
            pass

        if progress >= 1.0:
            try:
                self.stop(widget)
            except Exception:
                pass


Animation._update = _update
Animation._safe_anim_update = _update


def _anim_getattr(self, name):
    if name in ("_update", "_safe_anim_update", "safe_update"):
        return self._update
    raise AttributeError(f"'Animation' object has no attribute '{name}'")


Animation.__getattr__ = _anim_getattr

# Modular coordinators & repository/system font setup
from app_core import (
    AppBootstrap,
    ApplicationLifecycle,
    AppState,
    CatalogCoordinator,
    LyricsCoordinator,
    NavigationCoordinator,
    PlaybackUICoordinator,
    PlaylistOptionsCoordinator,
    SearchCoordinator,
    ServiceContainer,
    SettingsCoordinator,
    resolve_and_register_system_fonts,
)
from app_core.state import EQ_PRESETS, HEADPHONE_PROFILES, PROVIDER_LABELS, SEARCH_PLACEHOLDERS

# Re-exported database & utility symbols for test/benchmark compatibility
from models.database import (  # noqa: F401
    add_playlist,
    add_search_history,
    add_search_history_async,
    add_track,
    add_track_to_playlist,
    clear_search_history,
    clear_search_history_async,
    delete_playlist,
    flush_db_writes,
    get_all_playlists,
    get_all_podcasts,
    get_all_settings,
    get_all_tracks,
    get_continue_listening,
    get_daily_mix,
    get_dynamic_playlist_tracks,
    get_forgotten_favorites,
    get_heavy_rotation,
    get_library_analytics_summary,
    get_on_repeat,
    get_playlist_covers,
    get_playlist_tracks,
    get_recently_added,
    get_recently_played,
    get_search_history,
    get_setting,
    get_top_artists,
    init_db,
    is_favorite,
    load_cache_payload,
    remove_track_from_playlist,
    save_cache_payload,
    set_setting,
    set_setting_async,
    toggle_favorite,
    update_local_track_path,
    update_track_artwork,
)
from services.logger import (  # noqa: F401
    LogLevel,
    app_logger,
    get_current_log_level_name,
    init_logging,
    log_file,
    set_log_level,
)
from services.telemetry_service import get_telemetry
from utils.media_utils import (  # noqa: F401
    download_artwork,
    enforce_max_cache_size,
    ensure_artworks_downloaded,
    extract_video_id,
    fetch_youtube_metadata,
    get_cache_dir,
    get_thumbnail_path,
    is_podcast_item,
    parse_complete_media_metadata,
)
from utils.theme_utils import update_theme_from_image  # noqa: F401
import views.components  # noqa: F401 - register custom components with Kivy Factory
import views.screens  # noqa: F401 - register screen classes with Kivy Factory

RESOLVED_FONT_PATH, RESOLVED_FONT_NAME = resolve_and_register_system_fonts()
logger = app_logger


class MusicApp(MDApp):
    """Reactive KivyMD root app delegating domain logic to modular coordinators."""

    player_controller = ObjectProperty(None)
    mini_player_visible = BooleanProperty(False)
    mini_player_dismissed = BooleanProperty(False)
    selected_audio_quality = StringProperty("High (320kbps)")
    selected_eq_profile = StringProperty("Flat")
    active_playlist_name = StringProperty("Favorites")
    active_playlist_artwork = StringProperty("album_art2.png")
    active_playlist_info = StringProperty("0 tracks")
    active_playlist_tracks = ListProperty([])

    UI_MODE_NEW = "new"
    UI_MODE_CLASSIC = "classic"
    ui_mode = StringProperty("new")
    library_filter = StringProperty("Library")

    search_state = StringProperty("empty")
    search_loading = BooleanProperty(False)
    active_search_provider = StringProperty("all")
    search_placeholder = StringProperty("Search for songs...")

    album_loading = BooleanProperty(False)
    podcasts_loading = BooleanProperty(False)

    home_mood = StringProperty("All")
    home_greeting = StringProperty("Welcome back")
    home_header_texture = ObjectProperty(None, allownone=True)
    player_background_texture = ObjectProperty(None, allownone=True)
    current_lyric_line = StringProperty("Tap for synchronized lyrics")

    eq_bands = ListProperty([0.0] * 10)
    eq_reverb = BooleanProperty(False)
    eq_bass_boost = NumericProperty(0.0)

    listen_together_active = BooleanProperty(False)
    listen_together_room_id = StringProperty("")
    listen_together_role = StringProperty("idle")
    listen_together_status = StringProperty("Disconnected")
    listen_together_members = ListProperty([])

    EQ_PRESETS = EQ_PRESETS
    HEADPHONE_PROFILES = HEADPHONE_PROFILES
    PROVIDER_LABELS = PROVIDER_LABELS
    SEARCH_PLACEHOLDERS = SEARCH_PLACEHOLDERS

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

    cache_size_label = StringProperty("Calculating...")
    selected_music_provider = StringProperty("all")
    selected_music_provider_label = StringProperty("Unified (All Sources)")

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

    active_tab_name = StringProperty("home")
    current_volume = NumericProperty(1.0)

    @property
    def cache_dir(self):
        return get_cache_dir()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Construct single-responsibility coordinators cleanly (GEMINI.md Section 3)
        self.app_state = AppState(self)
        self.services = ServiceContainer(self)
        self.bootstrap = AppBootstrap(self)
        self.lifecycle = ApplicationLifecycle(self)
        self.navigation = NavigationCoordinator(self)
        self.settings_coord = SettingsCoordinator(self)
        self.playback_ui = PlaybackUICoordinator(self)
        self.lyrics_coord = LyricsCoordinator(self)
        self.playlist_options = PlaylistOptionsCoordinator(self)
        self.catalog = CatalogCoordinator(self)
        self.search_coord = SearchCoordinator(self)

        # Initialize state, services, persisted DB preferences, and player stack
        self.app_state.init_ui_handles()
        self.services.initialize_core_services()
        self.app_state.hydrate_settings_from_db()
        self.refresh_cache_size()
        self.services.wire_player_stack()

    # =========================================================================
    # Bootstrap & Telemetry Entrypoints
    # =========================================================================
    def build(self): return self.bootstrap.build_root()
    def on_start(self): return self.bootstrap.on_start()
    def start_warmup_pipeline(self): return self.bootstrap.start_warmup_pipeline()
    def _deferred_screen_prewarm(self, sm, names=None, index=0): return self.bootstrap.deferred_screen_prewarm(sm, names, index)
    def _stage_1_populate_home(self, dt=None): return self.bootstrap.stage_1_populate_home(dt)
    def _stage_2_populate_library_and_history(self, dt=None): return self.bootstrap.stage_2_populate_library_and_history(dt)
    def _cycle_search_placeholder(self, *args): return self.bootstrap.cycle_search_placeholder(*args)
    def _start_idle_prewarming(self, dt=None): return self.bootstrap.start_idle_prewarming(dt)
    def _prewarm_next_screen(self, dt=None): return self.bootstrap.prewarm_next_screen(dt)
    def _stage_3_apply_initial_theme(self, dt=None): return self.bootstrap.stage_3_apply_initial_theme(dt)
    def _stage_4_background_tasks(self, dt=None): return self.bootstrap.stage_4_background_tasks(dt)
    def _refresh_home_header_texture(self, *args): return self.bootstrap.refresh_home_header_texture(*args)
    def _refresh_player_background_texture(self, *args): return self.bootstrap.refresh_player_background_texture(*args)
    def get_telemetry_snapshot(self): return get_telemetry().snapshot(sample_rss_now=True)
    def _telemetry_sample_frame(self, dt): get_telemetry().record_frame_dt(dt)
    def _telemetry_sample_memory(self, dt): get_telemetry().sample_memory(min_interval_seconds=0.0)

    # =========================================================================
    # Lifecycle Entrypoints
    # =========================================================================
    def on_request_close(self, *args, **kwargs): return self.lifecycle.on_request_close(*args, **kwargs)
    def smooth_exit(self): return self.lifecycle.smooth_exit()
    def on_pause(self): return self.lifecycle.on_pause()
    def on_resume(self): return self.lifecycle.on_resume()
    def restore_last_session(self): return self.lifecycle.restore_last_session()
    def on_stop(self): return self.lifecycle.on_stop()

    # =========================================================================
    # Navigation Entrypoints
    # =========================================================================
    def toggle_ui_mode(self): return self.navigation.toggle_ui_mode()
    def switch_ui_mode(self, mode): return self.navigation.switch_ui_mode(mode)
    def switch_screen(self, screen_name: str): return self.navigation.switch_screen(screen_name)
    def go_back(self, target=None): return self.navigation.go_back(target=target)
    def on_keyboard(self, window, key, scancode=None, codepoint=None, modifier=None, *args, **kwargs): return self.navigation.on_keyboard(window, key, scancode, codepoint, modifier, *args, **kwargs)
    def on_switch_tabs(self, bar, item, item_icon: str, item_text: str): return self.navigation.on_switch_tabs(bar, item, item_icon, item_text)
    def sync_nav_bar(self, screen_name: str): return self.navigation.sync_nav_bar(screen_name)

    # =========================================================================
    # Settings, Theme & Equalizer Entrypoints
    # =========================================================================
    def toggle_wifi_only(self): return self.settings_coord.toggle_wifi_only()
    def set_wifi_only(self, is_enabled: bool): return self.settings_coord.set_wifi_only(is_enabled)
    def toggle_dark_mode(self): return self.settings_coord.toggle_dark_mode()
    def toggle_theme_style(self, is_dark: bool): return self.settings_coord.toggle_theme_style(is_dark)
    def toggle_extract_artwork_colors(self, is_enabled=None): return self.settings_coord.toggle_extract_artwork_colors(is_enabled)
    def toggle_animated_bg(self, is_enabled=None): return self.settings_coord.toggle_animated_bg(is_enabled)
    def toggle_sponsorblock(self): return self.settings_coord.toggle_sponsorblock()
    def set_sponsorblock_enabled(self, is_enabled: bool): return self.settings_coord.set_sponsorblock_enabled(is_enabled)
    def toggle_discord_rpc(self): return self.settings_coord.toggle_discord_rpc()
    def show_crossfade_dialog(self): return self.settings_coord.show_crossfade_dialog()
    def set_crossfade_duration(self, seconds: float): return self.settings_coord.set_crossfade_duration(seconds)
    def apply_autoeq_profile(self, profile_name: str): return self.settings_coord.apply_autoeq_profile(profile_name)
    def adjust_lyrics_offset(self, delta: float): return self.settings_coord.adjust_lyrics_offset(delta)
    def update_player_animated_bg(self): return self.settings_coord.update_player_animated_bg()
    def show_animated_bg_style_dialog(self): return self.settings_coord.show_animated_bg_style_dialog()
    def cycle_animated_bg_speed(self): return self.settings_coord.cycle_animated_bg_speed()
    def show_audio_quality_dialog(self): return self.settings_coord.show_audio_quality_dialog()
    def show_toast(self, msg: str): return self.settings_coord.show_toast(msg)
    def refresh_cache_size(self): return self.settings_coord.refresh_cache_size()
    def show_clear_cache_dialog(self): return self.settings_coord.show_clear_cache_dialog()
    def execute_clear_cache(self): return self.settings_coord.execute_clear_cache()
    def show_provider_selector_dialog(self): return self.settings_coord.show_provider_selector_dialog()
    def resync_offline_library_action(self): return self.settings_coord.resync_offline_library_action()
    def show_about_dialog(self): return self.settings_coord.show_about_dialog()
    def show_logs_dialog(self): return self.settings_coord.show_logs_dialog()
    def show_log_level_dialog(self): return self.settings_coord.show_log_level_dialog()
    def show_sleep_timer_dialog(self): return self.settings_coord.show_sleep_timer_dialog()
    def show_reset_settings_dialog(self): return self.settings_coord.show_reset_settings_dialog()
    def apply_eq_profile(self, profile_name: str): return self.settings_coord.apply_eq_profile(profile_name)
    def on_eq_slider_change(self, band_index: int, value: float): return self.settings_coord.on_eq_slider_change(band_index, value)
    def reset_eq(self): return self.settings_coord.reset_eq()
    def toggle_eq_reverb(self, active: bool): return self.settings_coord.toggle_eq_reverb(active)
    def apply_audio_eq(self): return self.settings_coord.apply_audio_eq()
    def show_autoeq_profile_dialog(self): return self.settings_coord.show_autoeq_profile_dialog()
    def show_auth_dialog(self, provider: str): return self.settings_coord.show_auth_dialog(provider)

    # =========================================================================
    # Playback UI, Carousel, Queue, Volume & Listen Together Entrypoints
    # =========================================================================
    def on_player_playing_change(self, instance, is_playing): return self.playback_ui.on_player_playing_change(instance, is_playing)
    def on_active_track_change(self, instance, track): return self.playback_ui.on_active_track_change(instance, track)
    def ensure_player_carousel(self, force_refresh=False): return self.playback_ui.ensure_player_carousel(force_refresh=force_refresh)
    def sync_player_carousel_track(self, track): return self.playback_ui.sync_player_carousel_track(track)
    def on_carousel_index(self, index): return self.playback_ui.on_carousel_index(index)
    def dismiss_mini_player(self): return self.playback_ui.dismiss_mini_player()
    def play_selected_track(self, track): return self.playback_ui.play_selected_track(track)
    def file_manager_open(self): return self.playback_ui.file_manager_open()
    def select_path(self, path): return self.playback_ui.select_path(path)
    def exit_manager(self, *args): return self.playback_ui.exit_manager(*args)
    def show_queue_sheet(self): return self.playback_ui.show_queue_sheet()
    def set_volume(self, val): return self.playback_ui.set_volume(val)
    def toggle_mute(self): return self.playback_ui.toggle_mute()
    def adjust_volume_delta(self, delta): return self.playback_ui.adjust_volume_delta(delta)
    def on_listen_together_state_changed(self, status: str, room_code: str): return self.playback_ui.on_listen_together_state_changed(status, room_code)
    def on_listen_together_members_updated(self, members: list): return self.playback_ui.on_listen_together_members_updated(members)
    def on_listen_together_playback_sync(self, msg: dict): return self.playback_ui.on_listen_together_playback_sync(msg)
    def broadcast_listen_together_state(self): return self.playback_ui.broadcast_listen_together_state()
    def create_listen_together_room(self): return self.playback_ui.create_listen_together_room()
    def show_join_listen_together_dialog(self): return self.playback_ui.show_join_listen_together_dialog()
    def copy_listen_together_code(self): return self.playback_ui.copy_listen_together_code()
    def add_demo_listen_together_peer(self): return self.playback_ui.add_demo_listen_together_peer()
    def leave_listen_together(self): return self.playback_ui.leave_listen_together()

    # =========================================================================
    # Synchronized Lyrics Entrypoints
    # =========================================================================
    def on_player_time_change(self, instance, current_time): return self.lyrics_coord.on_player_time_change(instance, current_time)
    def show_lyrics_sheet(self): return self.lyrics_coord.show_lyrics_sheet()
    def show_lyrics(self): return self.lyrics_coord.show_lyrics()
    def _recenter_active_lyric(self): return self.lyrics_coord.recenter_active_lyric()
    def _populate_lyrics_content(self, track): return self.lyrics_coord.populate_lyrics_content(track)
    def reload_lyrics_for_active_track(self): return self.lyrics_coord.reload_lyrics_for_active_track()
    def populate_inline_lyrics(self): return self.lyrics_coord.populate_inline_lyrics()
    def _recenter_inline_lyric(self): return self.lyrics_coord.recenter_inline_lyric()

    # =========================================================================
    # Playlist, Offline Download & Track Options Entrypoints
    # =========================================================================
    def show_add_playlist_dialog(self, track_to_add=None): return self.playlist_options.show_add_playlist_dialog(track_to_add=track_to_add)
    def show_import_spotify_dialog(self): return self.playlist_options.show_import_spotify_dialog()
    def import_spotify_playlist(self, url: str): return self.playlist_options.import_spotify_playlist(url)
    def open_playlist(self, playlist_name: str): return self.playlist_options.open_playlist(playlist_name)
    def _fetch_playlist_tracks_async(self, playlist_name: str): return self.playlist_options.fetch_playlist_tracks_async(playlist_name)
    def sync_active_playlist_screen(self): return self.playlist_options.sync_active_playlist_screen()
    def play_active_playlist(self, shuffle=False): return self.playlist_options.play_active_playlist(shuffle=shuffle)
    def download_active_playlist(self, playlist_name=None): return self.playlist_options.download_active_playlist(playlist_name=playlist_name)
    def show_playlists_overview(self): return self.playlist_options.show_playlists_overview()
    def show_add_to_active_playlist_sheet(self): return self.playlist_options.show_add_to_active_playlist_sheet()
    def show_playlist_options(self): return self.playlist_options.show_playlist_options()
    def show_add_to_playlist_sheet(self, track=None): return self.playlist_options.show_add_to_playlist_sheet(track=track)
    def download_track_offline(self, track): return self.playlist_options.download_track_offline(track)
    def _on_download_finished(self, track, success): return self.playlist_options.on_download_finished(track, success)
    def show_track_options(self): return self.playlist_options.show_track_options()

    # =========================================================================
    # Catalog, Home Shelves, Library, Artist, Album, Podcasts & Local Scan
    # =========================================================================
    def get_greeting(self): return self.catalog.get_greeting()
    def on_artwork_downloaded(self, track, art_path): return self.catalog.on_artwork_downloaded(track, art_path)
    def _debounced_refresh_views(self, dt=None): return self.catalog.debounced_refresh_views(dt)
    def get_track_object_from_row(self, r): return self.catalog.get_track_object_from_row(r)
    def load_recently_played_data(self): return self.catalog.load_recently_played_data()
    def load_analytics_data(self): return self.catalog.load_analytics_data()
    def populate_home_screen_data(self): return self.catalog.populate_home_screen_data()
    def _bg_fetch_dynamic_recommendations(self, mood="All"): return self.catalog.bg_fetch_dynamic_recommendations(mood=mood)
    def _apply_dynamic_shelves(self, shelves): return self.catalog.apply_dynamic_shelves(shelves)
    def _fetch_trending_tracks(self): return self.catalog.fetch_trending_tracks()
    def _on_trending_fetched(self): return self.catalog.on_trending_fetched()
    def select_mood_filter(self, chip_instance, mood: str): return self.catalog.select_mood_filter(chip_instance, mood)
    def _async_mood_search(self, mood: str): return self.catalog.async_mood_search(mood)
    def _on_mood_results(self, entries, mood): return self.catalog.on_mood_results(entries, mood)
    def play_home_shelf(self, shelf_id: str): return self.catalog.play_home_shelf(shelf_id)
    def play_home_quick_picks(self): return self.catalog.play_home_quick_picks()
    def select_library_filter(self, chip_instance, filter_name: str): return self.catalog.select_library_filter(chip_instance, filter_name)
    def refresh_library_data(self): return self.catalog.refresh_library_data()
    def _update_library_tile(self, lib, fan_id, artworks): return self.catalog.update_library_tile(lib, fan_id, artworks)
    @staticmethod
    def is_user_library_playlist(name: str) -> bool: return CatalogCoordinator.is_user_library_playlist(name)
    def _populate_playlists_grid(self): return self.catalog.populate_playlists_grid()
    def _sync_library_songs(self): return self.catalog.sync_library_songs()
    def open_album(self, album_name="New Releases", artist_name="Various Artists", artwork="album_art.png", tracks=None): return self.catalog.open_album(album_name, artist_name, artwork, tracks)
    def _render_album_tracks(self): return self.catalog.render_album_tracks()
    def _fetch_album_tracks_async(self, album_name: str, artist_name: str): return self.catalog.fetch_album_tracks_async(album_name, artist_name)
    def play_active_album(self, shuffle=False): return self.catalog.play_active_album(shuffle=shuffle)
    def open_artist(self, artist_name=None): return self.catalog.open_artist(artist_name=artist_name)
    def _fetch_artist_data_async(self, primary_artist: str): return self.catalog.fetch_artist_data_async(primary_artist)
    def play_active_artist(self, shuffle=False): return self.catalog.play_active_artist(shuffle=shuffle)
    def show_artist(self, artist_name=""): return self.catalog.show_artist(artist_name=artist_name)
    def open_podcasts(self): return self.catalog.open_podcasts()
    def load_podcasts_data(self): return self.catalog.load_podcasts_data()
    def _render_podcasts_list(self): return self.catalog.render_podcasts_list()
    def play_featured_podcast(self): return self.catalog.play_featured_podcast()
    def show_favorites(self): return self.catalog.show_favorites()
    def play_favorites(self, shuffle=False): return self.catalog.play_favorites(shuffle=shuffle)
    def sync_favorites_screen(self): return self.catalog.sync_favorites_screen()
    def show_downloaded(self): return self.catalog.show_downloaded()
    def show_local_audio_options(self): return self.catalog.show_local_audio_options()
    def ensure_storage_permissions(self, callback=None): return self.catalog.ensure_storage_permissions(callback=callback)
    def scan_and_load_offline_songs(self, auto_play=False, show_screen=True): return self.catalog.scan_and_load_offline_songs(auto_play=auto_play, show_screen=show_screen)

    # =========================================================================
    # Search Entrypoints
    # =========================================================================
    def clear_search_input(self): return self.search_coord.clear_search_input()
    def set_search_provider(self, provider: str): return self.search_coord.set_search_provider(provider)
    def load_search_history_from_db(self): return self.search_coord.load_search_history_from_db()
    def clear_search_history(self): return self.search_coord.clear_search_history()
    def clear_search_results(self): return self.search_coord.clear_search_results()
    def on_search_text_change(self, text: str): return self.search_coord.on_search_text_change(text)
    def perform_search(self, query: str): return self.search_coord.perform_search(query)
    def _async_url_extractor(self, url: str): return self.search_coord.async_url_extractor(url)
    def _on_url_extracted(self, meta): return self.search_coord.on_url_extracted(meta)
    def _async_spotify_extractor(self, url: str): return self.search_coord.async_spotify_extractor(url)
    def _async_yt_search(self, query: str): return self.search_coord.async_yt_search(query)
    def _on_search_results(self, entries, query): return self.search_coord.on_search_results(entries, query)
    def on_search_artwork_downloaded(self, track, art_path): return self.search_coord.on_search_artwork_downloaded(track, art_path)
    def _on_search_error(self, err_msg): return self.search_coord.on_search_error(err_msg)


if __name__ == "__main__":
    MusicApp().run()
