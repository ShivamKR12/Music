import os
import re
import socket
import threading
import urllib.request
from models.db_worker import sanitize_text
from services.logger import get_logger
from services.youtube_extractor import YtdlpLogBridge, SilentLogger

logger = get_logger("MediaUtils")

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

def is_podcast_item(item: dict) -> bool:
    """
    Accurately classifies whether a media item is a podcast or talk content vs a music track.
    Evaluates yt-dlp explicit episodic fields, media types, categories, tags, channel,
    and duration heuristics.
    """
    if not item or not isinstance(item, dict):
        return False

    # 1. Explicit episodic fields (Category 11)
    if any(item.get(k) for k in ('series', 'series_id', 'season', 'season_id', 'episode', 'episode_id', 'episode_number')):
        return True

    # 2. Explicit media_type (Category 1)
    mtype = (item.get('media_type') or '').lower()
    if mtype in ('podcast', 'episode', 'show', 'talk', 'audiobook'):
        return True

    title = str(item.get('title') or '').lower()
    artist = str(item.get('artist') or item.get('uploader') or item.get('channel') or '').lower()
    dur = int(item.get('duration') or 0)
    cats = [str(c).lower() for c in (item.get('categories') or [])]
    tags = [str(t).lower() for t in (item.get('tags') or [])]

    # 3. Known podcast channel or show names (Category 2)
    podcast_channels = (
        'podcast', 'podcasts', 'raj shamani', 'figuring out', 'rich roll', 
        'mel robbins', 'huberman', 'ranveer allahbadia', 'beerbiceps', 
        'joe rogan', 'lex fridman', 'super soul', 'the music podcast', 'ted talks',
        'think with shamani', 'english unleashed', 'akshat gupta'
    )
    if any(ch in artist for ch in podcast_channels) or any(ch in title for ch in ('podcast', 'podcasts', 'beerbiceps', 'ranveer allahbadia', 'raj shamani')):
        return True

    # 4. Keyword patterns in title or tags (Category 1)
    podcast_kw = re.compile(
        r'\b(podcast|podcasts|full episode|episode\s*\d+|ep\.\s*\d+|talk show|interview with|'
        r'exclusive interview|q&a with|fo\s*\d+|fo\d+|deep dive with|conversations with)\b',
        re.IGNORECASE
    )
    if podcast_kw.search(title):
        return True
    if any(podcast_kw.search(t) for t in tags):
        return True

    # 5. Non-music category with long duration (Category 1 & 5)
    if cats and 'music' not in cats:
        if any(c in cats for c in ('podcasts', 'education', 'news & politics', 'people & blogs', 'entertainment')):
            if dur > 600:
                return True

    # 6. Long duration (> 20 min = 1200s) without album/jukebox/mix designation
    if dur > 1200:
        music_mix_kw = re.compile(r'\b(album|jukebox|songs|mashup|nonstop|non-stop|mix|playlist|audio|t-series|speed records|zee music)\b', re.IGNORECASE)
        if not music_mix_kw.search(title):
            return True

    return False

def parse_complete_media_metadata(info: dict) -> dict:
    """
    Extracts and normalizes all available yt-dlp metadata fields into a structured dictionary:
    - Video identification (id, title, description, url, media_type)
    - Channel and creator info (channel, channel_id, uploader)
    - Music and audio metadata (track, artist, album, genre, release_date)
    - Engagement & technical properties (duration, view_count, like_count, chapters)
    - Categorization & tags
    """
    if not info or not isinstance(info, dict):
        return {}
    vid = info.get("id") or info.get("video_id") or ""
    title = info.get("track") or info.get("title") or "Unknown Title"

    # Artist extraction with multi-artist fallback
    artist = info.get("artist")
    if not artist and info.get("artists"):
        artist = ", ".join(info.get("artists"))
    if not artist:
        artist = info.get("uploader") or info.get("channel") or "Unknown Artist"

    album = info.get("album") or ""
    album_artist = info.get("album_artist") or ""
    genre = info.get("genre") or (", ".join(info.get("genres")) if info.get("genres") else "")
    duration = int(info.get("duration") or 0)
    url = info.get("webpage_url") or info.get("url") or (f"https://www.youtube.com/watch?v={vid}" if vid else "")
    thumb = info.get("thumbnail") or ""
    description = info.get("description") or ""
    view_count = int(info.get("view_count") or 0)
    like_count = int(info.get("like_count") or 0)
    channel = info.get("channel") or info.get("uploader") or ""
    channel_id = info.get("channel_id") or info.get("uploader_id") or ""
    release_date = str(info.get("release_date") or info.get("release_year") or info.get("upload_date") or "")
    track_number = int(info.get("track_number") or 0)

    # Chapters handling (JSON serialize if structured list)
    chapters = info.get("chapters")
    chapters_str = ""
    if chapters and isinstance(chapters, list):
        import json
        try:
            chapters_str = json.dumps(chapters)
        except Exception:
            pass

    # Classify media type
    mtype = "podcast" if is_podcast_item(info) else "song"

    return {
        "video_id": vid,
        "source_id": vid,
        "title": title,
        "artist": artist,
        "album": album,
        "album_artist": album_artist,
        "genre": genre,
        "duration": duration,
        "url": url,
        "artwork": thumb,
        "description": description,
        "view_count": view_count,
        "like_count": like_count,
        "channel": channel,
        "channel_id": channel_id,
        "release_date": release_date,
        "chapters": chapters_str,
        "track_number": track_number,
        "media_type": mtype,
        "source": "youtube",
        "bitrate": 128,
    }

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
    Asynchronously checks and downloads album artwork for tracks in a controlled background worker.
    Processes missing artwork politely without saturating system threads or network sockets.
    """
    if not tracks:
        return
    if cache_dir is None:
        cache_dir = get_cache_dir()

    def _batch_worker():
        import time
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
            time.sleep(0.08)  # Polite spacing between downloads

    threading.Thread(target=_batch_worker, daemon=True).start()

def fetch_youtube_metadata(query_or_url, extract_flat=False):
    """
    Fetches video metadata or search results via the centralized YouTubeExtractor
    without downloading audio, preserving lazy yt-dlp import on first network use.
    """
    from services.youtube_extractor import get_youtube_extractor
    return get_youtube_extractor().extract_metadata(query_or_url, extract_flat=extract_flat)

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
        logger.info("Cache limit exceeded (%.2f MB > %s MB). Evicting older entries...", total_size / 1024 / 1024, max_size_mb)
        for _, size, path in files:
            if total_size <= max_bytes:
                break
            try:
                os.remove(path)
                total_size -= size
                logger.debug("Evicted item: %s", path)
            except Exception as e:
                logger.warning("Failed to evict %s: %s", path, e)
    except Exception as e:
        logger.warning("General cache eviction check error: %s", e)

def get_cache_size_mb(cache_dir=None) -> float:
    """Calculates total size of files in cache_dir in Megabytes."""
    if cache_dir is None:
        cache_dir = get_cache_dir()
    if not os.path.exists(cache_dir):
        return 0.0
    total = 0
    try:
        for entry in os.scandir(cache_dir):
            if entry.is_file():
                total += entry.stat().st_size
    except Exception:
        pass
    return total / (1024 * 1024)

def clear_cache_files(cache_dir=None) -> tuple[int, int]:
    """Cleans temporary playback and network cache files while keeping user offline library intact.
    Returns (files_removed, bytes_freed)."""
    if cache_dir is None:
        cache_dir = get_cache_dir()
    if not os.path.exists(cache_dir):
        return (0, 0)
    removed = 0
    bytes_freed = 0
    offline_paths = set()
    try:
        from models.database import get_playlist_tracks
        for t in get_playlist_tracks("Offline Songs"):
            lp = t.get("local_path")
            if lp:
                offline_paths.add(os.path.normcase(os.path.abspath(lp)))
    except Exception:
        pass

    try:
        for entry in os.scandir(cache_dir):
            try:
                if entry.is_file():
                    abs_p = os.path.normcase(os.path.abspath(entry.path))
                    # Protect user's downloaded offline tracks
                    if abs_p in offline_paths:
                        continue
                    size = entry.stat().st_size
                    os.remove(entry.path)
                    removed += 1
                    bytes_freed += size
            except Exception:
                pass
    except Exception:
        pass
    return (removed, bytes_freed)

