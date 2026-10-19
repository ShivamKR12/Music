# library/database.py

import sqlite3
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "library.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

        print("DB PATH:", DB_PATH)

    def _create_tables(self):
        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            artist TEXT,
            album TEXT,
            duration REAL,
            source TEXT,
            file_path TEXT UNIQUE,
            artwork_path TEXT,
            last_played REAL,
            is_cached INTEGER DEFAULT 1
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS playlist_songs (
            playlist_id INTEGER,
            song_id INTEGER,
            position INTEGER,
            PRIMARY KEY (playlist_id, song_id)
        )
        """)

        self.conn.commit()

    # ---------------------------
    # SONG METHODS
    # ---------------------------
    def add_song(self, song):
        cur = self.conn.cursor()
        cur.execute("""
        INSERT OR IGNORE INTO songs
        (title, artist, album, duration, source, file_path, artwork_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            song.title,
            song.artist,
            song.album,
            song.duration,
            song.source,
            song.file_path,
            song.artwork_path
        ))
        self.conn.commit()

        cur.execute(
            "SELECT id FROM songs WHERE file_path = ?",
            (song.file_path,)
        )
        row = cur.fetchone()
        song.id = row["id"]

    def get_all_songs(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM songs")
        return cur.fetchall()
    
    def get_song_by_id(self, song_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
        return cur.fetchone()
    
    def get_songs_by_source(self, source):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM songs WHERE source = ?", (source,))
        return cur.fetchall()
    
    def mark_played(self, song_id):
        cur = self.conn.cursor()
        cur.execute("""
        UPDATE songs
        SET last_played = ?, is_cached = 1
        WHERE id = ?
        """, (time.time(), song_id))
        self.conn.commit()

    def get_cached_youtube_songs(self):
        cur = self.conn.cursor()
        cur.execute("""
        SELECT * FROM songs
        WHERE source='youtube' AND is_cached=1
        """)
        return cur.fetchall()

    def mark_uncached(self, song_id):
        cur = self.conn.cursor()
        cur.execute("""
        UPDATE songs SET is_cached=0 WHERE id=?
        """, (song_id,))
        self.conn.commit()
