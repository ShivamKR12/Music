from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.app import App
from kivy.uix.widget import Widget
import threading

# KivyMD Imports
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText, MDTextFieldLeadingIcon
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemLeadingIcon, MDListItemLeadingAvatar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton

from models.database import add_track, add_search_history, get_search_history, clear_search_history
from utils import extract_video_id, fetch_youtube_metadata, get_thumbnail_path
from logger import app_logger

class SearchScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_state = "idle"
        self.current_query = ""
        
        root = MDBoxLayout(orientation="vertical", padding=dp(32), spacing=dp(24))

        title = MDLabel(
            text="Search",
            font_style="Headline",
            role="medium",
            bold=True,
            size_hint_y=None,
            height=dp(48)
        )
        root.add_widget(title)

        self.search_input = MDTextField(
            MDTextFieldLeadingIcon(icon="magnify"),
            MDTextFieldHintText(text="Search or paste a YouTube link..."),
            mode="outlined",
        )
        self.search_input.bind(text=self.on_search_text)
        root.add_widget(self.search_input)

        self.state_container = MDBoxLayout()
        root.add_widget(self.state_container)

        self.idle_view = MDBoxLayout(orientation="vertical", spacing=dp(8))
        self.idle_view.bind(minimum_height=self.idle_view.setter("height"))
        
        self.typing_view = MDLabel(text="Searching...", font_style="Title", role="medium", halign="center", opacity=0.6)
        self.empty_view = MDLabel(text="No results found", font_style="Title", role="medium", halign="center", theme_text_color="Error")

        self.scroll_view = MDScrollView(always_overscroll=False)
        self.results_box = MDBoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        self.results_box.bind(minimum_height=self.results_box.setter("height"))
        self.results_list = MDList(spacing=dp(8))
        
        self.online_search_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(56), padding=[0, dp(16), 0, 0])
        self.online_search_btn = MDButton(
            MDButtonText(text="Search YouTube"),
            style="tonal",
            pos_hint={"center_x": 0.5},
            on_release=self.start_online_search
        )
        self.online_search_box.add_widget(Widget())
        self.online_search_box.add_widget(self.online_search_btn)
        self.online_search_box.add_widget(Widget())
        
        self.results_box.add_widget(self.results_list)
        self.results_box.add_widget(self.online_search_box)
        self.scroll_view.add_widget(self.results_box)

        self.add_widget(root)
        self.set_state("idle")

    def set_state(self, state):
        if self.search_state == state: return
        self.search_state = state
        self.state_container.clear_widgets()

        if state == "idle":
            self.populate_history()
            self.state_container.add_widget(self.idle_view)
        elif state == "typing":
            self.state_container.add_widget(self.typing_view)
        elif state == "empty":
            self.state_container.add_widget(self.empty_view)
        elif state == "results":
            self.state_container.add_widget(self.scroll_view)

    def populate_history(self):
        self.idle_view.clear_widgets()
        history = get_search_history(limit=15)
        
        if not history:
            lbl = MDLabel(text="Search for songs, artists, or albums", font_style="Title", role="medium", halign="center", opacity=0.6)
            self.idle_view.add_widget(lbl)
            return

        header = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48), padding=[dp(16), 0])
        title = MDLabel(text="Recent Searches", font_style="Title", role="medium", bold=True, halign="left")
        clear_btn = MDButton(
            MDButtonText(text="CLEAR"),
            style="text",
            on_release=self.clear_history,
            pos_hint={"center_y": 0.5}
        )
        header.add_widget(title)
        header.add_widget(clear_btn)
        
        self.idle_view.add_widget(header)

        scroll = MDScrollView(always_overscroll=False)
        hist_list = MDList(spacing=dp(4))
        
        for q in history:
            item = MDListItem(
                MDListItemLeadingIcon(icon="history"),
                MDListItemHeadlineText(text=q),
                radius=[dp(12)],
                theme_bg_color="Custom",
                md_bg_color=(0.95, 0.95, 0.97, 1),
                on_release=lambda x, text=q: self._apply_history_search(text)
            )
            hist_list.add_widget(item)
            
        scroll.add_widget(hist_list)
        self.idle_view.add_widget(scroll)

    def _apply_history_search(self, text):
        self.search_input.text = text

    def clear_history(self, *args):
        clear_search_history()
        self.populate_history()

    def on_search_text(self, instance, text):
        text = text.strip()
        self.current_query = text
        if not text:
            self.set_state("idle")
            return

        if "youtube.com/" in text or "youtu.be/" in text:
            self.set_state("typing")
            self.typing_view.text = "Extracting video metadata..."
            
            app_logger.info(f"[THREAD START] SearchScreen._async_url_extractor for URL: {text}")
            threading.Thread(target=self._async_url_extractor, args=(text,), daemon=True).start()
            return

        self.set_state("typing")
        self.typing_view.text = "Searching local library..."
        
        root_layout = MDApp.get_running_app().root
        self.results_list.clear_widgets()
        
        matches = 0
        for i, song_data in enumerate(root_layout.songs):
            title = song_data[0]
            artist = song_data[1]
            video_id = song_data[3]
            if text.lower() in title.lower() or text.lower() in artist.lower():
                matches += 1
                thumb_path = get_thumbnail_path(video_id)
                avatar = MDListItemLeadingAvatar(source=thumb_path) if thumb_path else MDListItemLeadingIcon(icon="music-note")
                item = MDListItem(
                    avatar,
                    MDListItemHeadlineText(text=title),
                    MDListItemSupportingText(text=artist),
                    radius=[dp(12)],
                    theme_bg_color="Custom",
                    md_bg_color=(0.95, 0.95, 0.97, 1),
                    on_release=lambda x, idx=i: self.play_local_result(idx)
                )
                self.results_list.add_widget(item)

        for child in self.online_search_btn.children:
            if isinstance(child, MDButtonText):
                child.text = f"Search YouTube for '{text}'"
        
        self.online_search_box.opacity = 1
        self.online_search_btn.disabled = False
        
        self.set_state("results")

    def start_online_search(self, *args):
        if not hasattr(self, 'current_query') or not self.current_query: return
        
        add_search_history(self.current_query)
        
        self.set_state("typing")
        self.typing_view.text = f"Searching YouTube for '{self.current_query}'..."
        
        query = self.current_query
        app_logger.info(f"[THREAD START] SearchScreen._async_youtube_search for: {query}")
        threading.Thread(target=self._async_youtube_search, args=(query,), daemon=True).start()

    def _async_youtube_search(self, query):
        try:
            info = fetch_youtube_metadata(f"ytsearch10:{query}", extract_flat=True)
            entries = info.get('entries', [])
            Clock.schedule_once(lambda dt: self._on_online_search_success(entries) if self.parent else None, 0)
        except Exception as e:
            app_logger.error(f"YouTube search error exception: {e}")
            
            def _show_err(dt):
                if self.parent:
                    self.set_state("empty")
                    MDApp.get_running_app().root.show_error(f"YouTube search failed:\n{e}")
                    
            Clock.schedule_once(_show_err, 0)

    def _on_online_search_success(self, entries):
        self.results_list.clear_widgets()
        
        if not entries:
            self.set_state("empty")
            return
            
        for entry in entries:
            video_id = entry.get('id')
            title = entry.get('title', 'Unknown Title')
            artist = entry.get('uploader', 'Unknown Artist')
            duration = int(entry.get('duration', 0) or 0)
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            thumb_path = get_thumbnail_path(video_id)
            avatar = MDListItemLeadingAvatar(source=thumb_path) if thumb_path else MDListItemLeadingIcon(icon="youtube")
            
            item = MDListItem(
                avatar,
                MDListItemHeadlineText(text=title),
                MDListItemSupportingText(text=artist),
                radius=[dp(12)],
                theme_bg_color="Custom",
                md_bg_color=(0.95, 0.95, 0.97, 1),
                on_release=lambda x, v=video_id, t=title, a=artist, u=url, d=duration: self.play_online_result(v, t, a, u, d)
            )
            self.results_list.add_widget(item)
            
        self.online_search_box.opacity = 0
        self.online_search_btn.disabled = True
        self.set_state("results")

    def play_local_result(self, index):
        if hasattr(self, 'current_query') and self.current_query:
            add_search_history(self.current_query)
            
        root_layout = MDApp.get_running_app().root
        if index < 0 or index >= len(root_layout.songs): return
        root_layout.go_to("now_playing")
        root_layout.play_song_at(index, rebuild_queue=True)
        
    def play_online_result(self, video_id, title, artist, url, duration):
        if hasattr(self, 'current_query') and self.current_query:
            add_search_history(self.current_query)
            
        root_layout = MDApp.get_running_app().root
        
        existing_index = None
        for i, song_data in enumerate(root_layout.songs):
            if song_data[3] == video_id:
                existing_index = i
                break
                
        if existing_index is not None:
            self.play_local_result(existing_index)
            return
            
        add_track(video_id, title, artist, url, duration)
        root_layout.refresh_catalog()
        
        new_track_index = len(root_layout.songs) - 1
        
        lib_screen = root_layout.screen_manager.get_screen("library")
        if lib_screen:
            lib_screen.populate()
            
        self.play_local_result(new_track_index)

    def _async_url_extractor(self, url):
        try:
            video_id = extract_video_id(url)
        except ValueError as e:
            app_logger.error(f"[THREAD FAILED] SearchScreen._async_url_extractor invalid URL {url}: {e}")
            Clock.schedule_once(lambda dt: self.set_state("empty") if self.parent else None, 0)
            return
            
        try:
            info = fetch_youtube_metadata(url)
            title = info.get('title', 'Unknown Title')
            artist = info.get('uploader', 'Unknown Artist')
            duration = int(info.get('duration', 0))

            add_track(video_id, title, artist, url, duration)

            app_logger.info(f"[THREAD SUCCESS] SearchScreen._async_url_extractor completed for URL: {url}")
            Clock.schedule_once(lambda dt: self._on_url_extraction_success(title, artist) if self.parent else None, 0)
        except Exception as e:
            app_logger.error(f"Link parsing error exception: {e}")
            
            def _show_err(dt):
                if self.parent:
                    self.set_state("empty")
                    MDApp.get_running_app().root.show_error(f"Link extraction failed:\n{e}")
                    
            Clock.schedule_once(_show_err, 0)

    def _on_url_extraction_success(self, title, artist):
        root_layout = MDApp.get_running_app().root
        root_layout.refresh_catalog()
        
        lib_screen = root_layout.screen_manager.get_screen("library")
        if lib_screen:
            lib_screen.populate()

        self.results_list.clear_widgets()
        self.online_search_box.opacity = 0
        self.online_search_btn.disabled = True
        
        new_track_index = len(root_layout.songs) - 1
        item = MDListItem(
            MDListItemLeadingIcon(icon="cloud-download"),
            MDListItemHeadlineText(text=title),
            MDListItemSupportingText(text=artist),
            radius=[dp(12)],
            theme_bg_color="Custom",
            md_bg_color=(0.95, 0.95, 0.97, 1),
            on_release=lambda x, idx=new_track_index: self.play_local_result(idx)
        )
        
        self.results_list.add_widget(item)
        self.set_state("results")
