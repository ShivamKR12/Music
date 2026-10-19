from kivy.app import App
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

from yt_dlp import YoutubeDL
from ffpyplayer.player import MediaPlayer

import threading
import time
import os


class SilentLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


class PlayerUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.url_input = TextInput(hint_text='Paste YouTube URL here', size_hint_y=None, height=40, multiline=False)

        controls = BoxLayout(size_hint_y=None, height=40)

        self.play_btn = Button(text='Play')
        self.pause_btn = Button(text='Pause')

        self.status = Label(text='Idle')

        self.progress = ProgressBar(max=1.0, value=0)
        self.time_label = Label(text='00:00 / 00:00')

        self.play_btn.bind(on_press=self.start_play)
        self.pause_btn.bind(on_press=self.pause_resume)

        controls.add_widget(self.play_btn)
        controls.add_widget(self.pause_btn)

        self.add_widget(controls)
        self.add_widget(self.url_input)
        self.add_widget(self.status)
        self.add_widget(self.progress)
        self.add_widget(self.time_label)

        self.player = None
        self.paused = False
        self.elapsed = 0.0
        self.duration = 0.0
        self.last_tick = None
        self.downloading = False
        self.player_active = False
        self.current_info = None
        self.stream_failed = False
        self.retry_scheduled = False
        self.resume_time = 0.0

    def cache_path_from_info(self, info):
        video_id = info['id']
        return os.path.join("cache", f"{video_id}.opus")

    def start_play(self, *_):
        self.set_play_enabled(False)
        url = self.url_input.text.strip()
        if not url:
            self.status.text = 'Please enter a URL'
            return
        self.status.text = "Fetching stream..."

        threading.Thread(
            target=self.stream_or_play_cached,
            args=(url,),
            daemon=True
        ).start()

    def stream_or_play_cached(self, url):
        try:
            ydl_opts = {
                'format': 'bestaudio',
                'quiet': True,
                'noplaylist': True,
                'logger': SilentLogger(),
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                prepared = ydl.prepare_filename(info)
                print("yt-dlp prepared filename:", prepared)

                cached_path = self.cache_path_from_info(info)
                print("Checking cache path:", cached_path)
                print("Exists?", os.path.exists(cached_path))

                id_cache = os.path.join("cache", f"{info['id']}.opus")
                print("ID-based cache path:", id_cache)
                print("Exists?", os.path.exists(id_cache))

                self.current_info = info
                self.stream_failed = False
                self.retry_scheduled = False

                # PLAY CACHED FILE (NO STREAMING)
                if os.path.exists(cached_path):
                    Clock.schedule_once(lambda dt:
                        self.play_audio(
                            cached_path,
                            info.get('title', 'Unknown'),
                            info.get('duration', 0)
                        )
                    )
                    return

                # NOT CACHED → STREAM + DOWNLOAD
                stream_url = info['url']

                Clock.schedule_once(lambda dt:
                    self.play_audio(
                        stream_url,
                        info.get('title', 'Unknown'),
                        info.get('duration', 0)
                    )
                )

                threading.Thread(
                    target=self.download_for_cache,
                    args=(url,),
                    daemon=True
                ).start()

        except Exception as e:
            Clock.schedule_once(lambda dt: self.set_status(f"Error: {e}"))
        finally:
            self.downloading = False

    def download_for_cache(self, url):
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'cache/%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
                'preferredquality': '192',
            }],
            'quiet': True,
            'noplaylist': True,
            'logger': SilentLogger(),
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=True)
        except:
            pass  # cache failure should not affect playback

    def retry_from_cache(self, dt):
        if not self.current_info:
            return

        cache_path = self.cache_path_from_info(self.current_info)

        if os.path.exists(cache_path):
            self.status.text = "Recovered from cache"
            self.play_audio(
                cache_path,
                self.current_info.get('title', 'Unknown'),
                self.current_info.get('duration', 0),
                seek_to=self.resume_time
            )
        else:
            self.status.text = "Playback failed (cache unavailable)"
            self.set_play_enabled(True)

    def play_audio(self, audio_url, title, duration, seek_to=0.0):
        # Stop existing player if active
        if self.player:
            Clock.unschedule(self.update)
            try:
                self.player.close_player()
            except:
                pass
            self.player = None

        self.player = MediaPlayer(audio_url)

        if seek_to > 0:
            try:
                self.player.seek(seek_to, relative=False)
                self.elapsed = seek_to
            except:
                self.elapsed = 0.0

        self.elapsed = 0.0
        self.duration = duration or 0.0
        self.last_tick = None

        self.progress.value = 0
        self.progress.max = self.duration if self.duration > 0 else 1

        self.status.text = f'Playing: {title}'
        self.update_time_label()

        self.url_input.text = ''

        self.set_play_enabled(True)

        Clock.schedule_interval(self.update, 0.1)
    
    def pause_resume(self, *_):
        if not self.player:
            return

        self.paused = not self.paused
        self.player.set_pause(self.paused)

        self.status.text = 'Paused' if self.paused else 'Playing'

    def update(self, dt):
        if not self.player:
            return

        try:
            audio_frame, val = self.player.get_frame()
        except:
            self.status.text = 'Stream disconnected'
            self.stream_failed = True
            self.cleanup_player()

            # Try auto-retry from cache (once)
            if not self.retry_scheduled:
                self.retry_scheduled = True
                Clock.schedule_once(self.retry_from_cache, 0.5)

            return False

        # Initialize timer on first tick
        if self.last_tick is None:
            self.last_tick = time.time()
            return

        if not self.paused:
            now = time.time()
            delta = now - self.last_tick
            self.last_tick = now

            if delta > 0:
                self.elapsed += delta
                self.resume_time = self.elapsed

        if self.duration > 0:
            self.progress.value = min(self.elapsed, self.duration)

        self.update_time_label()

        if val == 'eof' or (self.duration > 0 and self.elapsed >= self.duration):
            self.status.text = 'Finished'
            self.elapsed = self.duration  # ensure timer shows full length
            self.progress.value = self.duration
            if self.player:
                try:
                    self.player.close_player()  # ensures resources are freed
                except:
                    pass
            self.player = None
            return False

    def set_status(self, text):
        self.status.text = text
    
    def update_time_label(self):
        def fmt(seconds):
            m = int(seconds) // 60
            s = int(seconds) % 60
            return f"{m:02}:{s:02}"

        self.time_label.text = f"{fmt(self.elapsed)} / {fmt(self.duration)}"

    def cleanup_player(self):
        if self.player:
            Clock.unschedule(self.update)
            try:
                self.player.close_player()
            except:
                pass
            self.player = None

    def set_play_enabled(self, enabled: bool):
        self.play_btn.disabled = not enabled


class MusicApp(App):
    def build(self):
        return PlayerUI()


if __name__ == '__main__':
    MusicApp().run()
