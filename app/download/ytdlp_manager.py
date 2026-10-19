# download/ytdlp_manager.py

import os
from yt_dlp import YoutubeDL
from library.metadata import Song


class SilentLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass


class YTDLPManager:
    def __init__(self, cache_dir="cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def fetch(self, url):
        """
        Returns: (file_path, title, duration)
        Downloads only if missing.
        """
        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'noplaylist': True,
            'logger': SilentLogger(),
            'outtmpl': f'{self.cache_dir}/%(id)s_%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            file_path = ydl.prepare_filename(info)
            file_path = os.path.splitext(file_path)[0] + ".opus"

            if not os.path.exists(file_path):
                info = ydl.extract_info(url, download=True)

        return file_path, info.get("title", "Unknown"), info.get("duration", 0)
    
    def fetch_song(self, url):
        file_path, title, duration = self.fetch(url)

        song = Song(
            title=title,
            duration=duration,
            source="youtube",
            file_path=file_path
        )
        return song
