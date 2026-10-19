# download/cache_manager.py

import os
import time

CACHE_TTL = 15 * 60  # 15 minutes


class CacheManager:
    def __init__(self, db, cache_dir="cache"):
        self.db = db
        self.cache_dir = cache_dir

    def cleanup(self):
        now = time.time()
        songs = self.db.get_cached_youtube_songs()

        for song in songs:
            last_played = song["last_played"]
            if last_played is None:
                continue

            if now - last_played > CACHE_TTL:
                path = song["file_path"]
                if path and os.path.exists(path):
                    try:
                        os.remove(path)
                        self.db.mark_uncached(song["id"])
                    except Exception as e:
                        print("Cache cleanup error:", e)
