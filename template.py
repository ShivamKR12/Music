from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


# -------------------------
# Base Screen with helpers
# -------------------------
class BaseScreen(Screen):
    def placeholder_action(self, *args):
        # Placeholder logic – does nothing safely
        pass

    def go_to(self, screen_name):
        if self.manager:
            self.manager.current = screen_name


# -------------------------
# Core Player Screens
# -------------------------
class NowPlayingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        layout.add_widget(Label(text="Now Playing"))
        layout.add_widget(Button(text="Play / Pause", on_press=self.placeholder_action))
        layout.add_widget(Button(text="Next", on_press=self.placeholder_action))
        layout.add_widget(Button(text="Previous", on_press=self.placeholder_action))
        layout.add_widget(Button(text="Lyrics", on_press=lambda x: self.go_to("lyrics")))

        self.add_widget(layout)


class MiniPlayerScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout()

        layout.add_widget(Label(text="Mini Player"))
        layout.add_widget(Button(text="Play", on_press=self.placeholder_action))

        self.add_widget(layout)


# -------------------------
# Library & Browsing
# -------------------------
class LibraryScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        layout.add_widget(Button(text="Albums", on_press=lambda x: self.go_to("album")))
        layout.add_widget(Button(text="Artists", on_press=lambda x: self.go_to("artist")))
        layout.add_widget(Button(text="Playlists", on_press=lambda x: self.go_to("playlist")))
        layout.add_widget(Button(text="Downloads", on_press=lambda x: self.go_to("downloads")))

        self.add_widget(layout)


class BrowseScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Browse / Discover"))
        self.add_widget(layout)


class SearchScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Search"))
        self.add_widget(layout)


# -------------------------
# Content Detail Screens
# -------------------------
class AlbumScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Album View"))
        self.add_widget(layout)


class ArtistScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Artist View"))
        self.add_widget(layout)


class PlaylistScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Playlist View"))
        self.add_widget(layout)


class QueueScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Up Next / Queue"))
        self.add_widget(layout)


# -------------------------
# Supporting & Advanced
# -------------------------
class LyricsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout()
        layout.add_widget(Label(text="Lyrics View"))
        self.add_widget(layout)


class EqualizerScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout()
        layout.add_widget(Label(text="Equalizer / Audio Settings"))
        self.add_widget(layout)


class DownloadManagerScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout()
        layout.add_widget(Label(text="Download Manager"))
        self.add_widget(layout)


class DevicesScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout()
        layout.add_widget(Label(text="Devices / Connect"))
        self.add_widget(layout)


# -------------------------
# User & System
# -------------------------
class ProfileScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout()
        layout.add_widget(Label(text="Profile"))
        self.add_widget(layout)


class SettingsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout()
        layout.add_widget(Label(text="Settings"))
        self.add_widget(layout)


class OnboardingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Welcome / Paywall"))
        layout.add_widget(Button(text="Continue", on_press=self.placeholder_action))
        self.add_widget(layout)


# -------------------------
# App
# -------------------------
class MusicPlayerApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(OnboardingScreen(name="onboarding"))
        sm.add_widget(NowPlayingScreen(name="now_playing"))
        sm.add_widget(MiniPlayerScreen(name="mini_player"))
        sm.add_widget(LibraryScreen(name="library"))
        sm.add_widget(BrowseScreen(name="browse"))
        sm.add_widget(SearchScreen(name="search"))

        sm.add_widget(AlbumScreen(name="album"))
        sm.add_widget(ArtistScreen(name="artist"))
        sm.add_widget(PlaylistScreen(name="playlist"))
        sm.add_widget(QueueScreen(name="queue"))

        sm.add_widget(LyricsScreen(name="lyrics"))
        sm.add_widget(EqualizerScreen(name="equalizer"))
        sm.add_widget(DownloadManagerScreen(name="downloads"))
        sm.add_widget(DevicesScreen(name="devices"))

        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(SettingsScreen(name="settings"))

        sm.current = "browse"
        return sm


if __name__ == "__main__":
    MusicPlayerApp().run()
