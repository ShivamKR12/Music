from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.app import App
from kivy.clock import Clock

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemLeadingAvatar, MDListItemLeadingIcon

from models.database import get_playlist_tracks
from utils import get_thumbnail_path

class PlaylistDetailScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.playlist_name = ""
        
        self.root_box = MDBoxLayout(orientation="vertical", padding=dp(32), spacing=dp(24), size_hint_y=None)
        self.root_box.bind(minimum_height=self.root_box.setter("height"))

        scroll = MDScrollView(size_hint=(1, 1), always_overscroll=False)
        scroll.add_widget(self.root_box)
        self.add_widget(scroll)

    def set_playlist(self, name):
        self.playlist_name = name
        self.populate()

    def on_enter(self):
        self.populate()

    def populate(self, *args):
        self.root_box.clear_widgets()
        
        header = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48))
        
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_icon_color="Custom",
            icon_color=(0.2, 0.6, 1.0, 1),
            pos_hint={"center_y": 0.5},
            on_release=lambda x: App.get_running_app().root.go_to("playlists")
        )
        
        title = MDLabel(text=self.playlist_name, font_style="Headline", role="medium", bold=True, halign="left", padding=[dp(16), 0, 0, 0])
        
        header.add_widget(back_btn)
        header.add_widget(title)
        
        self.root_box.add_widget(header)
        
        tracks = get_playlist_tracks(self.playlist_name)
        
        if not tracks:
            empty_lbl = MDLabel(text="No tracks in this playlist yet.", font_style="Body", role="large", theme_text_color="Hint", halign="center", size_hint_y=None, height=dp(100))
            self.root_box.add_widget(empty_lbl)
            return

        track_list = MDList(spacing=dp(8))
        for title_str, artist, url, video_id in tracks:
            thumb_path = get_thumbnail_path(video_id)
            avatar = MDListItemLeadingAvatar(source=thumb_path) if thumb_path else MDListItemLeadingIcon(icon="music-circle-outline")
            
            item = MDListItem(
                avatar,
                MDListItemHeadlineText(text=title_str),
                MDListItemSupportingText(text=artist),
                radius=[dp(12)],
                theme_bg_color="Custom",
                md_bg_color=(0.95, 0.95, 0.97, 1),
                on_release=lambda x, t=title_str, a=artist: self.play_track(t, a)
            )
            track_list.add_widget(item)
            
        self.root_box.add_widget(track_list)

    def play_track(self, title, artist):
        root_layout = App.get_running_app().root
        
        # In a real app we might load ONLY this playlist into the queue, 
        # but for now we find the song in the global catalog and play it.
        # This keeps our queue logic simple.
        try:
            index = next(i for i, s in enumerate(root_layout.songs) if s[0] == title)
            root_layout.go_to("now_playing")
            root_layout.play_song_at(index, rebuild_queue=True)
        except StopIteration:
            pass

