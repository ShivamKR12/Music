# player/playback_state.py

from enum import Enum

class PlaybackMode(Enum):
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"

class RepeatMode(Enum):
    OFF = "off"
    ALL = "all"
    ONE = "one"

class PlaybackState:
    def __init__(self):
        self.mode = PlaybackMode.STOPPED
        self.current_song = None
        self.current_index = 0
        self.shuffle = False
        self.repeat_mode = RepeatMode.OFF
        self.queue = []
        self.history = []
        self.volume = 1.0
        self.progress = 0.0
        self.duration = 0.0

    def play(self):
        if self.current_song:
            self.mode = PlaybackMode.PLAYING

    def pause(self):
        if self.mode == PlaybackMode.PLAYING:
            self.mode = PlaybackMode.PAUSED

    def stop(self):
        self.mode = PlaybackMode.STOPPED
        self.progress = 0.0

    def next_song(self):
        if not self.queue:
            return None
        if self.repeat_mode == RepeatMode.ONE:
            return self.current_song
        if self.shuffle:
            import random
            available = [s for s in self.queue if s != self.current_song]
            if available:
                next_song = random.choice(available)
                self.history.append(self.current_song)
                return next_song
        else:
            try:
                current_idx = self.queue.index(self.current_song)
                next_idx = (current_idx + 1) % len(self.queue)
                self.history.append(self.current_song)
                return self.queue[next_idx]
            except ValueError:
                return self.queue[0] if self.queue else None

    def previous_song(self):
        if self.history:
            return self.history.pop()
        if self.repeat_mode == RepeatMode.ONE:
            return self.current_song
        if self.shuffle:
            import random
            available = [s for s in self.queue if s != self.current_song]
            if available:
                return random.choice(available)
        else:
            try:
                current_idx = self.queue.index(self.current_song)
                prev_idx = (current_idx - 1) % len(self.queue)
                return self.queue[prev_idx]
            except ValueError:
                return self.queue[-1] if self.queue else None

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle

    def set_repeat_mode(self, mode):
        if isinstance(mode, str):
            mode = RepeatMode(mode)
        self.repeat_mode = mode

    def cycle_repeat_mode(self):
        modes = list(RepeatMode)
        current_idx = modes.index(self.repeat_mode)
        self.repeat_mode = modes[(current_idx + 1) % len(modes)]

    def add_to_queue(self, song):
        self.queue.append(song)

    def remove_from_queue(self, song):
        if song in self.queue:
            self.queue.remove(song)

    def clear_queue(self):
        self.queue.clear()

    def set_current_song(self, song):
        if song in self.queue:
            self.current_song = song
            self.current_index = self.queue.index(song)

    def get_queue_position(self):
        if self.current_song and self.current_song in self.queue:
            return self.queue.index(self.current_song)
        return -1

    def is_playing(self):
        return self.mode == PlaybackMode.PLAYING

    def is_paused(self):
        return self.mode == PlaybackMode.PAUSED

    def is_stopped(self):
        return self.mode == PlaybackMode.STOPPED

    def set_progress(self, progress):
        self.progress = max(0.0, min(1.0, progress))

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))

    def seek_to(self, position):
        self.progress = max(0.0, min(1.0, position))

    def get_state_dict(self):
        return {
            'mode': self.mode.value,
            'current_song': self.current_song,
            'current_index': self.current_index,
            'shuffle': self.shuffle,
            'repeat_mode': self.repeat_mode.value,
            'queue': self.queue.copy(),
            'history': self.history.copy(),
            'volume': self.volume,
            'progress': self.progress,
            'duration': self.duration
        }

    def load_state_dict(self, state_dict):
        self.mode = PlaybackMode(state_dict.get('mode', 'stopped'))
        self.current_song = state_dict.get('current_song')
        self.current_index = state_dict.get('current_index', 0)
        self.shuffle = state_dict.get('shuffle', False)
        self.repeat_mode = RepeatMode(state_dict.get('repeat_mode', 'off'))
        self.queue = state_dict.get('queue', [])
        self.history = state_dict.get('history', [])
        self.volume = state_dict.get('volume', 1.0)
        self.progress = state_dict.get('progress', 0.0)
        self.duration = state_dict.get('duration', 0.0)
