from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.core.text import LabelBase

# ------------------ ICON FONT ------------------

LabelBase.register(
    name="MaterialIcons",
    fn_regular="MaterialIcons-Regular.ttf"
)

# ------------------ THEME ------------------

LIGHT_THEME = {
    "bg": (0.96, 0.97, 0.99, 1),
    "surface": (1, 1, 1, 1),
    "surface_alt": (0.94, 0.95, 0.98, 1),
    "text_primary": (0.12, 0.14, 0.18, 1),
    "text_secondary": (0.35, 0.38, 0.45, 1),
    "icon": (0.10, 0.11, 0.13, 1),
    "accent": (0.35, 0.45, 0.95, 1),
}

# ------------------ ROOT LAYOUT ------------------

class RootLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        with self.canvas.before:
            Color(*LIGHT_THEME["bg"])
            self.bg = Rectangle()

        self.bind(size=self._update_bg, pos=self._update_bg)

        self.top_bar = TopBar()
        self.add_widget(self.top_bar)

        self.body = BoxLayout()
        self.add_widget(self.body)

        self.sidebar = Sidebar(self)
        self.main_area = MainArea()

        self.body.add_widget(self.sidebar)
        self.body.add_widget(self.main_area)

        self.player_bar = PlayerBar()
        self.add_widget(self.player_bar)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def navigate(self, view_name):
        self.main_area.show(view_name)

# ------------------ TOP BAR ------------------

class TopBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(
            size_hint_y=None,
            height=dp(56),
            padding=dp(16),
            **kwargs
        )

        with self.canvas.before:
            Color(*LIGHT_THEME["surface"])
            self.bg = Rectangle()

        self.bind(size=self._update_bg, pos=self._update_bg)

        self.search_label = Label(
            text="Search music, artists, albums…",
            color=LIGHT_THEME["text_secondary"],
            halign="left",
            valign="middle"
        )
        self.search_label.bind(size=self.search_label.setter("text_size"))
        self.add_widget(self.search_label)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

# ------------------ SIDEBAR ------------------

class Sidebar(BoxLayout):
    def __init__(self, root, **kwargs):
        super().__init__(
            orientation="vertical",
            size_hint_x=None,
            width=dp(220),
            padding=dp(12),
            spacing=dp(8),
            **kwargs
        )
        self.root = root

        with self.canvas.before:
            Color(*LIGHT_THEME["surface"])
            self.bg = Rectangle()

        self.bind(size=self._update_bg, pos=self._update_bg)

        for name in ("Library", "Search", "Playlists", "Downloads"):
            btn = Button(
                text=name,
                background_normal="",
                background_color=(0, 0, 0, 0),
                color=LIGHT_THEME["text_primary"],
                on_press=lambda _, n=name: self.root.navigate(n.lower())
            )
            self.add_widget(btn)

        self.add_widget(Widget())

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

# ------------------ MAIN AREA ------------------

class MainArea(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(padding=dp(24), **kwargs)

        self.views = {
            "library": LibraryView(),
            "search": SearchView(),
            "playlists": PlaylistsView(),
            "downloads": DownloadsView(),
        }

        self.show("library")

    def show(self, name):
        self.clear_widgets()
        self.add_widget(self.views[name])

# ------------------ VIEWS ------------------

class LibraryView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(12), **kwargs)

        title = Label(
            text="Library",
            font_size="24sp",
            bold=True,
            color=LIGHT_THEME["text_primary"],
            size_hint_y=None,
            height=dp(40),
            halign="left",
            valign="middle"
        )
        title.bind(size=title.setter("text_size"))
        self.add_widget(title)

        for song, artist in (
            ("Midnight City", "M83"),
            ("Nightcall", "Kavinsky"),
            ("Digital Love", "Daft Punk"),
        ):
            self.add_widget(LibraryRow(song, artist))

        self.add_widget(Widget())

class SearchView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(16), **kwargs)

        title = Label(
            text="Search",
            font_size="24sp",
            bold=True,
            color=LIGHT_THEME["text_primary"]
        )
        self.add_widget(title)
        self.add_widget(Widget())

class PlaylistsView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(12), **kwargs)

        title = Label(
            text="Playlists",
            font_size="24sp",
            bold=True,
            color=LIGHT_THEME["text_primary"]
        )
        self.add_widget(title)

        for name in ("Favorites", "Late Night", "Workout"):
            self.add_widget(
                Label(text=name, font_size="16sp", color=LIGHT_THEME["text_secondary"])
            )

        self.add_widget(Widget())

class DownloadsView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.add_widget(Label(text="Offline Downloads"))

# ------------------ LIBRARY ROW ------------------

class LibraryRow(BoxLayout):
    def __init__(self, title, artist, **kwargs):
        super().__init__(
            size_hint_y=None,
            height=dp(64),
            padding=dp(12),
            spacing=dp(8),
            **kwargs
        )

        with self.canvas.before:
            Color(*LIGHT_THEME["surface_alt"])
            self.bg = RoundedRectangle(radius=[16])

        self.bind(size=self._update_bg, pos=self._update_bg)

        text_box = BoxLayout(orientation="vertical")
        text_box.add_widget(Label(text=title, bold=True))
        text_box.add_widget(Label(text=artist, font_size="12sp", opacity=0.6))
        self.add_widget(text_box)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

# ------------------ PLAYER BAR ------------------

class PlayerBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(
            size_hint_y=None,
            height=dp(96),
            padding=dp(16),
            spacing=dp(16),
            **kwargs
        )

        with self.canvas.before:
            Color(*LIGHT_THEME["surface"])
            self.bg = Rectangle()

        self.bind(size=self._update_bg, pos=self._update_bg)

        self.add_widget(Button(text="\ue045", font_name='MaterialIcons', font_size = "22sp"))
        self.add_widget(Button(text="\ue037", font_name='MaterialIcons', font_size = "22sp"))
        self.add_widget(Button(text="\ue044", font_name='MaterialIcons', font_size = "22sp"))

        self.timeline = Slider(min=0, max=100)
        self.add_widget(self.timeline)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

# ------------------ APP ------------------

class MusicPlayerApp(App):
    def build(self):
        return RootLayout()

if __name__ == "__main__":
    MusicPlayerApp().run()
