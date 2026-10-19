import os
import datetime
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.app import App
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout

from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemLeadingIcon, MDListItemLeadingAvatar
from kivymd.uix.button import MDIconButton

from models.database import get_continue_listening, get_recently_added
from utils import get_thumbnail_path
from ui.components import ArtworkIcon

class CategoryCard(MDCard):
    def __init__(self, title, icon_name, subtitle, on_press_cb=None, **kwargs):
        super().__init__(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=(0.95, 0.95, 0.97, 1),
            radius=[dp(16)],
            size_hint_y=None, 
            height=dp(140),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            **kwargs
        )
        self.on_press_cb = on_press_cb
        
        box = MDBoxLayout(orientation="vertical", spacing=dp(8))
        
        icon = MDIconButton(
            icon=icon_name,
            theme_icon_color="Custom",
            icon_color=(0.2, 0.6, 1.0, 1),
            pos_hint={"left": 1},
            padding=0
        )
        icon.disabled = True
        
        title_lbl = MDLabel(
            text=title, 
            font_style="Title", 
            role="medium",
            bold=True, 
            halign="left"
        )
        
        sub_lbl = MDLabel(
            text=subtitle, 
            font_style="Body", 
            role="small",
            theme_text_color="Hint", 
            halign="left"
        )
        
        box.add_widget(icon)
        box.add_widget(title_lbl)
        box.add_widget(sub_lbl)
        self.add_widget(box)

    def on_release(self):
        if self.on_press_cb:
            Clock.schedule_once(lambda dt: self.on_press_cb(), 0.15)

class HorizontalAlbumCard(MDCard):
    def __init__(self, title, artist, thumb_path, on_select, **kwargs):
        super().__init__(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=(0.95, 0.95, 0.97, 1),
            radius=[dp(16)],
            size_hint=(None, None),
            size=(dp(160), dp(220)),
            padding=dp(12),
            **kwargs
        )
        self.title = title
        self.artist = artist
        self.on_select = on_select
        
        box = MDBoxLayout(orientation="vertical", spacing=dp(12))
        
        self.art = ArtworkIcon(size_hint=(None, None), size=(dp(136), dp(136)))
        self.art.bg.radius = [dp(20)]
        self.art.icon.font_size = "48sp"
        self.art.set_artwork(thumb_path)
        
        text_box = MDBoxLayout(orientation="vertical", spacing=dp(4))
        title_lbl = MDLabel(
            text=title, 
            font_style="Title", 
            role="small",
            bold=True, 
            halign="left",
            shorten=True, 
            shorten_from="right"
        )
        
        artist_lbl = MDLabel(
            text=artist, 
            font_style="Body", 
            role="small",
            theme_text_color="Hint", 
            halign="left",
            shorten=True, 
            shorten_from="right"
        )
        
        text_box.add_widget(title_lbl)
        text_box.add_widget(artist_lbl)
        
        box.add_widget(self.art)
        box.add_widget(text_box)
        self.add_widget(box)

    def on_release(self):
        if self.on_select:
            Clock.schedule_once(lambda dt: self.on_select(self.title, self.artist), 0.15)

class LibraryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        root = MDBoxLayout(orientation="vertical")
        
        self.main_layout = MDBoxLayout(orientation="vertical", spacing=dp(32), size_hint_y=None, padding=[0, dp(32), 0, dp(32)])
        self.main_layout.bind(minimum_height=self.main_layout.setter("height"))
        
        scroll = MDScrollView(size_hint=(1, 1), always_overscroll=False)
        scroll.add_widget(self.main_layout)
        root.add_widget(scroll)
        self.add_widget(root)
        
        Clock.schedule_once(self.populate)
        self._last_catalog_size = -1

    def on_enter(self):
        self.populate()

    def create_song_carousel(self, title_text, songs):
        box = MDBoxLayout(orientation="vertical", size_hint_y=None, height=dp(280), spacing=dp(16))
        title = MDLabel(text=title_text, font_style="Title", role="large", bold=True, size_hint_y=None, height=dp(32), padding=[dp(32), 0, 0, 0])
        box.add_widget(title)
        
        scroll = MDScrollView(size_hint=(1, None), height=dp(232), always_overscroll=False, do_scroll_y=False, do_scroll_x=True)
        layout = MDBoxLayout(orientation="horizontal", spacing=dp(16), size_hint_x=None, padding=[dp(32), 0, dp(32), 0])
        layout.bind(minimum_width=layout.setter("width"))
        
        for t, a, u, v in songs:
            thumb = get_thumbnail_path(v)
            layout.add_widget(HorizontalAlbumCard(t, a, thumb, on_select=self.play))
            
        scroll.add_widget(layout)
        box.add_widget(scroll)
        return box

    def populate(self, *args):
        self.main_layout.clear_widgets()
        
        # Hero Section
        hero_box = MDBoxLayout(orientation="vertical", size_hint_y=None, height=dp(80), spacing=dp(4), padding=[dp(32), 0])
        import datetime
        hour = datetime.datetime.now().hour
        if hour < 12: greeting_text = "Good morning"
        elif hour < 18: greeting_text = "Good afternoon"
        else: greeting_text = "Good evening"
        
        greeting = MDLabel(text=greeting_text, font_style="Title", role="small", theme_text_color="Hint", size_hint_y=None, height=dp(24))
        title = MDLabel(text="Your Music", font_style="Headline", role="medium", bold=True, size_hint_y=None, height=dp(48))
        hero_box.add_widget(greeting)
        hero_box.add_widget(title)
        self.main_layout.add_widget(hero_box)
        
        root_layout = App.get_running_app().root
        if not root_layout: return
        self._last_catalog_size = len(root_layout.songs)
        
        # 1. Continue Listening
        continue_songs = get_continue_listening(limit=8)
        if not continue_songs and root_layout.songs:
            continue_songs = root_layout.songs[:8]
        if continue_songs:
            self.main_layout.add_widget(self.create_song_carousel("Continue Listening", continue_songs))
            
        # 2. Dynamic Playlists (Favorites, Workout, etc)
        from models.database import get_all_playlists, get_playlist_tracks
        playlists = get_all_playlists()
        for p_name in playlists:
            p_tracks = get_playlist_tracks(p_name)
            if p_tracks:
                self.main_layout.add_widget(self.create_song_carousel(p_name, p_tracks[:10]))
                
        # 3. Recently Added (Vertical list at the bottom for easy scrolling)
        recent_songs = get_recently_added(limit=15)
        if recent_songs:
            recent_box = MDBoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(16), padding=[dp(32), 0])
            recent_box.bind(minimum_height=recent_box.setter("height"))
            recent_title = MDLabel(text="Recently Added", font_style="Title", role="large", bold=True, size_hint_y=None, height=dp(32))
            recent_box.add_widget(recent_title)
            
            songs_layout = MDBoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
            songs_layout.bind(minimum_height=songs_layout.setter("height"))
            
            for i, (t, a, u, v) in enumerate(recent_songs):
                thumb_path = get_thumbnail_path(v)
                from kivymd.uix.list import MDListItemLeadingAvatar, MDListItemLeadingIcon, MDListItem, MDListItemHeadlineText, MDListItemSupportingText
                avatar = MDListItemLeadingAvatar(source=thumb_path) if thumb_path else MDListItemLeadingIcon(icon="music-circle-outline")
                item = MDListItem(
                    avatar,
                    MDListItemHeadlineText(text=t),
                    MDListItemSupportingText(text=a),
                    radius=[dp(12)],
                    theme_bg_color="Custom",
                    md_bg_color=(0.95, 0.95, 0.97, 1),
                    on_release=lambda x, title=t, artist=a: self.play(title, artist)
                )
                songs_layout.add_widget(item)
                
            recent_box.add_widget(songs_layout)
            self.main_layout.add_widget(recent_box)

    def play(self, title, artist):
        root_layout = App.get_running_app().root
        try:
            index = next(i for i, s in enumerate(root_layout.songs) if s[0] == title)
            root_layout.go_to("now_playing")
            root_layout.play_song_at(index, rebuild_queue=True)
        except StopIteration: pass
