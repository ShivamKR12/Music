from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.app import App

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemLeadingIcon
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText

from models.database import get_all_playlists, add_playlist

class PlaylistsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root_box = MDBoxLayout(orientation="vertical", padding=dp(32), spacing=dp(24), size_hint_y=None)
        self.root_box.bind(minimum_height=self.root_box.setter("height"))

        scroll = MDScrollView(size_hint=(1, 1), always_overscroll=False)
        scroll.add_widget(self.root_box)
        self.add_widget(scroll)
        
        self.dialog = None

    def on_enter(self):
        """Triggers dynamically to populate real metrics when screen is focused."""
        self.populate_playlists()

    def populate_playlists(self):
        self.root_box.clear_widgets()
        
        header = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48))
        title = MDLabel(text="Playlists", font_style="Headline", role="medium", bold=True, halign="left")
        
        create_btn = MDIconButton(
            icon="plus",
            theme_icon_color="Custom",
            icon_color=(0.2, 0.6, 1.0, 1), # LIGHT_THEME accent
            pos_hint={"center_y": 0.5},
            on_press=self.show_create_popup
        )
        
        header.add_widget(title)
        header.add_widget(create_btn)
        
        self.root_box.add_widget(header)
        
        active_playlists = get_all_playlists()
        
        if not active_playlists:
            empty_lbl = MDLabel(text="No playlists found\n(Create one to get started)", font_style="Body", role="large", theme_text_color="Hint", halign="center", size_hint_y=None, height=dp(100))
            self.root_box.add_widget(empty_lbl)
            return

        playlist_list = MDList(spacing=dp(8))
        for name in active_playlists:
            item = MDListItem(
                MDListItemLeadingIcon(icon="playlist-music"),
                MDListItemHeadlineText(text=name),
                radius=[dp(12)],
                theme_bg_color="Custom",
                md_bg_color=(0.95, 0.95, 0.97, 1),
                on_release=lambda x, n=name: self._go_to_playlist_detail(n)
            )
            playlist_list.add_widget(item)
            
        self.root_box.add_widget(playlist_list)

    def _go_to_playlist_detail(self, name):
        root_layout = App.get_running_app().root
        detail_screen = root_layout.screen_manager.get_screen("playlist_detail")
        detail_screen.set_playlist(name)
        root_layout.go_to("playlist_detail")

    def show_create_popup(self, *args):
        self.playlist_input = MDTextField(
            MDTextFieldHintText(text="Playlist Name"),
            mode="outlined",
        )
        
        cancel_btn = MDButton(
            MDButtonText(text="CANCEL"),
            style="text",
            on_release=lambda x: self.dialog.dismiss() if self.dialog else None
        )
        
        create_btn = MDButton(
            MDButtonText(text="CREATE"),
            style="text",
            on_release=self._on_create_playlist
        )
        
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="New Playlist"),
            MDDialogContentContainer(self.playlist_input, orientation="vertical"),
            MDDialogButtonContainer(cancel_btn, create_btn, spacing=dp(8))
        )
        self.dialog.open()

    def _on_create_playlist(self, *args):
        name = self.playlist_input.text.strip()
        if name:
            add_playlist(name)
            self.populate_playlists()
            if self.dialog:
                self.dialog.dismiss()