import os
import re
import json
import threading
import urllib.parse
import urllib.request
from kivy.clock import Clock

def get_cache_dir():
    from kivy.app import App
    from kivy.utils import platform
    app = App.get_running_app()
    if platform == 'android' and app:
        path = os.path.join(app.user_data_dir, 'cache')
    else:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache')
    os.makedirs(path, exist_ok=True)
    return path

def clean_song_title(title: str) -> str:
    """Removes common YouTube fluff like (Official Video), [HQ], etc."""
    if not title:
        return ""
    cleaned = re.sub(r'[\(\[\{].*?[\)\]\}]', '', title)
    cleaned = re.sub(r'(?i)\b(official|video|audio|remix|hd|4k|lyric|lyrics|full song)\b', '', cleaned)
    return cleaned.strip()

def get_cached_lyrics(video_id: str, cache_dir: str = None) -> str:
    """Retrieves cached lyrics text from disk if available."""
    if not video_id:
        return ""
    if cache_dir is None:
        cache_dir = get_cache_dir()
    lpath = os.path.join(cache_dir, f"{video_id}_lyrics.txt")
    if os.path.exists(lpath) and os.path.isfile(lpath):
        try:
            with open(lpath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception:
            pass
    return ""

def save_cached_lyrics(video_id: str, lyrics_text: str, cache_dir: str = None):
    """Persists lyrics text to disk for offline access."""
    if not video_id or not lyrics_text:
        return
    if cache_dir is None:
        cache_dir = get_cache_dir()
    lpath = os.path.join(cache_dir, f"{video_id}_lyrics.txt")
    try:
        with open(lpath, 'w', encoding='utf-8') as f:
            f.write(lyrics_text)
    except Exception as e:
        print(f"[LyricsService] Failed to cache lyrics: {e}")

def fetch_lyrics_sync(title: str, artist: str = "", video_id: str = None, cache_dir: str = None) -> str:
    """
    Synchronously fetches lyrics:
    1. Checks local cache first.
    2. Queries LRCLIB public API with fallback search queries.
    3. Caches retrieved lyrics and returns text.
    """
    if video_id:
        cached = get_cached_lyrics(video_id, cache_dir)
        if cached:
            return cached

    clean_t = clean_song_title(title)
    queries = []
    if clean_t and artist:
        queries.append(f"{clean_t} {artist}".strip())
    if clean_t:
        queries.append(clean_t)
    if title and title != clean_t:
        queries.append(title)

    for q in queries:
        try:
            url = f"https://lrclib.net/api/search?q={urllib.parse.quote(q)}"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) KivyMusicApp/2.0"}
            )
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if isinstance(data, list) and len(data) > 0:
                    for item in data:
                        text = item.get("plainLyrics") or item.get("syncedLyrics")
                        if text and len(text.strip()) > 20:
                            clean_lyrics = text.strip()
                            if video_id:
                                save_cached_lyrics(video_id, clean_lyrics, cache_dir)
                            return clean_lyrics
        except Exception as e:
            # Network or timeout, proceed to next query
            continue

    return "No lyrics found for this track."

def fetch_lyrics_async(title: str, artist: str = "", video_id: str = None, cache_dir: str = None, on_success=None):
    """
    Asynchronously fetches lyrics in a background thread and dispatches
    the result safely onto the Kivy main thread.
    """
    def _worker():
        lyrics = fetch_lyrics_sync(title, artist, video_id, cache_dir)
        if on_success:
            Clock.schedule_once(lambda dt: on_success(lyrics), 0)

    threading.Thread(target=_worker, daemon=True).start()
