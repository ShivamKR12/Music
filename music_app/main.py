import os
import logger # Activates logging, stdout redirection, and crash hooks instantly

import config  # MUST BE IMPORTED FIRST to apply Config.set before Kivy initializes Window

from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.loader import Loader

Loader.loading_image = os.path.join(os.path.dirname(__file__), 'blank.png')
from ui.root import RootLayout
from ui.screens.playlists import PlaylistsScreen
from ui.screens.search import SearchScreen
from ui.screens.library import LibraryScreen
from ui.screens.now_playing import NowPlayingScreen
from ui.screens.playlist_detail import PlaylistDetailScreen

from models.database import init_db

class MusicPlayerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Light"
        init_db()
        root = RootLayout()
        self.root = root
        root.screen_manager.add_widget(LibraryScreen(name="library"))
        root.screen_manager.add_widget(PlaylistsScreen(name="playlists"))
        root.screen_manager.add_widget(PlaylistDetailScreen(name="playlist_detail"))
        root.screen_manager.add_widget(SearchScreen(name="search"))
        root.screen_manager.add_widget(NowPlayingScreen(name="now_playing"))
        
        # Dynamically set initial boot location based on database state:
        initial_screen = "library" 
        if (root.queue_index is not None and root.queue_index > 0) or root.is_playing:
            initial_screen = "now_playing"
            
        root.go_to(initial_screen)

        from kivy.core.window import Window
        Window.bind(on_keyboard=self.on_keyboard)

        return root

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if key == 27:  # 27 is the Escape key, mapped to Android Back Button
            if self.root.screen_manager.current == "now_playing":
                self.root.go_to("library")
                return True # Prevent app exit
            elif self.root.screen_manager.current != "library":
                self.root.go_to("library")
                return True
            return False # Allow exit if already on library

    def on_stop(self):
        # Gracefully shutdown any running threads and C-level player objects
        if hasattr(self, 'root') and self.root:
            if hasattr(self.root, 'audio') and self.root.audio:
                # Set the event to abort any ongoing yt-dlp downloads immediately
                self.root.audio.cancel_event.set()
                # Stop and unload ffpyplayer stream handles to prevent segfaults
                self.root.audio.cleanup_player()

if __name__ == '__main__':
    MusicPlayerApp().run()
