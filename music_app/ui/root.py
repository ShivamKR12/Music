import os
import threading
import random
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from config import LIGHT_THEME
from audio import AudioEngine
from ui.components import MiniPlayerBar, BottomNavBar
from models.database import get_all_tracks, update_local_track_path, add_track, mark_track_played
from utils import get_thumbnail_path, extract_video_id, fetch_youtube_metadata

class RootLayout(MDBoxLayout):
    screen_manager = ObjectProperty(None)
    mini_player = ObjectProperty(None)
    current_title = ObjectProperty(None)
    current_artist = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        with self.canvas.before:
            Color(*LIGHT_THEME["bg"])
            self.bg = Rectangle()
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        self.screen_manager = MDScreenManager(transition=SlideTransition(direction="up", duration=0.35))
        self.add_widget(self.screen_manager)
        
        self.mini_player_wrapper = MDBoxLayout(size_hint_y=None, height=0, opacity=0, padding=[dp(16), 0])
        self.mini_player_wrapper.disabled = True
        self.mini_player = MiniPlayerBar(self)
        self.mini_player_wrapper.add_widget(self.mini_player)
        self.add_widget(self.mini_player_wrapper)
        
        self.navigation_spacer = Widget(size_hint_y=None, height=dp(12))
        self.add_widget(self.navigation_spacer)
        
        self.bottom_navigation_wrapper = MDBoxLayout(size_hint_y=None, height=dp(64), padding=[dp(16), 0])
        self.bottom_nav = BottomNavBar(self)
        self.bottom_navigation_wrapper.add_widget(self.bottom_nav)
        self.add_widget(self.bottom_navigation_wrapper)
        
        # Load Centralized Catalog Data dynamically from your SQLite store
        self.refresh_catalog()
        
        # Thread Decoupled Engine Instantiation
        self.audio = AudioEngine()
        self.audio.on_time_update = self._on_audio_time
        self.audio.on_track_end = self.next_song
        self.audio.on_artwork_loaded = self._on_artwork_received  # Thread safe callback bridge hook
        self.audio.on_error = self.show_error
        self.audio.on_loading = self._on_loading_state
        self.audio.on_download_progress = self._on_download_progress
        
        self.is_playing = False
        self.shuffle_enabled = False
        self.repeat_mode = "off"
        
        # Explicitly initialize the component layout state right on app launch
        Clock.schedule_once(lambda dt: self.sync_initial_player_state(), 0)
        
        # Dynamically fetch trending songs if library only has our short test tracks
        if len(self.songs) == 0:
            print("[THREAD START] RootLayout._fetch_trending_tracks")
            threading.Thread(target=self._fetch_trending_tracks, daemon=True).start()
            
        # Enforce cache limits asynchronously
        from config import enforce_max_cache_size
        threading.Thread(target=enforce_max_cache_size, kwargs={"max_size_mb": 5000}, daemon=True).start()

    def _on_loading_state(self, is_loading):
        self.mini_player.update_loading_state(is_loading)
        now_screen = self.screen_manager.get_screen("now_playing")
        if now_screen:
            now_screen.update_loading_state(is_loading)
            
        # Restore the original artist label once loading is finished
        if not is_loading and self.current_artist:
            self.mini_player.artist_label.text = self.current_artist
            if now_screen:
                now_screen.artist_label.text = self.current_artist
            
    def _on_download_progress(self, percent_str):
        display_text = f"{self.current_artist} (Downloading... {percent_str})" if self.current_artist else f"Downloading... {percent_str}"
        self.mini_player.artist_label.text = display_text
        now_screen = self.screen_manager.get_screen("now_playing")
        if now_screen:
            now_screen.artist_label.text = display_text
    
    def _set_global_song_info(self, title, artist, animate=False):
        self.current_title = title
        self.current_artist = artist
        self.mini_player.update_song(title, artist)
        now_screen = self.screen_manager.get_screen("now_playing")
        if now_screen:
            if animate:
                now_screen.animate_song_change(title, artist)
            else:
                now_screen.title_label.text = title
                now_screen.artist_label.text = artist

        idx = self.current_song_index
        if idx is not None and idx < len(self.songs):
            video_id = self.songs[idx][3]
            from models.database import is_favorite
            is_fav = is_favorite(video_id)
            self.mini_player.update_favorite_state(is_fav)
            if hasattr(now_screen, 'update_favorite_state'):
                now_screen.update_favorite_state(is_fav)
    
    def _set_global_artwork(self, thumb_path):
        self.mini_player.set_artwork(thumb_path)
        now_screen = self.screen_manager.get_screen("now_playing")
        if now_screen:
            now_screen.artwork.set_artwork(thumb_path)

    def sync_initial_player_state(self):
        """Passively configures interface labels to mirror initial data bounds."""
        idx = self.current_song_index
        if idx is not None and idx < len(self.songs):
            title, artist, url, video_id = self.songs[idx]
            self._set_global_song_info(title, artist, animate=False)
            
            self._set_global_artwork(get_thumbnail_path(video_id))

    def refresh_catalog(self):
        """Reloads active dataset tracking arrays directly from SQLite storage layers."""
        raw_tracks = get_all_tracks()
        # Preserve video_id at index position 3 inside your central memory cache array
        self.songs = [(t[0], t[1], t[2], t[3]) for t in raw_tracks]
        
        # Keep tracking lookup definitions indexed for sub-component access
        self.queue = list(range(len(self.songs)))
        self.user_ordered_queue = self.queue.copy()
        
        if not hasattr(self, 'queue_index'):
            self.queue_index = None

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def show_mini_player(self):
        self.mini_player_wrapper.disabled = False
        Animation(opacity=1, height=dp(72), duration=0.18).start(self.mini_player_wrapper)

    def hide_mini_player(self):
        self.mini_player_wrapper.disabled = True
        Animation(opacity=0, height=0, duration=0.18).start(self.mini_player_wrapper)

    def go_back(self):
        target = getattr(self, 'previous_screen', 'library')
        self.go_to(target)

    def go_to(self, screen_name):
        if not self.screen_manager.has_screen(screen_name):
            print(f"[UI WARN] Navigation ignored: Screen '{screen_name}' is not yet implemented.")
            return
            
        current = self.screen_manager.current
        if current != screen_name and screen_name == "now_playing":
            self.previous_screen = current
            
        hide = (screen_name == "now_playing")
        
        # Bottom nav and spacer follow the screen change
        for w, h in [(self.navigation_spacer, dp(12)), (self.bottom_navigation_wrapper, dp(64))]:
            w.disabled = hide
            Animation(opacity=0 if hide else 1, height=0 if hide else h, duration=0.18).start(w)
            
        if hide:
            self.hide_mini_player()
        else:
            if self.current_song_index is not None:
                self.show_mini_player()
            else:
                self.hide_mini_player()

        self.screen_manager.current = screen_name

    def _set_global_play_state(self, is_playing):
        self.is_playing = is_playing
        self.mini_player.update_play_state(is_playing)
        now_screen = self.screen_manager.get_screen("now_playing")
        if now_screen:
            now_screen.update_play_state(is_playing)
            if is_playing:
                now_screen.artwork.start_breathing()
            else:
                now_screen.artwork.stop_breathing()

    def toggle_play(self):
        if self.audio.loading or not self.queue: return
        if not self.audio.player:
            self.play_current()
            return
            
        new_state = not self.is_playing
        try:
            if new_state:
                self.audio.unpause()
            else:
                self.audio.pause()
        except Exception as e:
            print("Playback transformation failure state:", e)
            new_state = False
        
        self._set_global_play_state(new_state)

    def toggle_shuffle(self):
        if not self.queue: return
        self.shuffle_enabled = not self.shuffle_enabled
        if self.shuffle_enabled:
            current = self.queue[self.queue_index]
            rest = self.user_ordered_queue.copy()
            if current in rest: rest.remove(current)
            random.shuffle(rest)
            self.queue = [current] + rest
            self.queue_index = 0
        else:
            current_song = self.queue[self.queue_index]
            self.queue = self.user_ordered_queue.copy()
            self.queue_index = self.queue.index(current_song)
        self.screen_manager.get_screen("now_playing").update_shuffle_state(self.shuffle_enabled)

    def toggle_repeat(self):
        modes = ["off", "all", "one"]
        self.repeat_mode = modes[(modes.index(self.repeat_mode) + 1) % len(modes)]
        self.audio.repeat_one = (self.repeat_mode == "one")
        self.screen_manager.get_screen("now_playing").update_repeat_state(self.repeat_mode)

    def next_song(self):
        if not self.queue: return
        if self.queue_index is None:
            self.queue_index = 0
            self.play_current()
            return
        if self.repeat_mode == "one":
            self.play_current()
            return
        self.queue_index += 1
        if self.queue_index >= len(self.queue):
            if self.repeat_mode == "all":
                self.queue_index = 0
            else:
                self.queue_index = len(self.queue) - 1
                self._set_global_play_state(False)
                return
        self.play_current()

    def previous_song(self):
        if not self.queue: return
        if self.queue_index is None:
            self.queue_index = 0
            self.play_current()
            return
        self.queue_index -= 1
        if self.queue_index < 0:
            self.queue_index = (len(self.queue) - 1) if self.repeat_mode == "all" else 0
        self.play_current()

    def play_song_at(self, index, rebuild_queue=False):
        if index < 0 or index >= len(self.songs): return
        
        # Prevent ffpyplayer C-thread hard crashes on Windows by skipping reload
        # if the exact same track is already loaded/playing.
        # Also prevents resetting the track to 0:00 if they tap it from the Library!
        if self.current_song_index == index:
            if not self.is_playing:
                self.toggle_play()
            return

        if rebuild_queue:
            self.queue = list(range(len(self.songs)))
            self.user_ordered_queue = self.queue.copy()
            if self.shuffle_enabled:
                rest = self.user_ordered_queue.copy()
                if index in rest: rest.remove(index)
                random.shuffle(rest)
                self.queue = [index] + rest
                
        self.queue_index = self.queue.index(index)
        self.play_current()

    def _on_audio_time(self, elapsed, duration):
        progress = min(max(elapsed / duration, 0), 1) if duration > 0 else 0
        self.mini_player.set_progress(progress)
        
        now_screen = self.screen_manager.get_screen("now_playing")
        if now_screen.seeking: return
        if duration <= 0:
            now_screen.reset_timeline()
            return
        now_screen.update_timeline_state(progress, elapsed, duration)

    def _on_artwork_received(self, thumb_path):
        """Thread-safe UI callback hook assigned to the AudioEngine context."""
        self._set_global_artwork(thumb_path)

    def show_error(self, message):
        print(f"Stream Error: {message}")
        self._set_global_play_state(False)
        now_screen = self.screen_manager.get_screen("now_playing")
        if now_screen:
            now_screen.title_label.text = "Error loading track"
            
        from kivymd.uix.dialog import (
            MDDialog,
            MDDialogHeadlineText,
            MDDialogSupportingText,
            MDDialogButtonContainer
        )
        from kivymd.uix.button import MDButton, MDButtonText
        
        close_btn = MDButton(
            MDButtonText(text="Close"),
            style="text"
        )
        
        dialog = MDDialog(
            MDDialogHeadlineText(text="Playback Error", halign="left"),
            MDDialogSupportingText(text=str(message), halign="left"),
            MDDialogButtonContainer(
                Widget(),
                close_btn,
                spacing="8dp",
            ),
        )
        close_btn.bind(on_release=lambda x: dialog.dismiss())
        dialog.open()

    def play_current(self):
        idx = self.current_song_index
        if idx is None: return
        title, artist, url, video_id = self.songs[idx]
        self._set_global_song_info(title, artist, animate=True)
        
        # Show cached artwork immediately instead of clearing it
        self._set_global_artwork(get_thumbnail_path(video_id))
        
        # Dynamically record track into "Continue Listening" history
        mark_track_played(video_id)

        self.audio.cleanup_player()
        self._on_audio_time(0.0, 0.0)  # Explicitly reset UI timelines while downloading
        if not url: return
        
        # Completely decoupled bridge hook: assignments focus strictly on drawing elements
        self.audio.on_time_update = self._on_audio_time
        
        if self.audio.start_play(url):
            self._set_global_play_state(True)
            
            # Trigger our background metadata database entry once cleanly without loops
            video_id = extract_video_id(url)
            print(f"[THREAD START] RootLayout._async_db_sync for Video ID: {video_id}")
            threading.Thread(target=self._async_db_sync, args=(video_id,), daemon=True).start()

    def _async_db_sync(self, video_id):
        """Updates the local index reference smoothly in the background."""
        try:
            expected_path = self.audio._cache_path_from_id(video_id)
            if os.path.exists(expected_path):
                # Only save database values when file changes actually persist on disk
                update_local_track_path(video_id, expected_path, int(self.audio.duration))
                print(f"[THREAD SUCCESS] RootLayout._async_db_sync completed for Video ID: {video_id}")
            else:
                print(f"[THREAD SKIP] RootLayout._async_db_sync skipped (file missing) for Video ID: {video_id}")
        except Exception as e:
            print("Decoupled storage syncing engine failure pass:", e)
            print(f"[THREAD FAILED] RootLayout._async_db_sync error: {e}")

    def _fetch_trending_tracks(self):
        """Dynamically pulls top trending music on a fresh install."""
        try:
            info = fetch_youtube_metadata("ytsearch10:trending global top music hits", extract_flat=True)
            if 'entries' in info:
                    for entry in info['entries']:
                        video_id = entry.get('id')
                        if video_id:
                            add_track(
                                video_id=video_id,
                                title=entry.get('title', 'Unknown Title'),
                                artist=entry.get('uploader', 'Unknown Artist'),
                                url=entry.get('url', f"https://www.youtube.com/watch?v={video_id}"),
                                duration=int(entry.get('duration') or 0)
                            )
            print("[THREAD SUCCESS] RootLayout._fetch_trending_tracks completed")
            Clock.schedule_once(lambda dt: self._on_trending_fetched(), 0)
        except Exception as e:
            print("Trending fetch failed:", e)
            print(f"[THREAD FAILED] RootLayout._fetch_trending_tracks error: {e}")

    def _on_trending_fetched(self):
        """Main-thread callback to push the fresh trending data to the UI visually."""
        self.refresh_catalog()
        self.sync_initial_player_state()
        if self.screen_manager.has_screen("library"):
            self.screen_manager.get_screen("library").populate()

    @property
    def current_song_index(self):
        if self.queue and self.queue_index is not None and self.queue_index < len(self.queue):
            return self.queue[self.queue_index]
        return None
