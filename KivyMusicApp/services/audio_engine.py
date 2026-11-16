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
        self._has_started_playing = False
        self.eq_bands = [0.0] * 10
        self.eq_reverb = False

        # Decoupled UI Callbacks
        self.on_time_update = None       # callback(elapsed, duration)
        self.on_track_end = None         # callback()
        self.on_artwork_loaded = None    # callback(artwork_path)
        self.on_loading = None           # callback(is_loading)
        self.on_download_progress = None # callback(percent_str)
        self.on_error = None             # callback(error_msg)
        self.on_track_loaded = None      # callback(local_path, info)

        self.lock = threading.Lock()
        self.cancel_event = threading.Event()

    def _cache_path_from_id(self, video_id: str):
        """Locate any existing cached audio file for a given video ID."""
        base = os.path.join(get_cache_dir(), video_id)
        for ext in [".mp3", ".wav", ".ogg", ".flac", ".opus", ".webm", ".m4a", ".mp4", ".mkv"]:
            path = base + ext
            if os.path.exists(path) and os.path.isfile(path):
                return path
        return base + ".mp3"

    def start_play(self, url_or_path: str, track_info=None):
        """Initiate playback for a local file or remote YouTube track."""
        if not url_or_path:
            return False

        # 1. If it's an existing local audio file, play immediately on main thread
        if os.path.exists(url_or_path) and os.path.isfile(url_or_path):
            info = track_info or {"title": os.path.basename(url_or_path), "duration": 0}
            self.cleanup_player()
            self._set_main_thread_info(info, url_or_path)
            self._play_file(url_or_path, info)
            return True

        # 2. Check if this YouTube track/video ID is already installed/cached in local cache
        video_id = extract_video_id(url_or_path)
        cache_dir = get_cache_dir()
        cached_audio = self._cache_path_from_id(video_id) if video_id else ""
        if cached_audio and os.path.exists(cached_audio) and os.path.isfile(cached_audio):
            meta_path = os.path.join(cache_dir, f"{video_id}.json")
            cached_meta = self._load_cached_metadata(meta_path) or {}
            if track_info:
                cached_meta.update(track_info)
            self.cleanup_player()
            self._set_main_thread_info(cached_meta, cached_audio)
            thumb_path = os.path.join(cache_dir, f"{video_id}.jpg")
            art = cached_meta.get("artwork")
            if not art or not os.path.exists(art):
                if os.path.exists(thumb_path):
                    art = thumb_path
                    cached_meta["artwork"] = art
            if art and os.path.exists(art) and self.on_artwork_loaded:
                Clock.schedule_once(lambda dt: self.on_artwork_loaded(art), 0)
            self._play_file(cached_audio, cached_meta)
            return True

        # 3. Otherwise treat as online stream/video ID and process in background thread
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
            except Exception:
                pass
        self.player = None
        self.elapsed = 0.0
        self.duration = 0.0
        self.last_tick = None
        self.paused = False
        self._has_started_playing = False

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
                try:
                    from models.database import update_local_track_path
                    update_local_track_path(video_id, mp3_path, clean_info.get("duration", 0))
                except Exception:
                    pass
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
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            print(f"[AudioEngine] File not found: {abs_path}")
            return

        self.player = SoundLoader.load(abs_path)
        if self.player:
            self.player.play()
            file_len = getattr(self.player, 'length', 0)
            meta_len = info.get("duration", 0) if info else 0
            if file_len > 0:
                self.duration = file_len
            elif meta_len > 0:
                self.duration = meta_len
            else:
                self.duration = 180
            if info:
                info["duration"] = int(self.duration)
            self.elapsed = 0.0
            self.last_tick = None
            self.paused = False
            self._has_started_playing = False

            artwork = info.get("artwork") if info else None
            if artwork and os.path.exists(artwork) and self.on_artwork_loaded:
                Clock.schedule_once(lambda dt: self.on_artwork_loaded(artwork), 0)

            if self.on_track_loaded:
                Clock.schedule_once(lambda dt: self.on_track_loaded(abs_path, info), 0)

            Clock.schedule_interval(self._update, 0.1)
        else:
            print(f"[AudioEngine] SoundLoader failed to load: {abs_path}")
            if self.on_error:
                Clock.schedule_once(lambda dt: self.on_error(f"Failed to load audio: {os.path.basename(abs_path)}"), 0)

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

            if not getattr(self, '_has_started_playing', False):
                self._has_started_playing = True

            if getattr(self, '_has_started_playing', False):
                self.elapsed += dt_real
                # Dynamically sync exact duration from decoder if length resolved after first frames
                flen = getattr(self.player, 'length', 0)
                if flen > 0 and abs(self.duration - flen) > 1.0:
                    self.duration = flen
                # Monotonic progression: sync forward with decoder PTS but prevent backward jitter
                if pos is not None and pos > 0:
                    if pos > self.elapsed and (pos - self.elapsed) < 2.0:
                        self.elapsed = pos

        if self.on_time_update:
            self.on_time_update(self.elapsed, self.duration)

        # Track end detection
        if getattr(self.player, 'state', None) == 'stop' and not self.paused and self.elapsed > 1.0:
            return self._end_track()

        if self.duration > 0 and self.elapsed >= self.duration:
            return self._end_track()

        return True

    def pause(self):
        if not self.player:
            return
        self.paused = True
        try:
            if hasattr(self.player, '_ffplayer') and self.player._ffplayer:
                self.player._ffplayer.set_pause(True)
                self.player.state = 'stop'
                self.player._state = 'paused'
            elif hasattr(self.player, 'set_pause'):
                self.player.set_pause(True)
            else:
                self.player.stop()
        except Exception:
            self.player.stop()

    def unpause(self):
        if not self.player:
            return
        self.paused = False
        self.last_tick = time.time()
        try:
            if hasattr(self.player, '_ffplayer') and self.player._ffplayer:
                self.player._ffplayer.set_pause(False)
                self.player.state = 'play'
                self.player._state = 'playing'
            elif hasattr(self.player, 'set_pause'):
                self.player.set_pause(False)
            else:
                self.player.play()
                Clock.schedule_once(lambda dt: self._safe_seek(self.elapsed), 0.1)
        except Exception:
            self.player.play()
            Clock.schedule_once(lambda dt: self._safe_seek(self.elapsed), 0.1)

    def seek(self, target_pos: float):
        if not self.player:
            return
        self.elapsed = max(0.0, min(target_pos, self.duration if self.duration > 0 else target_pos))
        self.last_tick = time.time()
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

    def set_equalizer(self, bands: list, reverb: bool = False):
        """Sets 10-band equalizer dB gains (-12 to +12 dB) and reverb simulation."""
        self.eq_bands = list(bands)
        self.eq_reverb = reverb
        if self.player and hasattr(self.player, '_ffplayer') and self.player._ffplayer:
            try:
                freqs = [32, 64, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
                filters = []
                for freq, gain in zip(freqs, bands):
                    if abs(gain) >= 0.1:
                        filters.append(f"equalizer=f={freq}:t=q:w=1:g={gain:.1f}")
                if reverb:
                    filters.append("aecho=0.8:0.88:60:0.4")
                filter_str = ",".join(filters) if filters else "anull"
                if hasattr(self.player._ffplayer, 'set_filter'):
                    self.player._ffplayer.set_filter(filter_str)
            except Exception as e:
                print(f"[AudioEngine EQ]: {e}")

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

    def fade_out(self, duration: float = 0.25, on_complete=None):
        """
        Gradually decreases audio volume towards 0.0 over the given duration,
        then pauses/stops playback and triggers on_complete callback.
        """
        from kivy.clock import Clock
        if not self.player:
            if on_complete:
                on_complete()
            return

        current_vol = getattr(self.player, "volume", 1.0)
        steps = 10
        interval = max(0.01, duration / steps)
        step_val = current_vol / steps

        def _step(dt):
            nonlocal current_vol
            if not self.player:
                if on_complete:
                    on_complete()
                return False
            current_vol = max(0.0, current_vol - step_val)
            try:
                self.player.volume = current_vol
            except Exception:
                pass
            if current_vol <= 0.001:
                try:
                    self.player.stop()
                except Exception:
                    pass
                if on_complete:
                    on_complete()
                return False
            return True

        Clock.schedule_interval(_step, interval)
