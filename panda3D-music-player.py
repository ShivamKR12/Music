# music_player.py

import threading
import queue
import subprocess

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, DirectEntry, OnscreenText

from panda3d.core import AudioSound, loadPrcFileData
from yt_dlp import YoutubeDL


# OPTIONAL: Better audio quality settings
loadPrcFileData("", "audio-library-name p3fmod_audio")  # if FMOD is installed
# Otherwise Panda3D will fall back to p3openal_audio or p3xaudio.


class YouTubeAudioFetcher:
    """Fetches audio stream URLs via yt-dlp (in a thread-safe way)."""

    def __init__(self):
        self.result_queue = queue.Queue()

    def fetch_audio_url_async(self, url):
        thread = threading.Thread(target=self._fetch_audio_thread, args=(url,))
        thread.daemon = True
        thread.start()

    def _fetch_audio_thread(self, url):
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "outtmpl": "temp_audio.%(ext)s",  # download as a temp file
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                filename = filename.rsplit(".", 1)[0] + ".mp3"
                title = info.get("title", "Unknown Title")

            self.result_queue.put((True, filename, title))
        except Exception as e:
            self.result_queue.put((False, str(e), None))


class MusicApp(ShowBase):
    def __init__(self):
        super().__init__()

        self.fetcher = YouTubeAudioFetcher()
        self.sound = None

        self._build_ui()

        # Task to poll results from yt-dlp thread
        self.taskMgr.add(self._poll_audio_fetcher, "PollAudioFetcherTask")

    # -----------------------------
    # UI
    # -----------------------------
    def _build_ui(self):
        OnscreenText(text="YouTube URL:", pos=(-1.2, 0.85), scale=0.07)

        self.url_entry = DirectEntry(
            text="",
            scale=0.06,
            command=self._on_submit_url,
            initialText="https://www.youtube.com/watch?v=CNgPob9hPO4",
            numLines=1,
            focus=0,
            pos=(-0.9, 0, 0.8),
            width=40,
        )

        self.play_button = DirectButton(
            text="Play",
            scale=0.07,
            command=self._on_play_pressed,
            pos=(-0.1, 0, 0.65)
        )

        self.status_text = OnscreenText(
            text="Ready.",
            pos=(-1.2, -0.9),
            scale=0.06,
            mayChange=True
        )

    # -----------------------------
    # Logic
    # -----------------------------
    def _on_submit_url(self, text):
        self._fetch_audio(text)

    def _on_play_pressed(self):
        url = self.url_entry.get()
        self._fetch_audio(url)

    def _fetch_audio(self, url):
        self.status_text.setText("Fetching audio stream URL...")
        self.fetcher.fetch_audio_url_async(url)

    def _poll_audio_fetcher(self, task):
        # Non-blocking check for results
        try:
            success, data, title = self.fetcher.result_queue.get_nowait()
        except queue.Empty:
            return task.cont

        if not success:
            self.status_text.setText(f"Error: {data}")
            return task.cont

        filename = data
        self.status_text.setText(f"Playing: {title}")

        self._play_audio(filename)

        return task.cont

    def _play_audio(self, filename):
        if self.sound:
            self.sound.stop()

        # Panda3D can stream from URL
        self.sound = self.loader.loadSfx(filename)
        self.sound.setLoop(False)
        self.sound.play()


# Run the app
app = MusicApp()
app.run()
