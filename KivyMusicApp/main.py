from kivy.config import Config
from kivy.utils import platform
if platform in ('win', 'macosx', 'linux'):
    Config.set('graphics', 'width', '360')
    Config.set('graphics', 'height', '640')
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'fullscreen', False)

import os
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import (
    MDDialog, 
    MDDialogHeadlineText, 
    MDDialogSupportingText, 
    MDDialogButtonContainer
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.bottomsheet import MDBottomSheet, MDBottomSheetDragHandle, MDBottomSheetDragHandleTitle, MDBottomSheetDragHandleButton
from kivymd.uix.list import MDList, MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText

from models.track_model import PlaylistModel
from controllers.player_controller import PlayerController
from views.screens import HomeScreen, SearchScreen, LibraryScreen, SettingsScreen, PlayerScreen
from views.components import TrackListItem
from utils.theme_utils import update_theme_from_image

class MusicApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=['.mp3', '.wav', '.flac']
        )
        self.dialog = None
        self.bottom_sheet = None
        
        # MVC Initialization
        self.playlist_model = PlaylistModel()
        self.player_controller = PlayerController()
        self.player_controller.set_playlist(self.playlist_model)
        
        # Set default track
        if self.playlist_model.tracks:
            self.player_controller.set_track(self.playlist_model.tracks[0])

    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.dynamic_color = True
        return Builder.load_file(os.path.join("views", "main.kv"))
        
    def on_start(self):
        if self.player_controller.active_track:
            update_theme_from_image(self.player_controller.active_track.album_art)
            
        # Simulate asynchronous heavy operation (e.g., fetching from yt-dlp)
        from kivy.clock import Clock
        Clock.schedule_once(self.load_data_async, 1.0)
        
    def load_data_async(self, dt):
        try:
            # Dynamically populate Library and Carousel safely
            library_screen = self.root.ids.screen_manager.get_screen("library")
            library_list = library_screen.ids.library_list
            player_screen = self.root.ids.screen_manager.get_screen("player")
            carousel = player_screen.ids.album_carousel
        except AttributeError:
            print("Warning: Screen manager or ids not ready yet.")
            return
        
        from kivymd.uix.carousel import MDCarouselItem
        from kivymd.uix.fitimage import FitImage
        from kivy.metrics import dp
        
        rv_data = []
        for track in self.playlist_model.tracks:
            # Add to library list (RecycleView data)
            rv_data.append({
                "title": track.title,
                "artist": track.artist,
                "track_obj": track
            })
            
            # Add to carousel
            card = MDCarouselItem(
                radius=[dp(16)]
            )
            image = FitImage(source=track.album_art, radius=[dp(16)])
            card.add_widget(image)
            carousel.add_widget(card)
            
        library_list.data = rv_data

    def on_carousel_index(self, index):
        if index >= 0 and index < len(self.playlist_model.tracks):
            track = self.playlist_model.tracks[index]
            if track != self.player_controller.active_track:
                self.play_selected_track(track)

    def play_selected_track(self, track):
        self.player_controller.set_track(track)
        self.root.ids.screen_manager.current = "player"
        self.player_controller.toggle_play()
        update_theme_from_image(track.album_art)
        
        # Sync Carousel
        player_screen = self.root.ids.screen_manager.get_screen("player")
        carousel = player_screen.ids.album_carousel
        if track in self.playlist_model.tracks:
            idx = self.playlist_model.tracks.index(track)
            if carousel.index != idx:
                carousel.index = idx

    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))

    def select_path(self, path):
        self.exit_manager()
        print(f"Selected file: {path}")

    def exit_manager(self, *args):
        self.file_manager.close()
        
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
                    MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: self.bottom_sheet.set_state("toggle"))
                ),
                MDList(
                    MDListItem(MDListItemLeadingIcon(icon="playlist-plus"), MDListItemHeadlineText(text="Add to Playlist"), on_release=lambda x: self.bottom_sheet.set_state("toggle")),
                    MDListItem(MDListItemLeadingIcon(icon="share-variant"), MDListItemHeadlineText(text="Share"), on_release=lambda x: self.bottom_sheet.set_state("toggle")),
                    MDListItem(MDListItemLeadingIcon(icon="delete"), MDListItemHeadlineText(text="Remove"), on_release=lambda x: self.bottom_sheet.set_state("toggle")),
                )
            )
            Window.add_widget(self.bottom_sheet)
        self.bottom_sheet.set_state("toggle")

    def show_lyrics(self):
        if not self.player_controller.active_track:
            return
            
        from kivymd.uix.label import MDLabel
        from kivymd.uix.scrollview import MDScrollView
        from kivymd.uix.boxlayout import MDBoxLayout
        
        lyrics_sheet = MDBottomSheet(
            MDBottomSheetDragHandle(
                MDBottomSheetDragHandleTitle(text="Lyrics"),
                MDBottomSheetDragHandleButton(icon="close", on_release=lambda x: lyrics_sheet.set_state("toggle"))
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
        lyrics_sheet.set_state("toggle")

if __name__ == '__main__':
    MusicApp().run()
