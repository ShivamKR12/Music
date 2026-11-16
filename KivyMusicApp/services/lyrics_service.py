import os
import re
import json
import threading
import urllib.parse
import urllib.request
from kivy.clock import Clock

class LyricsResult(str):
    """
    Subclass of str providing backward-compatible string usage while attaching
    structured plain and synced lyric texts.
    """
    def __new__(cls, plain: str = "", synced: str = ""):
        text = plain if plain else (synced or "")
        obj = super().__new__(cls, text)
        obj.plain = plain or ""
        obj.synced = synced or ""
        return obj

def strip_lrc_tags(lrc_text: str) -> str:
    """Strips [mm:ss.xx] timestamp tags from LRC lyrics to produce clean plain text."""
    if not lrc_text:
        return ""
    time_tag_pattern = re.compile(r'\[\d{1,2}:\d{1,2}(?:\.\d{1,3})?\]')
    lines = [time_tag_pattern.sub('', line).strip() for line in lrc_text.splitlines()]
    return '\n'.join([l for l in lines if l])

def parse_lrc(lrc_text: str):
    """
    Parses LRC-formatted text into a sorted list of (seconds: float, text: str) tuples.
    Supports single or multiple timestamp prefixes per line: [00:12.34][00:45.67] text.
    """
    if not lrc_text:
        return []
    time_tag_pattern = re.compile(r'\[(\d{1,2}):(\d{1,2}(?:\.\d{1,3})?)\]')
    parsed_lines = []
    for raw_line in lrc_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        matches = list(time_tag_pattern.finditer(line))
        if not matches:
            continue
        text = time_tag_pattern.sub('', line).strip()
        for m in matches:
            minutes = int(m.group(1))
            seconds = float(m.group(2))
            total_sec = minutes * 60.0 + seconds
            parsed_lines.append((total_sec, text))
    parsed_lines.sort(key=lambda x: x[0])
    return parsed_lines

def find_active_line_index(parsed_lines, elapsed: float) -> int:
    """
    Returns the 0-based index of the lyric line currently being sung given elapsed seconds.
    Returns 0 if before first timestamp, or -1 if parsed_lines is empty.
    """
    if not parsed_lines:
        return -1
    if elapsed < parsed_lines[0][0]:
        return 0
    active_idx = 0
    for idx, (t, _) in enumerate(parsed_lines):
        if elapsed >= t:
            active_idx = idx
        else:
            break
    return active_idx

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

def get_cached_lyrics(video_id: str, cache_dir: str = None):
    """Retrieves cached lyrics text from disk if available."""
    if not video_id:
        return None
    if cache_dir is None:
        cache_dir = get_cache_dir()
    lpath = os.path.join(cache_dir, f"{video_id}_lyrics.txt")
    spath = os.path.join(cache_dir, f"{video_id}_synced.lrc")

    plain = ""
    synced = ""
    if os.path.exists(lpath) and os.path.isfile(lpath):
        try:
            with open(lpath, 'r', encoding='utf-8') as f:
                plain = f.read().strip()
        except Exception:
            pass

    if os.path.exists(spath) and os.path.isfile(spath):
        try:
            with open(spath, 'r', encoding='utf-8') as f:
                synced = f.read().strip()
        except Exception:
            pass

    if plain or synced:
        return LyricsResult(plain=plain or strip_lrc_tags(synced), synced=synced)
    return None

def save_cached_lyrics(video_id: str, lyrics_text: str, synced_text: str = None, cache_dir: str = None):
    """Persists plain and synced lyrics text to disk for offline access."""
    if not video_id:
        return
    if cache_dir is None:
        cache_dir = get_cache_dir()
    if lyrics_text:
        lpath = os.path.join(cache_dir, f"{video_id}_lyrics.txt")
        try:
            with open(lpath, 'w', encoding='utf-8') as f:
                f.write(lyrics_text)
        except Exception as e:
            print(f"[LyricsService] Failed to cache plain lyrics: {e}")

    if synced_text:
        spath = os.path.join(cache_dir, f"{video_id}_synced.lrc")
        try:
            with open(spath, 'w', encoding='utf-8') as f:
                f.write(synced_text)
        except Exception as e:
            print(f"[LyricsService] Failed to cache synced lyrics: {e}")

def fetch_lyrics_sync(title: str, artist: str = "", video_id: str = None, cache_dir: str = None, local_path: str = None):
    """
    Synchronously fetches multi-language lyrics:
    1. Checks local sidecar .lrc file alongside offline track if local_path exists.
    2. Checks persistent cache on disk.
    3. Queries LRCLIB public API (supports multilingual plain & synced lyrics).
    4. Fallback queries Lyrics.ovh for romanized/international tracks.
    5. Caches retrieved lyrics and returns LyricsResult.
    """
    # 1. Check local sidecar .lrc file for offline audio
    if local_path and os.path.exists(local_path):
        base, _ = os.path.splitext(local_path)
        lrc_path = f"{base}.lrc"
        if os.path.exists(lrc_path) and os.path.isfile(lrc_path):
            try:
                with open(lrc_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().strip()
                    if len(content) > 10:
                        return LyricsResult(plain=strip_lrc_tags(content), synced=content)
            except Exception:
                pass

    # 2. Check local persistent cache
    if video_id:
        cached = get_cached_lyrics(video_id, cache_dir)
        if cached:
            return cached

    clean_t = clean_song_title(title)
    clean_a = re.sub(r'(?i)\b(feat\.?|ft\.?)\b.*', '', artist).strip() if artist else ""

    queries = []
    if clean_t and clean_a:
        queries.append(f"{clean_t} {clean_a}".strip())
    if clean_t:
        queries.append(clean_t)
    if title and title != clean_t:
        queries.append(title)

    # 3. Query LRCLIB (supports multi-language: English, Hindi, Punjabi, Spanish, Japanese, etc.)
    for q in queries:
        try:
            url = f"https://lrclib.net/api/search?q={urllib.parse.quote(q)}"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) KivyMusicApp/2.0"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if isinstance(data, list) and len(data) > 0:
                    for item in data:
                        synced = (item.get("syncedLyrics") or "").strip()
                        plain = (item.get("plainLyrics") or "").strip()
                        if (synced and len(synced) > 20) or (plain and len(plain) > 20):
                            if not plain and synced:
                                plain = strip_lrc_tags(synced)
                            if video_id:
                                save_cached_lyrics(video_id, plain, synced, cache_dir)
                            return LyricsResult(plain=plain, synced=synced)
        except Exception:
            continue

    # 4. Fallback to Lyrics.ovh for romanized / international tracks
    if clean_t and clean_a:
        try:
            url_ovh = f"https://api.lyrics.ovh/v1/{urllib.parse.quote(clean_a)}/{urllib.parse.quote(clean_t)}"
            req_ovh = urllib.request.Request(
                url_ovh,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) KivyMusicApp/2.0"}
            )
            with urllib.request.urlopen(req_ovh, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                lyrics_ovh = (data.get("lyrics") or "").strip()
                if lyrics_ovh and len(lyrics_ovh) > 20:
                    if video_id:
                        save_cached_lyrics(video_id, lyrics_ovh, None, cache_dir)
                    return LyricsResult(plain=lyrics_ovh, synced="")
        except Exception:
            pass

    return LyricsResult(plain="No lyrics found for this track.", synced="")

def fetch_lyrics_async(title: str, artist: str = "", video_id: str = None, cache_dir: str = None, on_success=None, local_path: str = None):
    """
    Asynchronously fetches multi-language lyrics in a background thread and dispatches
    the result safely onto the Kivy main thread.
    """
    def _worker():
        lyrics = fetch_lyrics_sync(title, artist, video_id, cache_dir, local_path)
        if on_success:
            Clock.schedule_once(lambda dt: on_success(lyrics), 0)

    threading.Thread(target=_worker, daemon=True).start()
