from kivy.config import Config
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '720')
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput

LabelBase.register(name="MaterialIcons", fn_regular="MaterialIcons-Regular.ttf")

LIGHT_THEME = {
    "bg": (0.98, 0.97, 0.94, 1),          # warm cream
    "surface": (0.95, 0.97, 1.0, 1),      # light blue
    "surface_alt": (1.0, 0.96, 0.96, 1),  # light red tint

    "text_primary": (0.12, 0.14, 0.18, 1),
    "text_secondary": (0.40, 0.42, 0.48, 1),

    "icon": (0.18, 0.20, 0.26, 1),

    "accent": (0.95, 0.55, 0.25, 1),      # warm orange
    "accent_soft": (1.0, 0.85, 0.70, 1),  # peach
}

class RootLayout(BoxLayout):
    screen_manager = ObjectProperty(None)
    mini_player = ObjectProperty(None)
    current_title = ObjectProperty(None)
    current_artist = ObjectProperty(None)

    is_playing = False
    shuffle_enabled = False
    repeat_mode = "off"    # "off" | "all" | "one"

    def __init__(self, **kwargs):
        super().__init__(orientation = "vertical", **kwargs)
        with self.canvas.before:
            Color(*LIGHT_THEME["bg"])
            self.bg = Rectangle()
        self.bind(pos=self._update_bg, size=self._update_bg)
        self.screen_manager = ScreenManager(transition = SlideTransition(direction = "up", duration = 0.35))
        self.add_widget(self.screen_manager)
        self.mini_player_wrapper = BoxLayout(size_hint_y = None, height = dp(64), padding = [dp(16), 0])
        self.mini_player = MiniPlayerBar(self)
        self.mini_player_wrapper.add_widget(self.mini_player)
        self.add_widget(self.mini_player_wrapper)
        self.nav_spacer = Widget(size_hint_y = None, height = dp(12))
        self.add_widget(self.nav_spacer)
        self.bottom_nav_wrapper = BoxLayout(size_hint_y = None, height = dp(64), padding = [dp(16), 0])
        self.bottom_nav = BottomNavBar(self)
        self.bottom_nav_wrapper.add_widget(self.bottom_nav)
        self.add_widget(self.bottom_nav_wrapper)
        self.songs = [
            ("Midnight City", "M83"),
            ("Nightcall", "Kavinsky"),
            ("Digital Love", "Daft Punk")
        ]
        self.current_index = 0

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def go_to(self, screen_name):
        hide = (screen_name == "now_playing")
        for w, h in [(self.mini_player_wrapper, dp(64)), (self.nav_spacer, dp(12)), (self.bottom_nav_wrapper, dp(64))]:
            w.disabled = hide
            Animation(opacity = 0 if hide else 1, height = 0 if hide else h, duration = 0.18).start(w)
        self.screen_manager.current = screen_name

    def toggle_play(self):
        self.is_playing = not self.is_playing
        now = self.screen_manager.get_screen("now_playing")
        self.mini_player.update_play_state(self.is_playing)
        now.update_play_state(self.is_playing)
        if self.is_playing:
            now.resume_timeline()
        else:
            now.pause_timeline()

    def toggle_shuffle(self):
        self.shuffle_enabled = not self.shuffle_enabled
        self.screen_manager.get_screen("now_playing").update_shuffle_state(self.shuffle_enabled)

    def toggle_repeat(self):
        if self.repeat_mode == "off":
            self.repeat_mode = "all"
        elif self.repeat_mode == "all":
            self.repeat_mode = "one"
        else:
            self.repeat_mode = "off"
        self.screen_manager.get_screen("now_playing").update_repeat_state(self.repeat_mode)

    def next_song(self):
        self.play_song_at(self.get_next_index())

    def previous_song(self):
        self.play_song_at(self.get_previous_index())

    def play_song_at(self, index):
        self.current_index = index
        title, artist = self.songs[self.current_index]
        self.current_title = title
        self.current_artist = artist
        now = self.screen_manager.get_screen("now_playing")
        # RESET TIMELINE HERE
        now.timeline_progress = 0
        now.timeline_running = False
        Animation.cancel_all(now.track_fill)
        now.track_fill.size = (0, now.timeline.height)
        self.mini_player.update_song(title, artist)
        now.animate_song_change(title, artist)
        if self.is_playing:
            now.start_timeline()

    def get_next_index(self):
        if self.repeat_mode == "one":
            return self.current_index
        if self.shuffle_enabled:
            import random
            if len(self.songs) == 1:
                return self.current_index
            choices = list(range(len(self.songs)))
            choices.remove(self.current_index)
            return random.choice(choices)
        next_index = self.current_index + 1
        if next_index >= len(self.songs):
            return 0 if self.repeat_mode == "all" else self.current_index
        return next_index

    def get_previous_index(self):
        if self.repeat_mode == "one":
            return self.current_index
        if self.shuffle_enabled:
            import random
            if len(self.songs) == 1:
                return self.current_index
            choices = list(range(len(self.songs)))
            choices.remove(self.current_index)
            return random.choice(choices)
        prev_index = self.current_index - 1
        if prev_index < 0:
            return len(self.songs) - 1 if self.repeat_mode == "all" else self.current_index
        return prev_index


class AnimatedBackground(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.c1 = Color(*LIGHT_THEME["bg"])
            self.r1 = Rectangle()
            self.c2 = Color(*LIGHT_THEME["accent_soft"][:3], 0.35)
            self.r2 = Rectangle()

        self.bind(pos=self._update, size=self._update)
        Clock.schedule_interval(self.animate, 0.03)

    def _update(self, *args):
        self.r1.pos = self.pos
        self.r1.size = self.size
        self.r2.pos = (self.x, self.y - self.height * 0.2)
        self.r2.size = self.size

    def animate(self, dt):
        self.c1.h += 0.0008
        self.c2.h += 0.001


class ArtworkIcon(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(220), dp(220))

        with self.canvas.before:
            Color(*LIGHT_THEME["accent_soft"])
            self.bg = RoundedRectangle(radius=[dp(24)])

        self.icon = Label(
            text="\ue405",
            font_name="MaterialIcons",
            font_size="96sp",
            color=LIGHT_THEME["icon"],
            center=self.center
        )
        self.add_widget(self.icon)

        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.icon.center = self.center


class BottomNavBar(BoxLayout):
    def __init__(self, root, **kwargs):
        super().__init__(orientation = "horizontal", size_hint_y = None, height = dp(64), padding = [dp(16), dp(8)], spacing = dp(32), **kwargs)
        self.root = root
        with self.canvas.before:
            Color(*LIGHT_THEME["surface"])
            self.bg = Rectangle()
        self.bind(pos = self._update_bg, size = self._update_bg)
        self.add_nav_btn("\ue88a", "library")
        self.add_nav_btn("\ue8b6", "search")
        self.add_nav_btn("\ue03b", "playlists")

    def _update_bg(self, *args):
        self.bg.pos, self.bg.size = self.pos, self.size

    def add_nav_btn(self, icon, screen):
        self.add_widget(Button(text = icon, font_name = "MaterialIcons", font_size = "26sp", color=LIGHT_THEME["icon"], background_normal = "", background_color = (0, 0, 0, 0), on_press = lambda x: self.root.go_to(screen)))


class MiniPlayerBar(BoxLayout):
    def __init__(self, root, **kwargs):
        super().__init__(orientation = "horizontal", size_hint_y = None, height = dp(72), padding = dp(12), spacing = dp(8), **kwargs)
        self.root = root
        with self.canvas.before:
            self.bg_color = Color(*LIGHT_THEME["surface"])
            self.bg = RoundedRectangle(radius = [20])
        self.bind(pos = self._update_bg, size = self._update_bg)
        self.art_icon = Label(text="\ue405", font_name="MaterialIcons", font_size="28sp", size_hint=(None, None), size=(dp(40), dp(40)), color=LIGHT_THEME["icon"])
        text_box = BoxLayout(orientation="vertical", spacing=dp(4), size_hint_x=1)
        self.title_label = Label(text="Midnight City", font_size="14sp", color=LIGHT_THEME["text_primary"], halign="left", valign="middle", bold=True, size_hint_y=None, height=dp(20))
        self.title_label.bind(size=self.title_label.setter("text_size"))
        self.artist_label = Label(text="M83", font_size="12sp", color=LIGHT_THEME["text_secondary"], halign="left", valign="middle", size_hint_y=None, height=dp(20))
        self.artist_label.bind(size=self.artist_label.setter("text_size"))
        text_box.add_widget(self.title_label)
        text_box.add_widget(self.artist_label)
        self.play_btn = Button(text = "\ue037", font_name = "MaterialIcons", font_size = "26sp", color=LIGHT_THEME["icon"], size_hint = (None, None), size = (dp(48), dp(48)), background_normal = "", background_color = (0, 0, 0, 0))
        with self.play_btn.canvas.before:
            Color(*LIGHT_THEME["accent"])
            self.play_bg = RoundedRectangle(radius = [22])
        self.play_btn.bind(pos = self._update_play, size = self._update_play, on_press = lambda *_: self.root.toggle_play())
        self.add_widget(self.art_icon)
        self.add_widget(text_box)
        self.add_widget(self.play_btn)

    def _update_bg(self, *args):
        self.bg.pos, self.bg.size = self.pos, self.size

    def _update_play(self, *args):
        self.play_bg.pos, self.play_bg.size = self.play_btn.pos, self.play_btn.size

    def update_play_state(self, is_playing):
        self.play_btn.text = "\ue034" if is_playing else "\ue037"
        self.animate_play()

    def animate_play(self, *args):
        (Animation(size = (dp(48), dp(48)), duration = 0.08) + Animation(size = (dp(44), dp(44)), duration = 0.08)).start(self.play_btn)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        Animation(rgba = LIGHT_THEME["surface_alt"], duration = 0.05).start(self.bg_color)
        self.root.go_to("now_playing")
        return True

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            Animation(rgba = LIGHT_THEME["surface"], duration = 0.05).start(self.bg_color)
        return super().on_touch_up(touch)

    def update_song(self, title, artist):
        self.title_label.text = title
        self.artist_label.text = artist


class PlaylistsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation = "vertical", padding = dp(24), spacing = dp(16))
        title = Label(text = "Playlists", font_size = "24sp", color=LIGHT_THEME["icon"], bold = True, size_hint_y = None, height = dp(40), halign = "left", valign = "middle")
        title.bind(size = title.setter("text_size"))
        root.add_widget(title)
        for name in ["Favorites", "Late Night", "Workout"]:
            card = BoxLayout(size_hint_y = None, height = dp(64), padding = [dp(16), dp(12)])
            with card.canvas.before:
                Color(*LIGHT_THEME["surface"])
                bg = RoundedRectangle(radius = [16])
            card.bind(pos = lambda w, *x, bg = bg: setattr(bg, "pos", w.pos), size = lambda w, *x, bg = bg: setattr(bg, "size", w.size))
            label = Label(text = name, font_size = "16sp", color=LIGHT_THEME["icon"], bold = True, halign = "left", valign = "middle")
            label.bind(size = label.setter("text_size"))
            card.add_widget(label)
            root.add_widget(card)
        root.add_widget(Widget())
        self.add_widget(root)


class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_state = "idle"

        root = BoxLayout(orientation="vertical", padding=dp(24), spacing=dp(16))

        # ---------- Title ----------
        title = Label(text="Search", font_size="24sp", color=LIGHT_THEME["text_primary"], bold=True, size_hint_y=None, height=dp(40), halign="left", valign="middle")
        title.bind(size=title.setter("text_size"))
        root.add_widget(title)

        # ---------- Search Bar ----------
        search_bar = BoxLayout(size_hint_y=None, height=dp(48), padding=[dp(16), 0])

        with search_bar.canvas.before:
            Color(*LIGHT_THEME["surface"])
            self.search_bg = RoundedRectangle(radius=[16])

        search_bar.bind(pos=lambda *_: setattr(self.search_bg, "pos", search_bar.pos), size=lambda *_: setattr(self.search_bg, "size", search_bar.size))

        self.search_input = TextInput(hint_text="Search songs, artists, albums…", multiline=False, background_color=(0, 0, 0, 0), foreground_color=LIGHT_THEME["text_primary"], cursor_color=LIGHT_THEME["accent"])

        self.search_input.bind(text=self.on_search_text)
        search_bar.add_widget(self.search_input)
        root.add_widget(search_bar)

        # ---------- State Container ----------
        self.state_container = BoxLayout()
        root.add_widget(self.state_container)

        # ---------- State Views ----------
        self.idle_view = Label(text="Search for songs, artists, or albums", opacity=0.5, halign="center", valign="middle")
        self.idle_view.bind(size=self.idle_view.setter("text_size"))

        self.typing_view = Label(text="Searching…", opacity=0.6)

        self.empty_view = Label(text="No results found", opacity=0.6)

        self.results_view = BoxLayout(orientation="vertical", spacing=dp(12), size_hint_y=None)
        self.results_view.bind(minimum_height=self.results_view.setter("height"))

        self.add_widget(root)

        self.set_state("idle")

    def set_state(self, state):
        if self.search_state == state:
            return

        self.search_state = state
        self.state_container.clear_widgets()

        view = {
            "idle": self.idle_view,
            "typing": self.typing_view,
            "empty": self.empty_view,
            "results": self.results_view
        }[state]

        view.opacity = 0
        self.state_container.add_widget(view)
        Animation(opacity=1, duration=0.2).start(view)

    def on_search_text(self, instance, text):
        text = text.strip()

        if not text:
            self.set_state("idle")
            return

        self.set_state("typing")

        # Fake dataset (UI only)
        data = [
            "Midnight City",
            "Nightcall",
            "Digital Love",
            "Instant Crush"
        ]

        matches = [s for s in data if text.lower() in s.lower()]

        self.results_view.clear_widgets()

        if not matches:
            self.set_state("empty")
            return

        for item in matches:
            row = Label(
                text=item,
                font_size="16sp",
                color=LIGHT_THEME["text_primary"],
                size_hint_y=None,
                height=dp(44),
                halign="left",
                valign="middle"
            )
            row.bind(size=row.setter("text_size"))
            self.results_view.add_widget(row)

        self.set_state("results")


class LibraryRow(BoxLayout):
    def __init__(self, title, artist, on_select, **kwargs):
        super().__init__(orientation = "horizontal", size_hint_y = None, height = dp(64), padding = [dp(16), dp(12)], spacing = dp(8), **kwargs)
        self.title, self.artist, self.on_select, self.is_playing = title, artist, on_select, False
        with self.canvas.before:
            self.bg_color = Color(*LIGHT_THEME["surface_alt"])
            self.bg = RoundedRectangle(radius = [16])
        self.bind(pos = self._update_bg, size = self._update_bg)
        art = Label(text="\ue405", font_name="MaterialIcons", font_size="28sp", size_hint=(None, None), size=(dp(40), dp(40)), color=LIGHT_THEME["icon"])
        text_box = BoxLayout(orientation = "vertical")
        self.title_label = Label(text = title, font_size = "16sp", color=LIGHT_THEME["text_primary"], bold = True, halign = "left", valign = "middle")
        self.title_label.bind(size = self.title_label.setter("text_size"))
        self.artist_label = Label(text = artist, font_size = "13sp", color=LIGHT_THEME["text_primary"], opacity = 0.5, halign = "left", valign = "middle", bold = False)
        self.artist_label.bind(size = self.artist_label.setter("text_size"))
        text_box.add_widget(self.title_label)
        text_box.add_widget(self.artist_label)
        self.add_widget(art)
        self.add_widget(text_box)

    def _update_bg(self, *args):
        self.bg.pos, self.bg.size = self.pos, self.size

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        self.on_select(self.title, self.artist)
        Animation(rgba=LIGHT_THEME["accent_soft"], duration=0.08).start(self.bg_color)
        Clock.schedule_once(lambda dt: Animation(rgba=LIGHT_THEME["surface_alt"], duration=0.12).start(self.bg_color), 0.12)
        return True

    def set_playing(self, playing):
        self.is_playing = playing
        self.bg_color.rgba = (0.3, 0.3, 0.45, 1) if playing else (0.15, 0.15, 0.18, 0)

    def set_dimmed(self, dimmed):
        Animation(opacity = 0.45 if dimmed else 1, duration = 0.15).start(self)


class LibraryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation = "vertical", padding = dp(24), spacing = dp(14))
        for title, artist in [("Midnight City", "M83"), ("Nightcall", "Kavinsky"), ("Digital Love", "Daft Punk")]:
            layout.add_widget(LibraryRow(title, artist, on_select = self.play))
        self.add_widget(layout)

    def play(self, title, artist):
        app = App.get_running_app()
        root = app.root
        root.current_index = next(i for i, s in enumerate(root.songs) if s[0] == title)
        root.current_title = title
        root.current_artist = artist
        root.current_artist = artist
        self.update_playing_row(title, artist)
        root.screen_manager.get_screen("now_playing").update_artwork("\ue405")
        root.go_to("now_playing")

    def update_playing_row(self, title, artist):
        for row in self.children[0].children:
            is_playing = (row.title == title and row.artist == artist)
            row.set_playing(is_playing)
            row.set_dimmed(not is_playing)

    def albums(self, *args, **kwargs):
        pass

    def artists(self, *args, **kwargs):
        pass

    def playlists(self, *args, **kwargs):
        pass

    def downloads(self, *args, **kwargs):
        pass


class NowPlayingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation = "vertical", padding = dp(24), spacing = dp(24))
        top_bar = BoxLayout(orientation = "horizontal", size_hint_y = None, height = dp(48), padding = [dp(8), 0])
        back_btn = Button(text = "\ue5c4", font_name = "MaterialIcons", font_size = "28sp", size_hint = (None, None), size = (dp(48), dp(48)), background_normal = "", background_color = (0, 0, 0, 0), on_press = self.go_back)
        top_bar.add_widget(back_btn)
        top_bar.add_widget(Widget())
        root.add_widget(top_bar)
        self.hero = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint_y=0.55,
            padding=dp(24)
        )
        with self.hero.canvas.before:
            Color(*LIGHT_THEME["surface"])
            self.hero_bg = RoundedRectangle(radius = [24])
            # Color(*LIGHT_THEME["accent_soft"][:3], 0.25)
            # self.hero_gradient = Rectangle()
        self.hero.bind(pos = self._update_hero, size = self._update_hero)
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint=(None, None)
        )
        content.width = dp(260)
        content.bind(minimum_height=content.setter("height"))
        self.title_label = Label(text = "Midnight City", font_size = "20sp", color=LIGHT_THEME["text_primary"], bold = True, size_hint_y = None, height = dp(28))
        self.artist_label = Label(text = "M83", font_size = "14sp", color=LIGHT_THEME["text_secondary"], opacity = 0.7, size_hint_y = None, height = dp(20))
        self.artwork = ArtworkIcon()
        content.add_widget(self.artwork)
        content.add_widget(self.title_label)
        content.add_widget(self.artist_label)
        self.hero.add_widget(content)
        root.add_widget(self.hero)
        self.timeline_container = BoxLayout(size_hint_y = None, height = dp(16), padding = [dp(24), 0])
        self.timeline = Widget()
        with self.timeline.canvas:
            Color(*LIGHT_THEME["surface_alt"])
            self.track_bg = RoundedRectangle(radius = [6])
            Color(*LIGHT_THEME["accent"])
            self.track_fill = RoundedRectangle(radius = [8], size = (0, dp(20)))
        self.timeline.bind(pos = self._update_timeline, size = self._update_timeline)
        self.timeline_container.add_widget(self.timeline)
        root.add_widget(self.timeline_container)
        self.current_time_label = Label(text = "0:00", font_size = "12sp", color=LIGHT_THEME["text_secondary"], size_hint = (None, None), size = (dp(40), dp(16)), halign = "left", valign = "middle")
        self.current_time_label.bind(size = self.current_time_label.setter("text_size"))
        self.total_time_label = Label(text = "0:00", font_size = "12sp", color=LIGHT_THEME["text_secondary"], size_hint = (None, None), size = (dp(40), dp(16)), halign = "right", valign = "middle")
        self.total_time_label.bind(size = self.total_time_label.setter("text_size"))
        self.timeline_container.add_widget(self.current_time_label)
        self.timeline_container.add_widget(self.total_time_label)
        self.controls = BoxLayout(orientation = "horizontal", spacing = dp(16), size_hint_y = None, height = dp(80), padding = [dp(16), 0])
        self.prev_btn = Button(text = "\ue045", font_name = "MaterialIcons", font_size = "24sp", color=LIGHT_THEME["icon"], background_normal = "", background_color = (0, 0, 0, 0), size = (dp(56), dp(56)), on_press = self.previous)
        self.next_btn = Button(text = "\ue044", font_name = "MaterialIcons", font_size = "24sp", color=LIGHT_THEME["icon"], background_normal = "", background_color = (0, 0, 0, 0), size = (dp(56), dp(56)), on_press = self.next)
        self.play_btn = Button(text = "\ue037", font_name = "MaterialIcons", font_size = "28sp", color=LIGHT_THEME["icon"], background_normal = "", background_color = (0, 0, 0, 0), size = (dp(72), dp(72)))
        self.shuffle_btn = Button(text = "\ue043", font_name = "MaterialIcons", font_size = "24sp", color=LIGHT_THEME["icon"], background_normal = "", background_color = (0, 0, 0, 0))
        self.repeat_btn = Button(text = "\ue040", font_name = "MaterialIcons", font_size = "24sp", color=LIGHT_THEME["icon"], background_normal = "", background_color = (0, 0, 0, 0))
        self.shuffle_btn.bind(on_press = lambda *_: App.get_running_app().root.toggle_shuffle())
        self.repeat_btn.bind(on_press = lambda *_: App.get_running_app().root.toggle_repeat())
        self.lyrics_btn = Button(text = "\ue8f4", font_name = "MaterialIcons", font_size = "20sp", color=LIGHT_THEME["icon"], background_normal = "", background_color = (0, 0, 0, 0), size = (dp(48), dp(48)), on_press = self.toggle_lyrics)
        self.queue_btn = Button(text="\ue8ef", font_name="MaterialIcons", font_size="20sp", color=LIGHT_THEME["icon"], background_normal="", background_color=(0, 0, 0, 0), on_press=self.open_queue)
        with self.play_btn.canvas.before:
            Color(*LIGHT_THEME["accent"])
            self.play_bg = RoundedRectangle(radius = [36])
        self.play_btn.bind(pos = self._update_play, size = self._update_play, on_press = lambda *_: App.get_running_app().root.toggle_play())
        self.controls.add_widget(self.shuffle_btn)
        self.controls.add_widget(self.prev_btn)
        self.controls.add_widget(self.play_btn)
        self.controls.add_widget(self.next_btn)
        self.controls.add_widget(self.repeat_btn)
        secondary_controls = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(56), padding=[dp(24), 0], spacing=dp(32))
        secondary_controls.add_widget(self.lyrics_btn)
        secondary_controls.add_widget(Widget())
        secondary_controls.add_widget(self.queue_btn)
        root.add_widget(self.controls)
        root.add_widget(secondary_controls)
        self.lyrics_box = BoxLayout(orientation = "vertical", size_hint_y = None, height = 0, opacity = 0)
        self.lyrics_label = Label(text = "Lyrics will appear here...", font_size = "14sp", halign = "center", valign = "top", text_size = (self.width - dp(48), None))
        self.lyrics_label.bind(size = self.lyrics_label.setter("text_size"))
        self.lyrics_box.add_widget(self.lyrics_label)
        root.add_widget(self.lyrics_box)
        self.add_widget(root)
        self.timeline_anim = None
        self.timeline_duration = 8
        self.timeline_progress = 0
        self.timeline_running = False
        self.seeking = False
        self.queue_sheet = None

    def _update_play(self, *args):
        self.play_bg.pos, self.play_bg.size = self.play_btn.pos, self.play_btn.size

    def _update_hero(self, *args):
        self.hero_bg.pos, self.hero_bg.size = self.hero.pos, self.hero.size

    def update_play_state(self, is_playing):
        self.play_btn.text = "\ue034" if is_playing else "\ue037"
        self.animate_play()

    def update_shuffle_state(self, enabled):
        self.shuffle_btn.opacity = 1 if enabled else 0.4

    def update_repeat_state(self, mode):
        if mode == "off":
            self.repeat_btn.text = "\ue040"
            self.repeat_btn.opacity = 0.4
        elif mode == "all":
            self.repeat_btn.text = "\ue040"
            self.repeat_btn.opacity = 1
        else:
            self.repeat_btn.text = "\ue041"
            self.repeat_btn.opacity = 1

    def animate_play(self, *args):
        (Animation(size = (dp(80), dp(80)), duration = 0.08) + Animation(size = (dp(72), dp(72)), duration = 0.08)).start(self.play_btn)

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        root = app.root
        self.update_play_state(root.is_playing)
        self.update_shuffle_state(root.shuffle_enabled)
        self.update_repeat_state(root.repeat_mode)
        if root.current_title:
            self.title_label.text = root.current_title
            self.artist_label.text = root.current_artist
        self.opacity = 0
        Animation(opacity = 1, duration = 0.25).start(self)
        if root.is_playing:
            Clock.schedule_once(lambda dt: self.resume_timeline(), 0.05)

    def _update_timeline(self, *args):
        self.track_bg.pos, self.track_bg.size = self.timeline.pos, self.timeline.size
        self.track_fill.pos = self.timeline.pos

    def pause_timeline(self):
        if self.timeline_anim:
            Animation.cancel_all(self.track_fill)
            self.timeline_running = False

    def resume_timeline(self):
        if not self.timeline_running:
            self.start_timeline()

    def start_timeline(self, duration = None):
        if duration:
            self.timeline_duration = duration
        Animation.cancel_all(self.track_fill)
        self.track_fill.size = (self.timeline_progress * self.timeline.width, self.timeline.height)
        def update_time(anim, widget, progress):
            self.timeline_progress = progress
            elapsed = progress * self.timeline_duration
            self.current_time_label.text = f"{int(elapsed)//60}:{int(elapsed)%60:02d}"
            self.total_time_label.text = f"{int(self.timeline_duration)//60}:{int(self.timeline_duration)%60:02d}"
        self.timeline_anim = Animation(size = (self.timeline.width, self.timeline.height), duration = self.timeline_duration * (1 - self.timeline_progress), t = "linear")
        self.timeline_anim.bind(on_progress = update_time, on_complete = self.on_timeline_complete)
        self.timeline_anim.start(self.track_fill)
        self.timeline_running = True

    def on_timeline_complete(self, *args):
        if self.seeking:
            return
        self.timeline_running = False
        self.timeline_progress = 0
        root = App.get_running_app().root
        if not root.is_playing:
            return
        if root.repeat_mode == "one":
            self.start_timeline()
            return
        next_index = root.get_next_index()
        if next_index == root.current_index and root.repeat_mode == "off":
            root.is_playing = False
            root.mini_player.update_play_state(False)
            self.update_play_state(False)
            return
        root.play_song_at(next_index)

    def start_seek(self, touch):
        self.seeking = True
        self.pause_timeline()
        self.update_seek(touch)

    def update_seek(self, touch):
        x = min(max(touch.x, self.timeline.x), self.timeline.right)
        progress = (x - self.timeline.x) / self.timeline.width
        self.timeline_progress = progress
        self.track_fill.size = (progress * self.timeline.width, self.timeline.height)
        elapsed = progress * self.timeline_duration
        self.current_time_label.text = f"{int(elapsed)//60}:{int(elapsed)%60:02d}"
        self.total_time_label.text = f"{int(self.timeline_duration)//60}:{int(self.timeline_duration)%60:02d}"

    def end_seek(self):
        self.seeking = False
        root = App.get_running_app().root
        if root.is_playing:
            self.resume_timeline()

    def animate_song_change(self, new_title, new_artist):
        out_anim = Animation(opacity = 0, y = self.title_label.y + dp(10), duration = 0.15)
        def update_text(*args):
            self.title_label.text = new_title
            self.artist_label.text = new_artist
            self.title_label.y -= dp(10)
            self.artist_label.y -= dp(10)
            Animation(opacity = 1, y = self.title_label.y + dp(10), duration = 0.2).start(self.title_label)
            Animation(opacity = 0.7, y = self.artist_label.y + dp(10), duration = 0.25).start(self.artist_label)
            # if App.get_running_app().root.is_playing:
            #     self.start_timeline()
        out_anim.bind(on_complete = lambda *x: update_text())
        out_anim.start(self.title_label)
        out_anim.start(self.artist_label)

    def update_artwork(self, icon = "\ue405"):
        self.artwork.icon.text = icon

    def toggle_lyrics(self, *args):
        if self.lyrics_box.height == 0:
            Animation(height = dp(200), opacity = 1, duration = 0.3).start(self.lyrics_box)
        else:
            Animation(height = 0, opacity = 0, duration = 0.3).start(self.lyrics_box)

    def play_pause(self, *args, **kwargs):
        pass

    def next(self, *args, **kwargs):
        App.get_running_app().root.next_song()

    def previous(self, *args, **kwargs):
        App.get_running_app().root.previous_song()

    def lyrics(self, *args, **kwargs):
        pass

    def go_back(self, *args):
        App.get_running_app().root.go_to("library")

    def on_touch_down(self, touch):
        if self.timeline.collide_point(*touch.pos):
            self.start_seek(touch)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.seeking:
            self.update_seek(touch)  # update rectangle + time labels
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.seeking:
            self.end_seek()
            return True
        return super().on_touch_up(touch)

    def open_queue(self, *args):
        if self.queue_sheet:
            return
        self.queue_sheet = QueueBottomSheet(self._close_queue)
        self.queue_sheet.present(self)

    def _close_queue(self, sheet):
        if sheet in self.children:
            self.remove_widget(sheet)
        self.queue_sheet = None


class QueueRow(BoxLayout):
    def __init__(self, title, artist, is_current=False, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=dp(56), padding=[dp(12), dp(8)], spacing=dp(8), **kwargs)
        self.title = title
        self.artist = artist
        self.is_current = is_current
        self.dragging = False
        self.original_y = 0
        self.drag_offset = 0

        with self.canvas.before:
            self.bg_color = Color(*LIGHT_THEME["accent_soft"])
            self.bg = RoundedRectangle(radius=[12])
        self.bind(pos=self._update_bg, size=self._update_bg)

        text_box = BoxLayout(orientation="vertical")
        self.title_lbl = Label(text=title, bold=True, font_size="14sp", color=LIGHT_THEME["text_primary"], halign="left", valign="middle")
        self.title_lbl.bind(size=self.title_lbl.setter("text_size"))
        self.artist_lbl = Label(text=artist, font_size="12sp", color=LIGHT_THEME["text_secondary"], opacity=0.6, halign="left", valign="middle")
        self.artist_lbl.bind(size=self.artist_lbl.setter("text_size"))
        text_box.add_widget(self.title_lbl)
        text_box.add_widget(self.artist_lbl)
        self.add_widget(text_box)
        self.add_widget(Widget())  # spacer

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    # --- Drag & Drop ---
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dragging = True
            self.drag_offset = touch.y - self.y
            self.original_y = self.y
            touch.grab(self)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self and self.dragging:
            self.y = touch.y - self.drag_offset
            parent = self.parent

            # Iterate siblings in visual order (top to bottom)
            for sib in reversed(parent.children):
                if sib == self:
                    continue
                # Swap if center crosses sibling center
                if self.center_y > sib.center_y + sib.height / 2:
                    # move above sibling
                    parent.remove_widget(self)
                    parent.add_widget(self, index=parent.children.index(sib)+1)
                    break
                elif self.center_y < sib.center_y - sib.height / 2:
                    # move below sibling
                    parent.remove_widget(self)
                    parent.add_widget(self, index=parent.children.index(sib))
                    break
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.dragging = False
            # Snap to sibling y positions
            parent = self.parent
            siblings = [w for w in parent.children if isinstance(w, QueueRow)]
            siblings.sort(key=lambda w: w.y, reverse=True)  # top-to-bottom
            for i, sib in enumerate(siblings):
                Animation(y=sib.y, duration=0.15, t="out_quad").start(sib)
            return True
        return super().on_touch_up(touch)


class QueueBottomSheet(BoxLayout):
    def __init__(self, close_callback, **kwargs):
        super().__init__(orientation="vertical", size_hint_y=None, height=0, padding=dp(16), spacing=dp(12), **kwargs)
        self.close_callback = close_callback
        with self.canvas.before:
            Color(*LIGHT_THEME["surface"])
            self.bg = RoundedRectangle(radius=[24])
        self.bind(pos=self._update_bg, size=self._update_bg)
        header = BoxLayout(size_hint_y=None, height=dp(48))
        title = Label(text="Up Next", font_size="18sp", color=LIGHT_THEME["text_primary"], bold=True, halign="left", valign="middle")
        title.bind(size=title.setter("text_size"))
        close_btn = Button(text="\ue5cd", font_name="MaterialIcons", font_size="24sp", background_normal="", background_color=(0, 0, 0, 0), size_hint=(None, None), size=(dp(48), dp(48)), on_press=self.dismiss)
        header.add_widget(title)
        header.add_widget(Widget())
        header.add_widget(close_btn)
        self.add_widget(header)
        self.list_container = BoxLayout(orientation="vertical", spacing=dp(8))
        self.state_container = BoxLayout()
        self.add_widget(self.state_container)
        self.loading_view = self._build_loading()
        self.empty_view = self._build_empty()
        self.list_view = self._build_list()
        self.state_container.add_widget(self.loading_view)
        self.add_widget(self.list_container)
        self.state = "loading"

    def _update_bg(self, *args):
        self.bg.pos, self.bg.size = self.pos, self.size

    def present(self, parent):
        parent.add_widget(self)
        Animation(height=parent.height * 0.6, duration=0.25, t="out_quad").start(self)
        Clock.schedule_once(self._hint_drag, 0.35)
        Clock.schedule_once(lambda *_: self.set_state("list"), 0.6)

    def dismiss(self, *args):
        anim = Animation(height=0, duration=0.2, t="out_quad")
        anim.bind(on_complete=lambda *_: self.close_callback(self))
        anim.start(self)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            self.dismiss()
            return True
        return super().on_touch_down(touch)

    def _hint_drag(self, *args):
        for child in self.list_container.children:
            if isinstance(child, QueueRow) and not child.is_current:
                anim = Animation(x=child.x + dp(6), duration=0.08) + Animation(x=child.x, duration=0.08)
                anim.start(child)
                break

    def _build_loading(self):
        box = BoxLayout(orientation="vertical", spacing=dp(12))
        spinner = Label(text="\ue86a", font_name="MaterialIcons", font_size="32sp", opacity=0.6)
        text = Label(text="Loading queue…", opacity=0.6)
        box.add_widget(Widget())
        box.add_widget(spinner)
        box.add_widget(text)
        box.add_widget(Widget())
        return box

    def _build_empty(self):
        box = BoxLayout(orientation="vertical", spacing=dp(12))
        icon = Label(text="\ue03b", font_name="MaterialIcons", font_size="40sp", opacity=0.4)
        text = Label(text="Nothing up next", font_size="16sp", opacity=0.6)
        hint = Label(text="Play something to build your queue", font_size="13sp", opacity=0.4)
        box.add_widget(Widget())
        box.add_widget(icon)
        box.add_widget(text)
        box.add_widget(hint)
        box.add_widget(Widget())
        return box

    def _build_list(self):
        box = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))
        rows = [
            ("Midnight City", "M83", True),
            ("Nightcall", "Kavinsky", False),
            ("Digital Love", "Daft Punk", False)
        ]
        for t, a, c in rows:
            row = QueueRow(t, a, c)
            box.add_widget(row)
        return box

    def set_state(self, state):
        if self.state == state:
            return
        self.state = state
        self.state_container.clear_widgets()
        view = {"loading": self.loading_view, "empty": self.empty_view, "list": self.list_view}[state]
        view.opacity = 0
        self.state_container.add_widget(view)
        Animation(opacity=1, duration=0.2).start(view)


class MusicPlayerApp(App):
    def build(self):
        root = RootLayout()
        root.screen_manager.add_widget(PlaylistsScreen(name="playlists"))
        root.screen_manager.add_widget(SearchScreen(name="search"))
        root.screen_manager.add_widget(LibraryScreen(name="library"))
        root.screen_manager.add_widget(NowPlayingScreen(name="now_playing"))
        root.go_to("library")
        return root


if __name__ == "__main__":
    MusicPlayerApp().run()
