import os
import re
from yt_dlp import YoutubeDL

class SilentLogger:
    def debug(self, msg):
        print(f"[YTDLP DEBUG]: {msg}")
    def warning(self, msg):
        print(f"[YTDLP WARNING]: {msg}")
    def error(self, msg):
        print(f"[YTDLP ERROR]: {msg}")

def sanitize_text(text):
    """Strips out emojis and extended symbols to prevent rendering issues."""
    if not text: return "Unknown"
    clean = re.sub(r'[^\w\s\x20-\x7E]', '', text)
    return re.sub(r'\s+', ' ', clean).strip()

def format_time(seconds):
    """Converts seconds to M:SS format."""
    if not seconds or seconds < 0: return "0:00"
    return f"{int(seconds)//60}:{int(seconds)%60:02d}"

def get_cache_dir():
    from kivy.app import App
    from kivy.utils import platform
    app = App.get_running_app()
    if platform == 'android' and app:
        path = os.path.join(app.user_data_dir, 'cache')
    else:
        path = "cache"
    os.makedirs(path, exist_ok=True)
    return path

def get_thumbnail_path(video_id, cache_dir=None):
    """Returns the thumbnail path if it exists locally, otherwise returns web URL and triggers background download."""
    if cache_dir is None:
        cache_dir = get_cache_dir()
    thumb_path = os.path.join(cache_dir, f"{video_id}.jpg")
    
    if os.path.exists(thumb_path):
        return thumb_path
        
    web_url = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"
    
    # Spawn background thread to permanently download and cache the artwork for future sessions
    import threading
    def _download_art():
        try:
            import urllib.request
            urllib.request.urlretrieve(web_url, thumb_path)
        except:
            pass
            
    threading.Thread(target=_download_art, daemon=True).start()
    return web_url

def extract_video_id(url):
    """Extracts the YouTube video ID from a given URL."""
    if "v=" in url: return url.split("v=")[-1].split("&")[0]
    if "youtu.be/" in url: return url.split("youtu.be/")[-1].split("?")[0]
    raise ValueError("Unsupported YouTube link architecture")

def fetch_youtube_metadata(query_or_url, extract_flat=False):
    """Fetches metadata atomically."""
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'logger': SilentLogger(),
        'socket_timeout': 10,
        'extract_flat': extract_flat
    }
    with YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query_or_url, download=False)
