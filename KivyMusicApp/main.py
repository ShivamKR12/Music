from kivy.config import Config
from kivy.utils import platform
if platform in ('win', 'macosx', 'linux'):
    Config.set('graphics', 'width', '360')
    Config.set('graphics', 'height', '640')
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'fullscreen', False)

import os
import threading
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
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

from models.database import (
    init_db,
    add_track,
    get_all_tracks,
    get_playlist_tracks,
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
)
from services.lyrics_service import fetch_lyrics_async, get_cached_lyrics
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
)
from utils.theme_utils import update_theme_from_image
from services.logger import app_logger, init_logging
from utils.media_utils import (
    enforce_max_cache_size,
    extract_video_id,
    fetch_youtube_metadata,
    get_thumbnail_path,
    download_artwork,
    ensure_artworks_downloaded,
)

class MusicApp(MDApp):
    selected_audio_quality = StringProperty("High (320kbps)")
    selected_eq_profile = StringProperty("Flat")
    active_playlist_name = StringProperty("Favorites")
    active_playlist_artwork = StringProperty("album_art2.png")
    active_playlist_info = StringProperty("0 tracks")
    active_playlist_tracks = ListProperty([])

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
        self.screen_history = []
        
        # MVC Initialization
        init_db()
        self.playlist_model = PlaylistModel()
        self.player_controller = PlayerController()
        self.player_controller.set_playlist(self.playlist_model)
        
        # Set default track
        if self.playlist_model.tracks:
            self.player_controller.set_track(self.playlist_model.tracks[0])
            
        self.player_controller.bind(active_track=self.on_active_track_change)

    def on_active_track_change(self, instance, track):
        """Automatically harmonize Material You palette with new track album art."""
        if track and hasattr(track, "album_art") and track.album_art:
            update_theme_from_image(track.album_art)

    def toggle_theme_style(self, is_dark: bool):
        """Toggle between Dark and Light Material Design 3 theme styles."""
        self.theme_cls.theme_style = "Dark" if is_dark else "Light"
        if self.player_controller.active_track:
            update_theme_from_image(self.player_controller.active_track.album_art)

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
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.dynamic_color = True
        root = Builder.load_file(os.path.join("views", "main.kv"))
        Window.bind(on_keyboard=self.on_keyboard)
        # Enforce disk cache footprint limits in a background daemon thread
        threading.Thread(target=enforce_max_cache_size, kwargs={"max_size_mb": 5000}, daemon=True).start()
        return root

    def switch_screen(self, screen_name: str):
        """Navigate to screen and push current screen to navigation stack."""
        if hasattr(self, "root") and self.root and hasattr(self.root, "ids") and "screen_manager" in self.root.ids:
            sm = self.root.ids.screen_manager
            if sm.current != screen_name:
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

    def go_back(self, target=None):
        """Unified back action for UI back buttons and Android hardware back key."""
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
        if self.player_controller.active_track:
            update_theme_from_image(self.player_controller.active_track.album_art)
            
        # Simulate asynchronous heavy operation (e.g., fetching from yt-dlp)
        from kivy.clock import Clock
        Clock.schedule_once(self.load_data_async, 0.05)
        Clock.schedule_once(lambda dt: self.load_search_history_from_db(), 0.1)
        
    def load_data_async(self, dt):
        try:
            library_screen = self.root.ids.screen_manager.get_screen("library")
            library_list = library_screen.ids.library_list
        except AttributeError:
            print("Warning: Screen manager or ids not ready yet.")
            return

        rv_data = []
        for track in self.playlist_model.tracks:
            rv_data.append({
                "title": track.title,
                "artist": track.artist,
                "artwork": track.album_art,
                "track_obj": track
            })
        library_list.data = rv_data

        # Populate Home Screen horizontal carousels with real library tracks
        self.populate_home_screen_data()

        # Automatically download album artwork for all tracks in library/catalog in background
        ensure_artworks_downloaded(self.playlist_model.tracks, on_track_updated=self.on_artwork_downloaded)

        # Populate carousel slightly deferred so frame 0 renders instantly without freezing
        from kivy.clock import Clock
        Clock.schedule_once(lambda d: self.ensure_player_carousel(), 0.1)

        # Scan device offline songs silently in background so 'Offline Songs' playlist is populated
        threading.Thread(target=lambda: self.scan_and_load_offline_songs(auto_play=False, show_screen=False), daemon=True).start()

        # If catalog is minimal/fresh, dynamically discover trending tracks
        if len(self.playlist_model.tracks) <= 3:
            app_logger.info("[THREAD START] MusicApp._fetch_trending_tracks")
            threading.Thread(target=self._fetch_trending_tracks, daemon=True).start()

    def on_artwork_downloaded(self, track, art_path):
        """Dispatched on main thread whenever a track's album art finishes downloading."""
        track.album_art = art_path
        # Re-populate Home cards with downloaded artwork
        self.populate_home_screen_data()
        # Re-populate Library list with downloaded artwork
        if hasattr(self, "root") and self.root:
            try:
                lib_screen = self.root.ids.screen_manager.get_screen("library")
                if "library_list" in lib_screen.ids:
                    lib_screen.ids.library_list.data = [{
                        "title": t.title,
                        "artist": t.artist,
                        "artwork": t.album_art,
                        "track_obj": t
                    } for t in self.playlist_model.tracks]
            except Exception:
                pass
        # Refresh Carousel if Now Playing initialized
        self.ensure_player_carousel(force_refresh=True)

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

            if "quick_picks_list" in home.ids:
                home.ids.quick_picks_list.data = [
                    {
                        "title": t.title,
                        "artist": t.artist,
                        "artwork": t.album_art,
                        "track_obj": t,
                        "text": t.title,
                    } for t in quick_picks_tracks
                ]
            if "trending_list" in home.ids:
                home.ids.trending_list.data = [
                    {
                        "title": t.title,
                        "artist": t.artist,
                        "artwork": t.album_art,
                        "track_obj": t,
                        "text": t.title,
                    } for t in reversed(tracks)
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
                    } for t in featured_tracks
                ]
        except Exception as e:
            app_logger.warning(f"populate_home_screen_data encountered non-fatal error: {e}")

    def _fetch_trending_tracks(self):
        """Dynamically pulls top trending music on a fresh install in the background."""
        try:
            info = fetch_youtube_metadata("ytsearch8:trending global top music hits", extract_flat=True)
            entries = info.get('entries', []) if info else []
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
            app_logger.info("[THREAD SUCCESS] MusicApp._fetch_trending_tracks completed")
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
            } for t in self.playlist_model.tracks]
        except Exception:
            pass
        self.populate_home_screen_data()
        self.ensure_player_carousel(force_refresh=True)
        # Ensure all newly fetched tracks have their artwork automatically downloaded
        ensure_artworks_downloaded(self.playlist_model.tracks, on_track_updated=self.on_artwork_downloaded)

    def ensure_player_carousel(self, force_refresh=False):
        """Populate the Now Playing album carousel if not already initialized or on update."""
        if getattr(self, "_player_carousel_initialized", False) and not force_refresh:
            return
        if not hasattr(self, "root") or not self.root or not hasattr(self.root, "ids") or "screen_manager" not in self.root.ids:
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
            for track in self.playlist_model.tracks:
                card = MDCard(
                    style="elevated",
                    radius=[dp(24)],
                    size_hint=(None, None),
                    size=(dp(280), dp(280)),
                    pos_hint={"center_x": .5, "center_y": .5},
                    ripple_behavior=True,
                    on_release=lambda *args: self.show_lyrics()
                )
                image = FitImage(source=track.album_art, radius=[dp(24)])
                card.add_widget(image)
                carousel.add_widget(card)
            self._player_carousel_initialized = True
        finally:
            self._updating_carousel = False

    def on_carousel_index(self, index):
        if index is None or getattr(self, "_updating_carousel", False):
            return
        if 0 <= index < len(self.playlist_model.tracks):
            track = self.playlist_model.tracks[index]
            if track != self.player_controller.active_track:
                self.play_selected_track(track)

    def play_selected_track(self, track):
        self.ensure_player_carousel()
        if track not in self.playlist_model.tracks:
            self.playlist_model.add_track(track)
        # If playing from active playlist, synchronize playback queue for continuous playback
        if hasattr(self, "active_playlist_tracks") and self.active_playlist_tracks and track in self.active_playlist_tracks:
            self.player_controller.set_custom_queue(self.active_playlist_tracks, start_track=track)
        self.player_controller.set_track(track)
        self.switch_screen("player")
        self.player_controller.play()
        
        # Sync Carousel
        try:
            player_screen = self.root.ids.screen_manager.get_screen("player")
            carousel = player_screen.ids.album_carousel
            if track in self.playlist_model.tracks:
                idx = self.playlist_model.tracks.index(track)
                if carousel.index != idx:
                    self._updating_carousel = True
                    try:
                        carousel.index = idx
                    finally:
                        self._updating_carousel = False
        except Exception:
            pass

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
        """Display Material Design 3 single-choice dialog to select audio streaming/download quality."""
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

    def open_playlist(self, playlist_name: str):
        """Switches to PlaylistScreen and populates it with real tracks for the selected playlist."""
        self.active_playlist_name = playlist_name
        self.switch_screen("playlist")
        self.sync_active_playlist_screen()

    def sync_active_playlist_screen(self):
        """Synchronizes PlaylistScreen with SQLite data for active_playlist_name."""
        if not hasattr(self, "root") or not self.root:
            return
        try:
            pl_screen = self.root.ids.screen_manager.get_screen("playlist")
            raw_tracks = get_playlist_tracks(self.active_playlist_name)
            
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
                pl_screen.ids.playlist_tracks_list.data = [{
                    "title": t.title,
                    "artist": t.artist,
                    "artwork": t.album_art,
                    "track_obj": t
                } for t in track_objs]

            if track_objs:
                ensure_artworks_downloaded(track_objs, on_track_updated=self.on_artwork_downloaded, cache_dir=self.cache_dir)
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
        """Bottom sheet allowing user to select tracks from library to add to active playlist."""
        if not self.active_playlist_name:
            return
        current_vids = {t.video_id for t in getattr(self, "active_playlist_tracks", [])}
        available_tracks = [t for t in self.playlist_model.tracks if t.video_id not in current_vids]

        if not available_tracks and self.active_playlist_name != "Offline Songs":
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
        scroll = MDScrollView(size_hint_y=None, height="330dp")
        dlist = MDList()

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

        for track in available_tracks:
            def on_add(inst, t=track):
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

            item = MDListItem(
                MDListItemLeadingAvatar(
                    source=track.album_art if track.album_art else "album_art.png",
                    radius=[dp(8), dp(8), dp(8), dp(8)],
                ),
                MDListItemHeadlineText(text=track.title),
                MDListItemSupportingText(text=track.artist),
                MDListItemTrailingIcon(icon="plus"),
                on_release=on_add
            )
            dlist.add_widget(item)

        scroll.add_widget(dlist)
        sheet.add_widget(scroll)
        Window.add_widget(sheet)
        sheet.width = Window.width
        sheet.x = 0
        sheet.set_state("open")

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

    def show_autoeq_profile_dialog(self):
        """Display single-choice dialog to choose an AutoEq profile."""
        profiles = ["Flat", "Bass Boost", "Vocal Booster", "Rock", "Electronic", "Classical", "Hip-Hop", "Acoustic"]
        list_container = MDList()
        for p in profiles:
            def on_sel(instance, prof=p):
                self.selected_eq_profile = prof
                if self.autoeq_dialog:
                    self.autoeq_dialog.dismiss()
            is_sel = (p == self.selected_eq_profile)
            item = MDListItem(
                MDListItemHeadlineText(text=p),
                on_release=on_sel,
            )
            if is_sel:
                item.add_widget(MDListItemTrailingIcon(icon="check"))
            list_container.add_widget(item)
            
        self.autoeq_dialog = MDDialog(
            MDDialogHeadlineText(text="Select AutoEq Profile"),
            MDDialogContentContainer(
                list_container,
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: self.autoeq_dialog.dismiss()),
            ),
        )
        self.autoeq_dialog.open()

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

    def open_album(self, album_name="Future Echoes"):
        """Populates AlbumScreen with real tracks from library."""
        self.switch_screen("album")
        if hasattr(self, "root") and self.root:
            try:
                screen = self.root.ids.screen_manager.get_screen("album")
                if "album_tracks_list" in screen.ids:
                    screen.ids.album_tracks_list.data = [{
                        "title": t.title,
                        "artist": t.artist,
                        "artwork": t.album_art,
                        "track_obj": t
                    } for t in self.playlist_model.tracks]
            except Exception as e:
                print(f"[open_album error]: {e}")

    def open_artist(self, artist_name="Synthwave Collective"):
        """Populates ArtistScreen with real tracks from library."""
        self.switch_screen("artist")
        if hasattr(self, "root") and self.root:
            try:
                screen = self.root.ids.screen_manager.get_screen("artist")
                if "artist_tracks_list" in screen.ids:
                    screen.ids.artist_tracks_list.data = [{
                        "title": t.title,
                        "artist": t.artist,
                        "artwork": t.album_art,
                        "track_obj": t
                    } for t in self.playlist_model.tracks]
            except Exception as e:
                print(f"[open_artist error]: {e}")

    def show_favorites(self):
        """Navigate to the dedicated Favorite Songs screen and sync with SQLite."""
        self.sync_favorites_screen()
        self.switch_screen("favorites")

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
            if fav_tracks:
                container.clear_widgets()
                track_objs = []
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
                # Automatically ensure artwork is downloaded for all favorite tracks
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
                from utils.local_audio_utils import scan_device_offline_songs
                from models.database import add_playlist, add_track_to_playlist
                add_playlist("Offline Songs")

                scanned = scan_device_offline_songs(cache_dir=self.cache_dir)
                loaded_tracks = []
                for meta in scanned:
                    add_track_to_playlist("Offline Songs", meta["video_id"], meta)
                    t = self.playlist_model.get_track_by_video_id(meta["video_id"])
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

                def _finish(dt):
                    count = len(scanned)
                    if show_screen:
                        self.show_toast(f"Loaded {count} offline songs into 'Offline Songs' playlist!")
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
                if "search_results_list" in search_screen.ids:
                    search_screen.ids.search_results_list.data = []
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

        # 1. Direct YouTube URL extraction check
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

        # 2. Local Library search (instant 0ms response)
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

    def _async_yt_search(self, query: str):
        try:
            info = fetch_youtube_metadata(f"ytsearch8:{query}", extract_flat=True)
            entries = info.get('entries', []) if info else []
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
                vid = entry.get("id", "")
                title = entry.get("title", "Unknown Title")
                artist = entry.get("uploader") or entry.get("channel") or "YouTube"
                dur = int(entry.get("duration", 0) or 180)
                thumb = get_thumbnail_path(vid) if vid else "album_art.png"
                track_obj = TrackModel(
                    video_id=vid,
                    title=title,
                    artist=artist,
                    url=f"https://www.youtube.com/watch?v={vid}" if vid else "",
                    duration=dur,
                    album_art=thumb
                )
                rv_data.append({
                    "title": title,
                    "artist": f"{artist} • {track_obj.formatted_duration}",
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
        """Displays real fetched lyrics with asynchronous background loading."""
        track = self.player_controller.active_track
        if not track:
            return

        from kivymd.uix.label import MDLabel
        from kivymd.uix.scrollview import MDScrollView
        from kivymd.uix.boxlayout import MDBoxLayout

        lyrics_sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text=f"Lyrics - {track.title[:20]}"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: lyrics_sheet.set_state("close"))
            ),
            size_hint_y=None,
            height="440dp"
        )
        scroll = MDScrollView(size_hint_y=None, height="370dp")
        box = MDBoxLayout(orientation="vertical", adaptive_height=True, padding=["20dp", "16dp", "20dp", "32dp"], spacing="12dp")
        
        title_lbl = MDLabel(
            text=f"{track.title}\n{track.artist}",
            font_style="Title",
            role="large",
            bold=True,
            adaptive_height=True,
            halign="center"
        )
        box.add_widget(title_lbl)

        current_lyrics = track.lyrics.strip() if track.lyrics else ""
        if not current_lyrics or "dummy lyrics" in current_lyrics.lower():
            body_text = "Fetching lyrics from LRCLIB..."
        else:
            body_text = current_lyrics

        lyrics_lbl = MDLabel(
            text=body_text,
            font_style="Body",
            role="large",
            adaptive_height=True,
            halign="center"
        )
        box.add_widget(lyrics_lbl)
        scroll.add_widget(box)
        lyrics_sheet.add_widget(scroll)
        Window.add_widget(lyrics_sheet)
        lyrics_sheet.width = Window.width
        lyrics_sheet.x = 0
        lyrics_sheet.set_state("open")

        if not current_lyrics or "dummy lyrics" in current_lyrics.lower():
            def on_fetched(lyrics_text):
                track.lyrics = lyrics_text
                lyrics_lbl.text = lyrics_text
            fetch_lyrics_async(track.title, track.artist, track.video_id, cache_dir=self.cache_dir, on_success=on_fetched)

    def show_queue_sheet(self):
        """Display YouTube Music style Up Next bottom sheet with playlist queue."""
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
            from kivymd.uix.scrollview import MDScrollView
            scroll = MDScrollView(size_hint_y=None, height="390dp")
            self.queue_list_widget = MDList()
            scroll.add_widget(self.queue_list_widget)
            self.queue_sheet.add_widget(scroll)
            Window.add_widget(self.queue_sheet)

        self.queue_sheet.width = Window.width
        self.queue_sheet.x = 0

        # Refresh queue list items with current playlist state
        if hasattr(self, "queue_list_widget"):
            self.queue_list_widget.clear_widgets()
            for track in self.playlist_model.tracks:
                is_active = (track == self.player_controller.active_track)
                icon_name = "volume-high" if is_active else "music"

                def on_select(instance, t=track):
                    self.play_selected_track(t)
                    self.queue_sheet.set_state("close")

                item = MDListItem(
                    MDListItemLeadingAvatar(
                        source=track.album_art if track.album_art else "album_art.png",
                        radius=[dp(8), dp(8), dp(8), dp(8)],
                    ),
                    MDListItemHeadlineText(
                        text=track.title,
                        bold=is_active,
                        theme_text_color="Custom" if is_active else "Primary",
                        text_color=self.theme_cls.primaryColor if is_active else self.theme_cls.onSurfaceColor,
                    ),
                    MDListItemSupportingText(
                        text=f"{track.artist} • {track.formatted_duration}",
                    ),
                    on_release=on_select,
                )
                self.queue_list_widget.add_widget(item)

        self.queue_sheet.set_state("open")

    def on_stop(self):
        """Clean up audio streams, threads, and background workers on application exit."""
        if hasattr(self, "player_controller") and self.player_controller:
            self.player_controller.stop()

if __name__ == '__main__':
    MusicApp().run()
