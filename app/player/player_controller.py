import threading
from kivy.clock import Clock


class PlayerController:
    def __init__(self, engine, db, downloader, cache):
        self.engine = engine
        self.db = db
        self.downloader = downloader
        self.cache = cache

    # -------------------------
    # LOCAL / GENERIC PLAY
    # -------------------------
    def play_song(self, song, on_started=None):
        self.engine.play(song.file_path, song.duration)
        self.db.mark_played(song.id)

        if on_started:
            on_started(song)

    # -------------------------
    # YOUTUBE PLAY
    # -------------------------
    def play_youtube(self, url, on_status=None, on_started=None):
        def task():
            try:
                if on_status:
                    Clock.schedule_once(lambda dt: on_status("Fetching..."))

                song = self.downloader.fetch_song(url)

                Clock.schedule_once(
                    lambda dt: self._store_and_play(song, on_status, on_started)
                )

            except Exception as e:
                if on_status:
                    Clock.schedule_once(lambda dt: on_status(str(e)))

        threading.Thread(target=task, daemon=True).start()

    def _store_and_play(self, song, on_status, on_started):
        self.db.add_song(song)
        self.play_song(song, on_started)

        if on_status:
            on_status(f"Playing: {song.title}")
