import os
import sqlite3
import threading
from kivy.app import App
from kivy.utils import platform

DB_LOCK = threading.Lock()
_POOL_CONN = None

def sanitize_text(text):
    """Sanitize strings by stripping out unsupported emojis or extended characters."""
    if not text:
        return "Unknown"
    import re
    clean = re.sub(r'[^\w\s\x20-\x7E]', '', str(text))
    return re.sub(r'\s+', ' ', clean).strip()

def get_db_path():
    app = App.get_running_app()
    if platform == 'android' and app:
        return os.path.join(app.user_data_dir, 'music_app.db')
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'music_app.db')

def get_connection(db_path=None):
    global _POOL_CONN
    if _POOL_CONN is None:
        target_path = db_path or get_db_path()
        _POOL_CONN = sqlite3.connect(target_path, check_same_thread=False)
        _POOL_CONN.row_factory = sqlite3.Row
    return _POOL_CONN

def init_db(db_path=None):
    """Initializes the database schema and seeds default playlists if needed."""
    with DB_LOCK:
        conn = get_connection(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                video_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                artist TEXT,
                url TEXT,
                local_path TEXT,
                duration INTEGER DEFAULT 0,
                artwork TEXT,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_played DATETIME
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlist_tracks (
                playlist_id INTEGER,
                video_id TEXT,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(playlist_id) REFERENCES playlists(id),
                FOREIGN KEY(video_id) REFERENCES tracks(video_id),
                UNIQUE(playlist_id, video_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                query TEXT UNIQUE NOT NULL,
                searched_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Seed default playlists if table is newly created
        cursor.execute("SELECT COUNT(*) FROM playlists")
        if cursor.fetchone()[0] == 0:
            default_playlists = [("Favorites",), ("Late Night",), ("Workout",), ("Chillwave",)]
            cursor.executemany("INSERT INTO playlists (name) VALUES (?)", default_playlists)

        conn.commit()

def add_track(video_id, title, artist, url, duration=0, artwork="", local_path=""):
    """Inserts a new track record into the database, or updates an existing record."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            clean_title = sanitize_text(title)
            clean_artist = sanitize_text(artist)
            cursor.execute('''
                INSERT INTO tracks (video_id, title, artist, url, local_path, duration, artwork)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(video_id) DO UPDATE SET
                    title=excluded.title,
                    artist=excluded.artist,
                    url=excluded.url,
                    local_path=CASE WHEN excluded.local_path != '' THEN excluded.local_path ELSE tracks.local_path END,
                    duration=CASE WHEN excluded.duration > 0 THEN excluded.duration ELSE tracks.duration END,
                    artwork=CASE WHEN excluded.artwork != '' THEN excluded.artwork ELSE tracks.artwork END
            ''', (video_id, clean_title, clean_artist, url, local_path, duration, artwork))
            conn.commit()
        except Exception as e:
            print("Database error in add_track:", e)

def get_all_tracks():
    """Retrieves all tracks stored in the database."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT video_id, title, artist, url, local_path, duration, artwork FROM tracks ORDER BY added_at DESC")
        return [dict(row) for row in cursor.fetchall()]

def get_track(video_id):
    """Retrieves metadata for a specific track by video ID."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT video_id, title, artist, url, local_path, duration, artwork FROM tracks WHERE video_id = ?", (video_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_local_track_path(video_id, local_path, duration=None):
    """Updates local file path and duration once an asset is cached on disk."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        if duration is not None and duration > 0:
            cursor.execute('''
                UPDATE tracks 
                SET local_path = ?, duration = ? 
                WHERE video_id = ?
            ''', (local_path, duration, video_id))
        else:
            cursor.execute('''
                UPDATE tracks 
                SET local_path = ? 
                WHERE video_id = ?
            ''', (local_path, video_id))
        conn.commit()

def mark_track_played(video_id):
    """Records the timestamp when a track is played."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tracks SET last_played = CURRENT_TIMESTAMP WHERE video_id = ?", (video_id,))
        conn.commit()

def get_recently_played(limit=10):
    """Fetches the most recently played tracks."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT video_id, title, artist, url, local_path, duration, artwork 
            FROM tracks 
            WHERE last_played IS NOT NULL 
            ORDER BY last_played DESC 
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]

def get_all_playlists():
    """Fetches all playlist names from the database."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM playlists ORDER BY name ASC")
        return [dict(row) for row in cursor.fetchall()]

def add_playlist(name):
    """Creates a new playlist."""
    clean_name = sanitize_text(name)
    if not clean_name:
        return None
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO playlists (name) VALUES (?)", (clean_name,))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

def get_playlist_tracks(playlist_name):
    """Retrieves all tracks for a given playlist."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.video_id, t.title, t.artist, t.url, t.local_path, t.duration, t.artwork
            FROM playlist_tracks pt
            JOIN playlists p ON pt.playlist_id = p.id
            JOIN tracks t ON pt.video_id = t.video_id
            WHERE p.name = ?
            ORDER BY pt.rowid ASC
        ''', (playlist_name,))
        return [dict(row) for row in cursor.fetchall()]

def add_track_to_playlist(playlist_name, video_id):
    """Adds a track to a playlist by name."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM playlists WHERE name = ?", (playlist_name,))
        row = cursor.fetchone()
        if not row:
            cursor.execute("INSERT INTO playlists (name) VALUES (?)", (playlist_name,))
            playlist_id = cursor.lastrowid
        else:
            playlist_id = row['id']
            
        try:
            cursor.execute("INSERT OR IGNORE INTO playlist_tracks (playlist_id, video_id) VALUES (?, ?)", (playlist_id, video_id))
            conn.commit()
            return True
        except Exception:
            return False

def remove_track_from_playlist(playlist_name, video_id):
    """Removes a track from a playlist."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM playlists WHERE name = ?", (playlist_name,))
        row = cursor.fetchone()
        if not row:
            return False
        playlist_id = row['id']
        cursor.execute("DELETE FROM playlist_tracks WHERE playlist_id = ? AND video_id = ?", (playlist_id, video_id))
        conn.commit()
        return True

def is_favorite(video_id):
    """Returns True if the track is in the 'Favorites' playlist."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 1 
            FROM playlist_tracks pt 
            JOIN playlists p ON pt.playlist_id = p.id 
            WHERE p.name = 'Favorites' AND pt.video_id = ?
        ''', (video_id,))
        return cursor.fetchone() is not None

def toggle_favorite(video_id):
    """Toggles favorite status for a video ID and returns the new status."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM playlists WHERE name = 'Favorites'")
        row = cursor.fetchone()
        if not row:
            cursor.execute("INSERT INTO playlists (name) VALUES ('Favorites')")
            fav_id = cursor.lastrowid
        else:
            fav_id = row['id']

        cursor.execute("SELECT 1 FROM playlist_tracks WHERE playlist_id = ? AND video_id = ?", (fav_id, video_id))
        is_fav = cursor.fetchone() is not None

        if is_fav:
            cursor.execute("DELETE FROM playlist_tracks WHERE playlist_id = ? AND video_id = ?", (fav_id, video_id))
            new_status = False
        else:
            cursor.execute("INSERT INTO playlist_tracks (playlist_id, video_id) VALUES (?, ?)", (fav_id, video_id))
            new_status = True

        conn.commit()
        return new_status

def add_search_history(query):
    """Adds or updates a search query timestamp in search history."""
    clean_query = str(query).strip()
    if not clean_query:
        return
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO search_history (query, searched_at) VALUES (?, CURRENT_TIMESTAMP)", (clean_query,))
        conn.commit()

def get_search_history(limit=10):
    """Retrieves recent search queries ordered by searched_at timestamp."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT query FROM search_history ORDER BY searched_at DESC LIMIT ?", (limit,))
        return [row['query'] for row in cursor.fetchall()]

def clear_search_history():
    """Wipes all search history entries."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM search_history")
        conn.commit()
