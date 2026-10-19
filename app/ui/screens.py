# ui/screens.py

from pathlib import Path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock

from player.audio_engine import AudioEngine
from download.ytdlp_manager import YTDLPManager
from library.database import Database
from download.cache_manager import CacheManager
from library.metadata import Song
from ui.mini_player import MiniPlayer
from player.player_controller import PlayerController
from ui.player_controls import PlayerControls
from ui.import_popup import ImportPopup


class PlayerUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.engine = AudioEngine()
        self.downloader = YTDLPManager()
        self.db = Database()
        self.cache = CacheManager(self.db)
        self.tabs = TabbedPanel(do_default_tab=False)
        self.local_tab = TabbedPanelItem(text="Local")
        self.yt_tab = TabbedPanelItem(text="Online")
        self.controller = PlayerController(self.engine, self.db, self.downloader, self.cache)
        self.tabs.add_widget(self.local_tab)
        self.tabs.add_widget(self.yt_tab)
        self.add_widget(self.tabs)

        Clock.schedule_interval(lambda dt: self.cache.cleanup(), 300)  # every 5 min
        Clock.schedule_interval(lambda dt: self.online_library.refresh(), 300)

        self.player_controls = PlayerControls(engine=self.engine, on_play_pressed=self.start_play)
        self.add_widget(self.player_controls)

        self.mini_player = MiniPlayer(self.engine)
        self.add_widget(self.mini_player)

    def start_play(self, *_):
        url = self.url_input.text.strip()
        if not url:
            self.player_controls.set_status("Enter URL")
            return

        self.player_controls.set_status("Fetching...")
        self.controller.play_youtube(url, on_status=lambda msg: setattr(self.status, 'text', msg), on_started=self._on_song_started)

    def _on_song_started(self, song):
        self.player_controls.set_status(f"Playing: {song.title}")
        self.mini_player.title.text = song.title
    
    def import_local_folder(self):
        popup = ImportPopup(
            self.db,
            on_done=lambda count: self._on_import_done(count)
        )
        popup.open()

    def _on_import_done(self, count):
        self.local_library.refresh()
        self.status.text = f"Imported {count} local songs"
    
    def _fetch_and_play(self, url):
        try:
            song = self.downloader.fetch_song(url)
            Clock.schedule_once(lambda dt: self._store_and_play(song))
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.status, 'text', str(e)))
            return
            
    def _store_and_play(self, song):
        self.db.add_song(song)
        self.online_library.refresh()
        self._play(song)
    
    def _play(self, song):
        self.engine.play(song.file_path, song.duration)
        self.db.mark_played(song.id)
        self.status.text = f"Playing: {song.title}"
        self.mini_player.title.text = song.title
        Clock.schedule_interval(self._update, 0.1)

    def _update(self, dt):
        state = self.engine.update()
        if not self.engine.player:
            return False

        self.progress.max = self.engine.duration or 1
        self.progress.value = min(self.engine.elapsed, self.engine.duration)
        self._update_time()

    def _update_time(self):
        def fmt(s):
            return f"{int(s//60):02}:{int(s%60):02}"
        self.time_label.text = f"{fmt(self.engine.elapsed)} / {fmt(self.engine.duration)}"
    
    def _play_from_library(self, row):
        song = Song(title=row["title"], artist=row["artist"], album=row["album"], duration=row["duration"], source=row["source"], file_path=row["file_path"], artwork_path=row["artwork_path"], song_id=row["id"])

        # self._play(song)
        self.controller.play_song(song)
        self.mini_player.title.text = song.title
