# player/audio_engine.py

import time
from ffpyplayer.player import MediaPlayer


class AudioEngine:
    def __init__(self):
        self.player = None
        self.paused = False
        self.elapsed = 0.0
        self.duration = 0.0
        self.last_tick = None

    def play(self, file_path, duration=0):
        self.stop()

        self.player = MediaPlayer(file_path)
        self.elapsed = 0.0
        self.duration = duration or 0.0
        self.last_tick = time.time()
        self.paused = False

    def toggle_pause(self):
        if not self.player:
            return
        self.paused = not self.paused
        self.player.set_pause(self.paused)

    def stop(self):
        if self.player:
            try:
                self.player.close_player()
            except:
                pass
        self.player = None

    def update(self):
        if not self.player:
            return None

        audio_frame, val = self.player.get_frame()

        if not self.paused:
            now = time.time()
            self.elapsed += now - self.last_tick
            self.last_tick = now

        if val == 'eof':
            self.stop()
            return 'eof'

        return 'playing'
