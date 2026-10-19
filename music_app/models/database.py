import sqlite3
import os
import threading
from kivy.app import App
from kivy.utils import platform

from utils import sanitize_text

DB_LOCK = threading.Lock()
_POOL_CONN = None

def get_db_path():
    app = App.get_running_app()
    if platform == 'android' and app:
        return os.path.join(app.user_data_dir, 'music_app.db')
    return 'music_app.db'

def get_connection():
    global _POOL_CONN
    if _POOL_CONN is None:
        _POOL_CONN = sqlite3.connect(get_db_path(), check_same_thread=False)
    return _POOL_CONN

def init_db():
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                video_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                artist TEXT,
                url TEXT,
                local_path TEXT,
                duration INTEGER,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_played DATETIME
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
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
        
        cursor.execute("SELECT COUNT(*) FROM playlists")
        
        if cursor.fetchone()[0] == 0:
            default_playlists = [("Favorites",), ("Late Night",), ("Workout",)]
            cursor.executemany("INSERT INTO playlists (name) VALUES (?)", default_playlists)
        
        conn.commit()

def get_all_tracks():
    """Fetches every tracking record stored inside the persistent engine."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT title, artist, url, video_id FROM tracks")
        
        rows = cursor.fetchall()
        
        return rows

def update_local_track_path(video_id, local_path, duration):
    """Updates the record once a background thread finishes downloading an asset."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tracks 
            SET local_path = ?, duration = ? 
            WHERE video_id = ?
        ''', (local_path, duration, video_id))
        
        conn.commit()

def add_track(video_id, title, artist, url, duration=0):
    """Inserts a new track into the database if it doesn't already exist."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            title = sanitize_text(title)
            artist = sanitize_text(artist)
        
            cursor.execute('''
                INSERT OR IGNORE INTO tracks (video_id, title, artist, url, local_path, duration)
                VALUES (?, ?, ?, ?, '', ?)
            ''', (video_id, title, artist, url, duration))
        
            conn.commit()
        
        except Exception as e:
            print("Database insertion failure:", e)

def get_continue_listening(limit=5):
    """Fetches recently played tracks for the Continue Listening section."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title, artist, url, video_id FROM tracks WHERE last_played IS NOT NULL ORDER BY last_played DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        return rows

def get_recently_added(limit=10):
    """Fetches newest tracks sorted by creation timestamp."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title, artist, url, video_id FROM tracks ORDER BY added_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        return rows

def mark_track_played(video_id):
    """Stamps the given track with the current time as its last played date."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tracks SET last_played = CURRENT_TIMESTAMP WHERE video_id = ?", (video_id,))
        conn.commit()

def get_all_playlists():
    """Fetches every custom user playlist profile out of storage."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM playlists ORDER BY name ASC")
        
        rows = cursor.fetchall()
        
        return [r[0] for r in rows]

def add_playlist(name):
    """Dynamically creates a new user playlist grouping."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO playlists (name) VALUES (?)", (name,))
            conn.commit()
        except Exception as e:
            print("Playlist creation failure:", e)

def get_playlist_tracks(playlist_name):
    """Retrieves all tracks associated with a specific playlist name."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.title, t.artist, t.url, t.video_id
            FROM playlist_tracks pt
            JOIN playlists p ON pt.playlist_id = p.id
            JOIN tracks t ON pt.video_id = t.video_id
            WHERE p.name = ?
            ORDER BY pt.rowid ASC
        ''', (playlist_name,))
        return cursor.fetchall()

def add_track_to_playlist(playlist_name, video_id):
    """Adds a track to a specific playlist."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM playlists WHERE name = ?", (playlist_name,))
        row = cursor.fetchone()
        if not row: return
        playlist_id = row[0]
        try:
            cursor.execute("INSERT INTO playlist_tracks (playlist_id, video_id) VALUES (?, ?)", (playlist_id, video_id))
            conn.commit()
        except: pass

def remove_track_from_playlist(playlist_name, video_id):
    """Removes a track from a specific playlist."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM playlists WHERE name = ?", (playlist_name,))
        row = cursor.fetchone()
        if not row: return
        playlist_id = row[0]
        cursor.execute("DELETE FROM playlist_tracks WHERE playlist_id = ? AND video_id = ?", (playlist_id, video_id))
        conn.commit()

def is_favorite(video_id):
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM playlist_tracks pt JOIN playlists p ON pt.playlist_id = p.id WHERE p.name = 'Favorites' AND pt.video_id = ?", (video_id,))
        return cursor.fetchone() is not None

def toggle_favorite(video_id):
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM playlists WHERE name = 'Favorites'")
        row = cursor.fetchone()
        if not row:
            cursor.execute("INSERT INTO playlists (name) VALUES ('Favorites')")
            fav_id = cursor.lastrowid
        else:
            fav_id = row[0]
            
        cursor.execute("SELECT 1 FROM playlist_tracks WHERE playlist_id = ? AND video_id = ?", (fav_id, video_id))
        is_fav = cursor.fetchone() is not None
        
        if is_fav:
            cursor.execute("DELETE FROM playlist_tracks WHERE playlist_id = ? AND video_id = ?", (fav_id, video_id))
        else:
            cursor.execute("INSERT INTO playlist_tracks (playlist_id, video_id) VALUES (?, ?)", (fav_id, video_id))
        
        conn.commit()
        return not is_fav
def add_search_history(query):
    query = query.strip()
    if not query: return
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO search_history (query, searched_at) VALUES (?, CURRENT_TIMESTAMP)", (query,))
        conn.commit()

def get_search_history(limit=10):
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT query FROM search_history ORDER BY searched_at DESC LIMIT ?", (limit,))
        return [r[0] for r in cursor.fetchall()]

def clear_search_history():
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM search_history")
        conn.commit()
