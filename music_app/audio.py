import os
import socket
import time
import json
import threading
import urllib.request
import re
from kivy.clock import Clock
from yt_dlp import YoutubeDL
from kivy.core.audio import SoundLoader

from utils import sanitize_text, extract_video_id, SilentLogger, fetch_youtube_metadata, get_cache_dir

class AudioEngine:
    """Download-then-play audio engine isolation."""
    def __init__(self):
        self.player = None
        self.elapsed = 0.0
        self.duration = 0.0
        self.last_tick = None
        self.paused = False
        self.current_info = None
        self.current_path = None
        self.loading = False

        self.on_time_update = None
        self.on_track_end = None
        self.on_artwork_loaded = None  # Decoupled bridge hook
        self.on_track_ready = None
        self.on_error = None
        self.on_loading = None
        self.on_download_progress = None

        self.repeat_one = False
        self.lock = threading.Lock()
        self.cancel_event = threading.Event()

    def start_play(self, url: str):
        if not url:
            return False

        with self.lock:
            self.cancel_event.set()
            self.cleanup_player()
            self.loading = True
            self.cancel_event = threading.Event()
            current_event = self.cancel_event

        print(f"[THREAD START] AudioEngine._download_and_play for URL: {url}")
        threading.Thread(
            target=self._download_and_play,
            args=(url, current_event),
            daemon=True
        ).start()
        return True

    def cleanup_player(self):
        Clock.unschedule(self._update)
        if self.player:
            try:
                self.player.stop()
                self.player.unload()
            except:
                pass
        self.player = None
        self.elapsed = 0.0
        self.duration = 0.0
        self.last_tick = None
        self.paused = False
        
    def _set_loading(self, state):
        self.loading = state
        if self.on_loading:
            self.on_loading(state)

    def _download_and_play(self, url, cancel_event):
        try:
            Clock.schedule_once(lambda dt: self._set_loading(True), 0)
            video_id = extract_video_id(url)
            audio_path = self._cache_path_from_id(video_id)
            
            if os.path.exists(audio_path):
                info = self._load_cached_metadata(audio_path) or {}
                if cancel_event.is_set():
                    print(f"[THREAD SKIP] AudioEngine._download_and_play cancelled/skipped for cached URL: {url}")
                    return
                
                # Use Clock to pass variables safely across boundaries to the Main UI Thread
                Clock.schedule_once(lambda dt: self._set_main_thread_info(info, audio_path), 0)
                
                if info.get("artwork") and self.on_artwork_loaded:
                    Clock.schedule_once(lambda dt: self.on_artwork_loaded(info["artwork"]), 0)
                    
                print(f"[THREAD SUCCESS] AudioEngine._download_and_play (from cache) for URL: {url}")
                Clock.schedule_once(lambda dt: self._play_file(audio_path, info), 0)
                Clock.schedule_once(lambda dt: self._set_loading(False), 0)
                return

            if cancel_event.is_set():
                print(f"[THREAD SKIP] AudioEngine._download_and_play cancelled before download for URL: {url}")
                return

            def download_hook(d):
                if cancel_event.is_set():
                    raise InterruptedError("Cancelled by user action")
                if d.get('status') == 'downloading' and self.on_download_progress:
                    raw_percent = d.get('_percent_str', '')
                    # yt-dlp outputs ANSI color codes in strings; strip them for UI labels
                    clean_percent = re.sub(r'\x1b\[[0-9;]*m', '', raw_percent).strip()
                    if clean_percent:
                        Clock.schedule_once(lambda dt, p=clean_percent: self.on_download_progress(p), 0)

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(get_cache_dir(), "%(id)s.%(ext)s"),
                "quiet": True,
                "noplaylist": True,
                "logger": SilentLogger(),
                "socket_timeout": 15,
                "nocheckcertificate": True, # Skips SSL check issues on older environments
                "continuedl": True, # Safely resume interrupted downloads so we don't start from 0%
                "retries": 3,
                "sleep_interval": 2,
                "max_sleep_interval": 5,
                "progress_hooks": [download_hook],
            }
            
            # Create a single YoutubeDL instance to preserve session cookies and URL signatures
            with YoutubeDL(ydl_opts) as ydl_dl:
                # 1. Fetch metadata first (Fast)
                info = ydl_dl.extract_info(url, download=False)
                if cancel_event.is_set(): return
                
                stream_url = info.get("url")

                # Structure explicit tracking variables out cleanly
                clean_info = {
                    "id": info.get("id"),
                    "title": sanitize_text(info.get("title", "Unknown Title")),
                    "duration": int(info.get("duration", 0)),
                    "artwork": ""
                }

                thumb_url = info.get("thumbnail")
                base_path, _ = os.path.splitext(audio_path)
                thumb_path = base_path + ".jpg"

                if thumb_url and not os.path.exists(thumb_path):
                    self._download_thumbnail(thumb_url, thumb_path)

                if os.path.exists(thumb_path):
                    clean_info["artwork"] = thumb_path

                if cancel_event.is_set():
                    return

                # 2. Push metadata to UI instantly so the user sees the track title and cover
                Clock.schedule_once(lambda dt: self._set_main_thread_info(clean_info, audio_path), 0)
                if clean_info.get("artwork") and self.on_artwork_loaded:
                    Clock.schedule_once(lambda dt: self.on_artwork_loaded(clean_info["artwork"]), 0)
                
                # 3. Download using the same session (Prevents 403 Forbidden signature mismatch)
                actual_download_path = ydl_dl.prepare_filename(info)
                ydl_dl.process_ie_result(info, download=True)
                
            if not os.path.exists(audio_path) and os.path.exists(actual_download_path):
                audio_path = actual_download_path
            self._save_cached_metadata(audio_path, clean_info)
            
            if cancel_event.is_set(): return
            
            Clock.schedule_once(lambda dt: self._play_file(audio_path, clean_info), 0)
            Clock.schedule_once(lambda dt: self._set_loading(False), 0)
            
        except Exception as e:
            if cancel_event.is_set():
                print(f"[THREAD SKIP] AudioEngine._download_and_play aborted via exception for URL: {url}")
                return
            print("AudioEngine background processing error:", e)
            print(f"[THREAD FAILED] AudioEngine._download_and_play error: {e}")
            if self.on_error:
                error_msg = str(e)
                Clock.schedule_once(lambda dt: self.on_error(error_msg), 0)
            Clock.schedule_once(lambda dt: self._set_loading(False), 0)
        finally:
            print(f"[THREAD END] AudioEngine._download_and_play exiting for URL: {url}")
            with self.lock:
                if not cancel_event.is_set():
                    Clock.schedule_once(lambda dt: self._set_loading(False), 0)

    def _set_main_thread_info(self, info, path):
        """Safely assign values to properties on the Main Thread context."""
        self.current_info = info
        self.current_path = path

    def _play_file(self, path, info):
        self.cleanup_player()
        self.player = SoundLoader.load(path)
        if self.player:
            self.player.play()
        self.duration = info.get("duration", 0) or (self.player.length if hasattr(self.player, 'length') else 0)
        self.elapsed = 0.0
        self.last_tick = None
        self.paused = False
        self._has_started_playing = False
        
        artwork = info.get("artwork")
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
            pos = self.player.get_pos() if hasattr(self.player, 'get_pos') else None
            
            if not getattr(self, '_has_started_playing', False):
                if pos is not None and pos > 0:
                    self._has_started_playing = True
                elif pos is None:
                    self._has_started_playing = True
                    
            if getattr(self, '_has_started_playing', False):
                self.elapsed += dt_real
                
                # Periodically sync with the underlying engine to prevent drift
                if pos is not None and pos > 0:
                    if abs(self.elapsed - pos) > 0.5:
                        self.elapsed = pos
            
        if self.on_time_update:
            self.on_time_update(self.elapsed, self.duration)
            
        if self.player.state == 'stop' and not self.paused and self.elapsed > 0:
            return self._end_track()
        if self.duration > 0 and self.elapsed >= self.duration:
            return self._end_track()
        return True

    def pause(self):
        if not self.player: return
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
        except:
            self.player.stop()
            
    def unpause(self):
        if not self.player: return
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
                # Schedule seek slightly later to ensure stream is open
                Clock.schedule_once(lambda dt: self._safe_seek(self.elapsed), 0.1)
        except:
            self.player.play()
            Clock.schedule_once(lambda dt: self._safe_seek(self.elapsed), 0.1)

    def _safe_seek(self, pos):
        if hasattr(self.player, 'seek'):
            try:
                self.player.seek(pos)
            except TypeError:
                try:
                    self.player.seek(pos, relative=False)
                except: pass

    def _end_track(self):
        if self.repeat_one and self.player:
            try:
                self.player.seek(0)
                self.player.play()
                self.elapsed = 0.0
                self.last_tick = time.time()
                if self.on_time_update:
                    self.on_time_update(0.0, self.duration)
                return True
            except:
                pass
        self.cleanup_player()
        if self.on_track_end:
            self.on_track_end()
        return False

    def _cache_path_from_id(self, video_id):
        base = os.path.join(get_cache_dir(), video_id)
        for ext in [".opus", ".webm", ".m4a", ".mp4", ".mp3", ".wav", ".flac", ".ogg", ".mkv"]:
            path = base + ext
            if os.path.exists(path): return path
        return base + ".opus"

    def _save_cached_metadata(self, audio_path, info):
        base_path, _ = os.path.splitext(audio_path)
        meta_path = base_path + ".json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump({
                "id": info.get("id"),
                "title": info.get("title"),
                "duration": info.get("duration", 0),
                "artwork": info.get("artwork")
            }, f, ensure_ascii=False, indent=4)

    def _load_cached_metadata(self, audio_path):
        base_path, _ = os.path.splitext(audio_path)
        meta_path = base_path + ".json"
        if not os.path.exists(meta_path): return None
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _download_thumbnail(self, url, path):
        try:
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            socket.setdefaulttimeout(15)
            with urllib.request.urlopen(url, context=ctx) as response, open(path, 'wb') as out_file:
                out_file.write(response.read())
        except Exception as e:
            print("Thumbnail recovery failed:", e)
