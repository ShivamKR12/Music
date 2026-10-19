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

    def start_play(self, *_):
        url = self.url_input.text.strip()
        if not url:
            self.status.text = 'Please enter a URL'
            return

        self.status.text = 'Fetching audio...'
        threading.Thread(target=self.fetch_and_play, args=(url,), daemon=True).start()

    def fetch_and_play(self, url):
        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'noplaylist': True,
            'logger': SilentLogger(),
            'outtmpl': 'cache/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
                'preferredquality': '192',
            }],
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                local_file_path = ydl.prepare_filename(info)
                # adjust for postprocessor extension
                local_file_path = os.path.splitext(local_file_path)[0] + ".opus"

                if not os.path.exists(local_file_path):
                    # download only if missing
                    info = ydl.extract_info(url, download=True)

            Clock.schedule_once(lambda dt, u=local_file_path, t=info.get('title', 'Unknown'), d=info.get('duration', 0): self.play_audio(u, t, d))

        except Exception as e:
            err = str(e)
            Clock.schedule_once(lambda dt, err=err: self.set_status(f'Error: {err}'))

    def play_audio(self, audio_url, title, duration):
        if self.player:
            Clock.unschedule(self.update)

        self.player = MediaPlayer(audio_url)

        self.elapsed = 0.0
        self.duration = duration or 0.0
        self.last_tick = time.time()

        self.progress.value = 0
        self.progress.max = self.duration if self.duration > 0 else 1

        self.status.text = f'Playing: {title}'
        self.update_time_label()

        self.url_input.text = ''

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
            self.player = None
            return False

        if audio_frame is not None and self.last_tick is None:
            # first frame arrived → start timer
            self.last_tick = time.time()

        if not self.paused:
            now = time.time()
            self.elapsed += now - self.last_tick
            self.last_tick = now

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


class MusicApp(App):
    def build(self):
        return PlayerUI()


if __name__ == '__main__':
    MusicApp().run()
