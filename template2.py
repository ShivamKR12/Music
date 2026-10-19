from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty


# -------------------------
# ROOT LAYOUT
# -------------------------
class RootLayout(BoxLayout):
    screen_manager = ObjectProperty(None)
    mini_player = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.screen_manager = ScreenManager()
        self.add_widget(self.screen_manager)

        self.mini_player = MiniPlayerBar(self)
        self.add_widget(self.mini_player)

        self.bottom_nav = BottomNavBar(self)
        self.add_widget(self.bottom_nav)

    def go_to(self, screen_name):
        self.screen_manager.current = screen_name

        if screen_name == "now_playing":
            self.mini_player.height = 0
            self.mini_player.opacity = 0
        else:
            self.mini_player.height = 60
            self.mini_player.opacity = 1


# -------------------------
# BOTTOM NAV BAR
# -------------------------
class BottomNavBar(BoxLayout):
    def __init__(self, root, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=60, **kwargs)
        self.root = root

        self.add_widget(Button(text="Home", on_press=lambda x: root.go_to("browse")))
        self.add_widget(Button(text="Search", on_press=lambda x: root.go_to("search")))
        self.add_widget(Button(text="Offline", on_press=lambda x: root.go_to("library")))
        self.add_widget(Button(text="Profile", on_press=lambda x: root.go_to("settings")))


# -------------------------
# MINI PLAYER
# -------------------------
class MiniPlayerBar(BoxLayout):
    def __init__(self, root, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=60, padding=10, spacing=10, **kwargs)
        self.root = root
        self.add_widget(Label(text="Song Title - Artist"))
        self.add_widget(Button(text="play/pause", size_hint_x=None, width=80, on_press=self.play_pause))
        self.add_widget(Button(text="Open", size_hint_x=None, width=80, on_press=lambda x: root.go_to("now_playing")))

    def play_pause(self, *args, **kwargs):
        pass

    def open(self, *args, **kwargs):
        pass


# -------------------------
# SCREENS
# -------------------------
class BrowseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Browse / Home"))


class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Search"))


class LibraryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)
        layout.add_widget(Label(text="Offline Library", size_hint_y=None, height=40))
        layout.add_widget(Button(text="Albums", on_press=self.albums))
        layout.add_widget(Button(text="Artists", on_press=self.artists))
        layout.add_widget(Button(text="Playlists", on_press=self.playlists))
        layout.add_widget(Button(text="Downloads", on_press=self.downloads))
        self.add_widget(layout)
    
    def albums(self, *args, **kwargs):
        pass

    def artists(self, *args, **kwargs):
        pass

    def playlists(self, *args, **kwargs):
        pass

    def downloads(self, *args, **kwargs):
        pass


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Profile / Settings"))


class NowPlayingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main = BoxLayout(orientation="vertical", padding=20, spacing=20)
        main.add_widget(Label(text="Now Playing", size_hint_y=None, height=40))
        controls = BoxLayout(orientation="horizontal", size_hint_y=None, height=60, spacing=10)
        controls.add_widget(Button(text="Previous", on_press=self.previous))
        controls.add_widget(Button(text="Play/Pause", on_press=self.play_pause))
        controls.add_widget(Button(text="Next", on_press=self.next))
        main.add_widget(controls)
        main.add_widget(Button(text="Lyrics", size_hint_y=None, height=50, on_press=self.lyrics))
        self.add_widget(main)
    
    def play_pause(self, *args, **kwargs):
        pass

    def next(self, *args, **kwargs):
        pass

    def previous(self, *args, **kwargs):
        pass

    def lyrics(self, *args, **kwargs):
        pass


# -------------------------
# APP
# -------------------------
class MusicPlayerApp(App):
    def build(self):
        root = RootLayout()

        root.screen_manager.add_widget(BrowseScreen(name="browse"))
        root.screen_manager.add_widget(SearchScreen(name="search"))
        root.screen_manager.add_widget(LibraryScreen(name="library"))
        root.screen_manager.add_widget(SettingsScreen(name="settings"))
        root.screen_manager.add_widget(NowPlayingScreen(name="now_playing"))

        root.go_to("browse")
        return root


if __name__ == "__main__":
    MusicPlayerApp().run()
