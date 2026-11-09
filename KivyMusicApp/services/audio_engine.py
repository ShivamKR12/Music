import os
import re
import time
import json
import socket
import threading
import urllib.request
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from yt_dlp import YoutubeDL

class SilentLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): print(f"[YTDLP ERROR]: {msg}")

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

def extract_video_id(url):
    """Extract YouTube video ID or return string if already an 11-char ID."""
    if not url:
        return ""
    if len(url) == 11 and not ("/" in url or "=" in url):
        return url
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    # Fallback: clean alphanumeric
    cleaned = re.sub(r'[^a-zA-Z0-9_-]', '', url)
    return cleaned[:11] if cleaned else "unknown"

class AudioEngine:
    """
    Asynchronous, non-blocking audio streaming and playback engine.
    Integrates yt-dlp downloading/caching with Kivy's SoundLoader (SDL2 backend).
    All UI state notifications are dispatched safely onto the Kivy Main Thread.
    """
    def __init__(self):
        self.player = None
        self.elapsed = 0.0
        self.duration = 0.0
        self.last_tick = None
        self.paused = False
        self.loading = False
        self.current_info = None
        self.current_path = None
        self.repeat_one = False

        # Decoupled UI Callbacks
        self.on_time_update = None       # callback(elapsed, duration)
        self.on_track_end = None         # callback()
        self.on_artwork_loaded = None    # callback(artwork_path)
        self.on_loading = None           # callback(is_loading)
        self.on_download_progress = None # callback(percent_str)
        self.on_error = None             # callback(error_msg)

        self.lock = threading.Lock()
        self.cancel_event = threading.Event()

    def start_play(self, url_or_path: str, track_info=None):
        """Initiate playback for a local file or remote YouTube track."""
        if not url_or_path:
            return False

        # If it's an existing local audio file, play immediately on main thread
        if os.path.exists(url_or_path) and os.path.isfile(url_or_path):
            info = track_info or {"title": os.path.basename(url_or_path), "duration": 0}
            self.cleanup_player()
            self._play_file(url_or_path, info)
            return True

        # Otherwise treat as online stream/video ID and process in background thread
        with self.lock:
            self.cancel_event.set()
            self.cleanup_player()
            self.loading = True
            self.cancel_event = threading.Event()
            current_cancel = self.cancel_event

        threading.Thread(
            target=self._download_and_play,
            args=(url_or_path, current_cancel, track_info),
            daemon=True
        ).start()
        return True

    def cleanup_player(self):
        Clock.unschedule(self._update)
        if self.player:
            try:
                self.player.stop()
                self.player.unload()
            except Exception:
                pass
        self.player = None
        self.elapsed = 0.0
        self.duration = 0.0
        self.last_tick = None
        self.paused = False

    def _set_loading(self, state: bool):
        self.loading = state
        if self.on_loading:
            self.on_loading(state)

    def _download_and_play(self, target: str, cancel_event: threading.Event, user_info=None):
        try:
            Clock.schedule_once(lambda dt: self._set_loading(True), 0)
            video_id = extract_video_id(target)
            cache_dir = get_cache_dir()
            mp3_path = os.path.join(cache_dir, f"{video_id}.mp3")
            meta_path = os.path.join(cache_dir, f"{video_id}.json")

            # 1. Cache hit check
            if os.path.exists(mp3_path):
                cached_meta = self._load_cached_metadata(meta_path) or {}
                if user_info:
                    cached_meta.update(user_info)
                if cancel_event.is_set():
                    return

                Clock.schedule_once(lambda dt: self._set_main_thread_info(cached_meta, mp3_path), 0)
                if cached_meta.get("artwork") and os.path.exists(cached_meta["artwork"]) and self.on_artwork_loaded:
                    Clock.schedule_once(lambda dt: self.on_artwork_loaded(cached_meta["artwork"]), 0)

                Clock.schedule_once(lambda dt: self._play_file(mp3_path, cached_meta), 0)
                Clock.schedule_once(lambda dt: self._set_loading(False), 0)
                return

            if cancel_event.is_set():
                return

            # 2. Setup download hooks and yt-dlp configuration
            def download_hook(d):
                if cancel_event.is_set():
                    raise InterruptedError("Playback cancelled")
                if d.get('status') == 'downloading' and self.on_download_progress:
                    raw_p = d.get('_percent_str', '')
                    clean_p = re.sub(r'\x1b\[[0-9;]*m', '', raw_p).strip()
                    if clean_p:
                        Clock.schedule_once(lambda dt, p=clean_p: self.on_download_progress(p), 0)

            full_url = target if ("youtube.com" in target or "youtu.be" in target) else f"https://www.youtube.com/watch?v={video_id}"
            out_tmpl = os.path.join(cache_dir, f"{video_id}.%(ext)s")

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': out_tmpl,
                'quiet': True,
                'noplaylist': True,
                'logger': SilentLogger(),
                'socket_timeout': 15,
                'nocheckcertificate': True,
                'continuedl': True,
                'retries': 3,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web', 'mweb'],
                    }
                },
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '128',
                }],
                'progress_hooks': [download_hook],
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(full_url, download=False)
                if cancel_event.is_set():
                    return

                clean_info = {
                    "id": video_id,
                    "title": info.get("title", user_info.get("title", "Unknown") if user_info else "Unknown"),
                    "artist": info.get("uploader", user_info.get("artist", "") if user_info else ""),
                    "duration": int(info.get("duration", 0) or (user_info.get("duration", 0) if user_info else 0)),
                    "artwork": ""
                }

                thumb_url = info.get("thumbnail")
                thumb_path = os.path.join(cache_dir, f"{video_id}.jpg")
                if thumb_url and not os.path.exists(thumb_path):
                    self._download_thumbnail(thumb_url, thumb_path)
                if os.path.exists(thumb_path):
                    clean_info["artwork"] = thumb_path

                if cancel_event.is_set():
                    return

                # Push metadata and artwork to UI immediately
                Clock.schedule_once(lambda dt: self._set_main_thread_info(clean_info, mp3_path), 0)
                if clean_info.get("artwork") and self.on_artwork_loaded:
                    Clock.schedule_once(lambda dt: self.on_artwork_loaded(clean_info["artwork"]), 0)

                # Process download & ffmpeg conversion
                ydl.process_ie_result(info, download=True)

            if cancel_event.is_set():
                return

            if os.path.exists(mp3_path):
                self._save_cached_metadata(meta_path, clean_info)
                Clock.schedule_once(lambda dt: self._play_file(mp3_path, clean_info), 0)

            Clock.schedule_once(lambda dt: self._set_loading(False), 0)

        except InterruptedError:
            pass
        except Exception as e:
            if not cancel_event.is_set():
                print(f"[AudioEngine Error]: {e}")
                if self.on_error:
                    err_str = str(e)
                    Clock.schedule_once(lambda dt: self.on_error(err_str), 0)
            Clock.schedule_once(lambda dt: self._set_loading(False), 0)
        finally:
            with self.lock:
                if not cancel_event.is_set():
                    Clock.schedule_once(lambda dt: self._set_loading(False), 0)

    def _set_main_thread_info(self, info, path):
        self.current_info = info
        self.current_path = path

    def _play_file(self, path: str, info: dict):
        self.cleanup_player()
        if not os.path.exists(path):
            return

        self.player = SoundLoader.load(path)
        if self.player:
            self.player.play()
            file_len = getattr(self.player, 'length', 0)
            meta_len = info.get("duration", 0) if info else 0
            self.duration = meta_len if meta_len > 0 else (file_len if file_len > 0 else 180)
            self.elapsed = 0.0
            self.last_tick = time.time()
            self.paused = False

            artwork = info.get("artwork") if info else None
            if artwork and os.path.exists(artwork) and self.on_artwork_loaded:
                Clock.schedule_once(lambda dt: self.on_artwork_loaded(artwork), 0)

            Clock.schedule_interval(self._update, 0.1)

    def _update(self, dt):
        if not self.player:
            return False

        now = time.time()
        if self.last_tick is None:
            self.last_tick = now
            return True

        dt_real = now - self.last_tick
        self.last_tick = now

        if not self.paused:
            pos = getattr(self.player, 'get_pos', lambda: None)()
            if pos is not None and pos > 0:
                self.elapsed = pos
            else:
                self.elapsed += dt_real

        if self.on_time_update:
            self.on_time_update(self.elapsed, self.duration)

        # Track end detection
        if self.player.state == 'stop' and not self.paused and self.elapsed > 1.0:
            return self._end_track()
        if self.duration > 0 and self.elapsed >= self.duration:
            return self._end_track()

        return True

    def pause(self):
        if not self.player:
            return
        self.paused = True
        try:
            self.player.stop()
        except Exception:
            pass

    def unpause(self):
        if not self.player:
            return
        self.paused = False
        self.last_tick = time.time()
        try:
            self.player.play()
            Clock.schedule_once(lambda dt: self._safe_seek(self.elapsed), 0.05)
        except Exception:
            pass

    def seek(self, target_pos: float):
        if not self.player:
            return
        self.elapsed = max(0.0, min(target_pos, self.duration if self.duration > 0 else target_pos))
        self._safe_seek(self.elapsed)

    def _safe_seek(self, pos: float):
        if hasattr(self.player, 'seek'):
            try:
                self.player.seek(pos)
            except TypeError:
                try:
                    self.player.seek(pos, relative=False)
                except Exception:
                    pass

    def _end_track(self):
        if self.repeat_one and self.player:
            try:
                self.elapsed = 0.0
                self.last_tick = time.time()
                self.player.seek(0)
                self.player.play()
                if self.on_time_update:
                    self.on_time_update(0.0, self.duration)
                return True
            except Exception:
                pass

        self.cleanup_player()
        if self.on_track_end:
            self.on_track_end()
        return False

    def _save_cached_metadata(self, meta_path: str, info: dict):
        try:
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(info, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _load_cached_metadata(self, meta_path: str):
        if not os.path.exists(meta_path):
            return None
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def _download_thumbnail(self, url: str, path: str):
        try:
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            socket.setdefaulttimeout(10)
            with urllib.request.urlopen(url, context=ctx) as resp, open(path, 'wb') as out_f:
                out_f.write(resp.read())
        except Exception:
            pass
