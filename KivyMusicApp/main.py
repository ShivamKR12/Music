from kivy.config import Config
from kivy.utils import platform
if platform in ('win', 'macosx', 'linux'):
    Config.set('graphics', 'width', '360')
    Config.set('graphics', 'height', '640')
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'fullscreen', False)

import os
from kivy.lang import Builder
from kivy.properties import StringProperty
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
from kivymd.uix.bottomsheet import MDBottomSheet, MDBottomSheetDragHandle, MDBottomSheetDragHandleTitle, MDBottomSheetDragHandleButton
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem, MDNavigationItemIcon, MDNavigationItemLabel
from kivymd.uix.list import (
    MDList, 
    MDListItem, 
    MDListItemLeadingIcon, 
    MDListItemHeadlineText,
    MDListItemSupportingText,
    MDListItemTrailingIcon
)

from models.track_model import PlaylistModel
from controllers.player_controller import PlayerController
from views.screens import HomeScreen, SearchScreen, LibraryScreen, SettingsScreen, PlayerScreen, FavoritesScreen
from views.components import (
    TrackListItem,
    DirectionalHorizontalScrollView,
    DirectionalHorizontalRecycleView,
)
from utils.theme_utils import update_theme_from_image

class MusicApp(MDApp):
    selected_audio_quality = StringProperty("High (320kbps)")
    selected_eq_profile = StringProperty("Flat")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        return root

    def switch_screen(self, screen_name: str):
        """Navigate to screen and push current screen to navigation stack."""
        if hasattr(self, "root") and self.root and hasattr(self.root, "ids") and "screen_manager" in self.root.ids:
            sm = self.root.ids.screen_manager
            if sm.current != screen_name:
                self.screen_history.append(sm.current)
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
                "track_obj": track
            })
        library_list.data = rv_data

        # Populate carousel slightly deferred so frame 0 renders instantly without freezing
        from kivy.clock import Clock
        Clock.schedule_once(lambda d: self.ensure_player_carousel(), 0.1)

    def ensure_player_carousel(self):
        """Populate the Now Playing album carousel if not already initialized."""
        if getattr(self, "_player_carousel_initialized", False):
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

    def on_carousel_index(self, index):
        if index >= 0 and index < len(self.playlist_model.tracks):
            track = self.playlist_model.tracks[index]
            if track != self.player_controller.active_track:
                self.play_selected_track(track)

    def play_selected_track(self, track):
        self.ensure_player_carousel()
        self.player_controller.set_track(track)
        self.switch_screen("player")
        self.player_controller.toggle_play()
        
        # Sync Carousel
        player_screen = self.root.ids.screen_manager.get_screen("player")
        carousel = player_screen.ids.album_carousel
        if track in self.playlist_model.tracks:
            idx = self.playlist_model.tracks.index(track)
            if carousel.index != idx:
                carousel.index = idx

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
        print(f"Selected file: {path}")

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

    def show_add_playlist_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                MDDialogHeadlineText(text="New Playlist"),
                MDDialogSupportingText(text="Do you want to create a new playlist?"),
                MDDialogButtonContainer(
                    MDButton(MDButtonText(text="CANCEL"), style="text", on_release=lambda x: self.dialog.dismiss()),
                    MDButton(MDButtonText(text="CREATE"), style="text", on_release=lambda x: self.dialog.dismiss()),
                ),
            )
        self.dialog.open()
        
    def show_track_options(self):
        if not self.bottom_sheet:
            self.bottom_sheet = MDBottomSheet(
                MDBottomSheetDragHandle(
                    MDBottomSheetDragHandleTitle(text="Track Options"),
                    MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: self.bottom_sheet.set_state("close"))
                ),
                MDList(
                    MDListItem(
                        MDListItemLeadingIcon(icon="playlist-plus"), 
                        MDListItemHeadlineText(text="Add to Playlist"), 
                        on_release=lambda x: (self.bottom_sheet.set_state("close"), self.show_add_playlist_dialog())
                    ),
                    MDListItem(
                        MDListItemLeadingIcon(icon="text-box-outline"), 
                        MDListItemHeadlineText(text="View Lyrics"), 
                        on_release=lambda x: (self.bottom_sheet.set_state("close"), self.show_lyrics())
                    ),
                    MDListItem(
                        MDListItemLeadingIcon(icon="share-variant"), 
                        MDListItemHeadlineText(text="Share"), 
                        on_release=lambda x: self.bottom_sheet.set_state("close")
                    ),
                    MDListItem(
                        MDListItemLeadingIcon(icon="delete"), 
                        MDListItemHeadlineText(text="Remove"), 
                        on_release=lambda x: self.bottom_sheet.set_state("close")
                    ),
                ),
                size_hint_y=None,
                height="340dp",
            )
            Window.add_widget(self.bottom_sheet)
        self.bottom_sheet.width = Window.width
        self.bottom_sheet.x = 0
        self.bottom_sheet.set_state("open")

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
        mapping = {
            "Playlists": "playlist",
            "Albums": "album",
            "Artists": "artist",
        }
        if filter_name in mapping:
            self.switch_screen(mapping[filter_name])

    def show_favorites(self):
        """Navigate to the dedicated Favorite Songs screen."""
        self.switch_screen("favorites")

    def show_downloaded(self):
        """Open file manager or filter downloaded items."""
        self.file_manager_open()

    def perform_search(self, query: str):
        """Execute search query and prepend to search history."""
        if not query or not str(query).strip():
            return
        q = str(query).strip()
        search_screen = self.root.ids.screen_manager.get_screen("search")
        if "search_input" in search_screen.ids:
            search_screen.ids.search_input.text = q
        if "search_history_list" in search_screen.ids:
            rv = search_screen.ids.search_history_list
            existing = [item["text"].lower() for item in rv.data]
            if q.lower() not in existing:
                rv.data.insert(0, {"text": q})

    def show_lyrics(self):
        if not self.player_controller.active_track:
            return
            
        from kivymd.uix.label import MDLabel
        from kivymd.uix.scrollview import MDScrollView
        from kivymd.uix.boxlayout import MDBoxLayout
        
        lyrics_sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text="Lyrics"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: lyrics_sheet.set_state("close"))
            ),
        )
        
        scroll = MDScrollView(size_hint_y=None, height="300dp")
        box = MDBoxLayout(orientation="vertical", adaptive_height=True, padding="24dp")
        label = MDLabel(
            text=self.player_controller.active_track.lyrics,
            font_style="Headline",
            role="small",
            adaptive_height=True,
            halign="center"
        )
        box.add_widget(label)
        scroll.add_widget(box)
        lyrics_sheet.add_widget(scroll)
        
        Window.add_widget(lyrics_sheet)
        lyrics_sheet.width = Window.width
        lyrics_sheet.x = 0
        lyrics_sheet.set_state("open")

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
                    MDListItemLeadingIcon(
                        icon=icon_name,
                        theme_icon_color="Custom" if is_active else "Primary",
                        icon_color=self.theme_cls.primaryColor if is_active else self.theme_cls.onSurfaceVariantColor,
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

if __name__ == '__main__':
    MusicApp().run()
