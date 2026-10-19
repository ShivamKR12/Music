class PlaybackQueue:
    def __init__(self):
        self.queue = []
        self.index = 0

    def set(self, songs):
        self.queue = songs
        self.index = 0

    def current(self):
        return self.queue[self.index] if self.queue else None

    def next(self):
        self.index += 1
        if self.index < len(self.queue):
            return self.queue[self.index]
