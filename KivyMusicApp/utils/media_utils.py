import os
import re
import socket
import threading
import urllib.request
from yt_dlp import YoutubeDL

class SilentLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): print(f"[YTDLP ERROR]: {msg}")

def sanitize_text(text):
    """Strips out emojis and extended non-ASCII symbols to prevent font rendering bugs."""
    if not text:
        return "Unknown"
    clean = re.sub(r'[^\w\s\x20-\x7E]', '', str(text))
    return re.sub(r'\s+', ' ', clean).strip() or "Unknown"

def format_time(seconds):
    """Converts seconds into M:SS formatted string."""
    if not seconds or seconds < 0:
        return "0:00"
    m, s = divmod(int(seconds), 60)
    return f"{m}:{s:02d}"

def get_cache_dir():
    """Returns absolute path to local cache folder (per-platform)."""
    from kivy.app import App
    from kivy.utils import platform
    app = App.get_running_app()
    if platform == 'android' and app:
        path = os.path.join(app.user_data_dir, 'cache')
    else:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache')
    os.makedirs(path, exist_ok=True)
    return path

def extract_video_id(url):
    """Extracts YouTube video ID from various URL architectures or 11-character strings."""
    if not url:
        return ""
    if len(url) == 11 and not ("/" in url or "=" in url):
        return url
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    cleaned = re.sub(r'[^a-zA-Z0-9_-]', '', str(url))
    return cleaned[:11] if cleaned else "unknown"

def download_artwork(video_id, custom_url=None, cache_dir=None, on_success=None):
    """
    Downloads artwork for a video ID or from custom_url to local cache/{video_id}.jpg.
    Tries multiple candidate URLs (custom URL, hqdefault, mqdefault, default).
    If file already exists on disk, invokes on_success immediately.
    Otherwise spawns a daemon thread to download, persist, update SQLite DB, and trigger on_success.
    """
    if not video_id or str(video_id).startswith("loc_") or str(video_id).startswith("local_"):
        return "album_art.png"
    if cache_dir is None:
        cache_dir = get_cache_dir()

    thumb_path = os.path.join(cache_dir, f"{video_id}.jpg")
    if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 0:
        if on_success:
            try:
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: on_success(thumb_path), 0)
            except Exception:
                on_success(thumb_path)
        return thumb_path

    # Candidate URLs to attempt in order of resolution quality
    candidates = []
    if custom_url and custom_url.startswith("http"):
        candidates.append(custom_url)
    candidates.extend([
        f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
        f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg",
        f"https://i.ytimg.com/vi/{video_id}/default.jpg",
    ])

    def _worker():
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        for url in candidates:
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
                    if resp.status == 200:
                        content = resp.read()
                        if len(content) > 500:  # Valid image payload
                            with open(thumb_path, 'wb') as out_f:
                                out_f.write(content)
                            break
            except Exception:
                continue

        if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 0:
            # Update SQLite database if track exists
            try:
                from models.database import update_track_artwork
                update_track_artwork(video_id, thumb_path)
            except Exception:
                pass

            if on_success:
                try:
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: on_success(thumb_path), 0)
                except Exception:
                    on_success(thumb_path)

    threading.Thread(target=_worker, daemon=True).start()
    return candidates[0] if candidates else "album_art.png"

def get_thumbnail_path(video_id, cache_dir=None, custom_url=None, on_success=None):
    """
    Returns the local thumbnail path if it exists on disk.
    Otherwise returns best web URL and triggers download_artwork in the background.
    """
    return download_artwork(video_id, custom_url=custom_url, cache_dir=cache_dir, on_success=on_success)

def ensure_artworks_downloaded(tracks, on_track_updated=None, cache_dir=None):
    """
    Asynchronously checks and downloads album artwork for all provided tracks.
    Invokes on_track_updated(track, local_art_path) on main thread as each item finishes.
    """
    if not tracks:
        return
    if cache_dir is None:
        cache_dir = get_cache_dir()

    def _batch_worker():
        for t in list(tracks):
            vid = getattr(t, "video_id", None) or (t.get("video_id") if isinstance(t, dict) else None)
            if not vid or str(vid).startswith("loc_") or str(vid).startswith("local_"):
                continue
            thumb_path = os.path.join(cache_dir, f"{vid}.jpg")
            if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 0:
                if hasattr(t, "album_art") and t.album_art != thumb_path:
                    t.album_art = thumb_path
                continue

            # Need to download
            custom_art = getattr(t, "album_art", "") or (t.get("artwork") if isinstance(t, dict) else "")
            custom_url = custom_art if (custom_art and custom_art.startswith("http")) else None

            def _success(local_path, trk=t):
                if hasattr(trk, "album_art"):
                    trk.album_art = local_path
                if on_track_updated:
                    on_track_updated(trk, local_path)

            download_artwork(vid, custom_url=custom_url, cache_dir=cache_dir, on_success=_success)

    threading.Thread(target=_batch_worker, daemon=True).start()

def fetch_youtube_metadata(query_or_url, extract_flat=False):
    """
    Fetches video metadata or search results via yt-dlp atomically without downloading audio.
    Employs robust multi-client fallbacks to avoid YouTube 'content not available' restrictions.
    """
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'logger': SilentLogger(),
        'socket_timeout': 15,
        'nocheckcertificate': True,
        'extract_flat': extract_flat,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web', 'mweb'],
            }
        },
    }
    with YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query_or_url, download=False)

def enforce_max_cache_size(cache_dir=None, max_size_mb=5000):
    """
    Audits local cache folder footprint and evicts oldest media assets
    (sorted by last-modified timestamp) if the folder exceeds max_size_mb.
    """
    if cache_dir is None:
        cache_dir = get_cache_dir()

    if not os.path.exists(cache_dir):
        return

    try:
        files = []
        total_size = 0
        for entry in os.scandir(cache_dir):
            if entry.is_file():
                stat = entry.stat()
                files.append((stat.st_mtime, stat.st_size, entry.path))
                total_size += stat.st_size

        max_bytes = int(max_size_mb * 1024 * 1024)
        if total_size <= max_bytes:
            return

        files.sort(key=lambda x: x[0])
        print(f"[CacheManager] Cache limit exceeded ({total_size / 1024 / 1024:.2f} MB > {max_size_mb} MB). Evicting older entries...")
        for _, size, path in files:
            if total_size <= max_bytes:
                break
            try:
                os.remove(path)
                total_size -= size
                print(f"[CacheManager] Evicted item: {path}")
            except Exception as e:
                print(f"[CacheManager] Failed to evict {path}: {e}")
    except Exception as e:
        print(f"[CacheManager] General cache eviction check error: {e}")
