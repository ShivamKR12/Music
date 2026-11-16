import os
import sqlite3
import threading
from kivy.app import App
from kivy.utils import platform

DB_LOCK = threading.RLock()
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

get_db_connection = get_connection

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
                last_played DATETIME,
                play_count INTEGER DEFAULT 0
            )
        ''')

        try:
            cursor.execute("ALTER TABLE tracks ADD COLUMN play_count INTEGER DEFAULT 0")
        except Exception:
            pass

        for col_stmt in [
            "ALTER TABLE tracks ADD COLUMN source TEXT DEFAULT 'youtube'",
            "ALTER TABLE tracks ADD COLUMN source_id TEXT",
            "ALTER TABLE tracks ADD COLUMN bitrate INTEGER DEFAULT 128",
            "ALTER TABLE tracks ADD COLUMN isrc TEXT",
        ]:
            try:
                cursor.execute(col_stmt)
            except Exception:
                pass

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

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('theme_style', 'Light')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('wifi_only', 'False')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('extract_artwork_colors', 'True')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('animated_bg_enabled', 'True')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('sponsorblock_enabled', 'True')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('crossfade_duration', '3')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('autoeq_profile', 'None')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('lyrics_offset', '0.0')")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache_store (
                cache_key TEXT PRIMARY KEY,
                payload TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Seed dynamic and default playlists
        dynamic_seed_playlists = [
            ("Favorites",),
            ("YouTube Global Top 50",),
            ("Viral Hits Today",),
            ("Your Daily Mix",),
            ("On Repeat",),
            ("Heavy Rotation",),
            ("Forgotten Favorites",),
            ("Chillwave",),
            ("Workout",),
            ("Late Night",)
        ]
        cursor.executemany("INSERT OR IGNORE INTO playlists (name) VALUES (?)", dynamic_seed_playlists)

        # Seed initial tracks to default playlists if playlist_tracks is empty
        cursor.execute("SELECT COUNT(*) FROM playlist_tracks")
        if cursor.fetchone()[0] == 0:
            cursor.execute("SELECT video_id FROM tracks LIMIT 4")
            sample_vids = [r[0] for r in cursor.fetchall()]
            if sample_vids:
                for pl_name in ["Favorites", "Chillwave", "Late Night", "Workout"]:
                    cursor.execute("SELECT id FROM playlists WHERE name = ?", (pl_name,))
                    prow = cursor.fetchone()
                    if prow:
                        pid = prow[0]
                        for vid in sample_vids:
                            cursor.execute("INSERT OR IGNORE INTO playlist_tracks (playlist_id, video_id) VALUES (?, ?)", (pid, vid))

        conn.commit()

def add_track(video_id, title, artist, url, duration=0, artwork="", local_path="", source="youtube", source_id="", bitrate=128, isrc=""):
    """Inserts a new track record into the database, or updates an existing record."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            clean_title = sanitize_text(title)
            clean_artist = sanitize_text(artist)
            cursor.execute('''
                INSERT INTO tracks (video_id, title, artist, url, local_path, duration, artwork, source, source_id, bitrate, isrc)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(video_id) DO UPDATE SET
                    title=excluded.title,
                    artist=excluded.artist,
                    url=excluded.url,
                    local_path=CASE WHEN excluded.local_path != '' THEN excluded.local_path ELSE tracks.local_path END,
                    duration=CASE WHEN excluded.duration > 0 THEN excluded.duration ELSE tracks.duration END,
                    artwork=CASE WHEN excluded.artwork != '' THEN excluded.artwork ELSE tracks.artwork END,
                    source=CASE WHEN excluded.source != '' THEN excluded.source ELSE tracks.source END,
                    source_id=CASE WHEN excluded.source_id != '' THEN excluded.source_id ELSE tracks.source_id END,
                    bitrate=CASE WHEN excluded.bitrate > 0 THEN excluded.bitrate ELSE tracks.bitrate END,
                    isrc=CASE WHEN excluded.isrc != '' THEN excluded.isrc ELSE tracks.isrc END
            ''', (video_id, clean_title, clean_artist, url, local_path, duration, artwork, source, source_id, bitrate, isrc))
            conn.commit()
        except Exception as e:
            print("Database error in add_track:", e)

def get_all_tracks():
    """Retrieves all tracks stored in the database."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT video_id, title, artist, url, local_path, duration, artwork, source, source_id, bitrate, isrc FROM tracks ORDER BY added_at DESC")
        return [dict(row) for row in cursor.fetchall()]

def get_track(video_id):
    """Retrieves metadata for a specific track by video ID."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT video_id, title, artist, url, local_path, duration, artwork, source, source_id, bitrate, isrc FROM tracks WHERE video_id = ?", (video_id,))
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

def update_track_artwork(video_id, artwork_path):
    """Updates the artwork path for a track in the database."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tracks 
            SET artwork = ? 
            WHERE video_id = ?
        ''', (artwork_path, video_id))
        conn.commit()

def mark_track_played(video_id):
    """Records the timestamp when a track is played and increments its play count."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tracks 
            SET last_played = CURRENT_TIMESTAMP,
                play_count = COALESCE(play_count, 0) + 1
            WHERE video_id = ?
        ''', (video_id,))
        conn.commit()

def get_on_repeat(limit=25):
    """
    Fetches tracks user listens to repeatedly (play_count >= 2).
    Falls back to recently played if library is fresh.
    """
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT video_id, title, artist, url, local_path, duration, artwork,
                   COALESCE(play_count, 0) as play_count
            FROM tracks 
            WHERE play_count >= 2
            ORDER BY play_count DESC, last_played DESC 
            LIMIT ?
        ''', (limit,))
        rows = [dict(r) for r in cursor.fetchall()]
        if len(rows) < 3:
            return get_recently_played(limit=limit)
        return rows

def get_heavy_rotation(limit=25):
    """Fetches user's all-time most played tracks."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT video_id, title, artist, url, local_path, duration, artwork,
                   COALESCE(play_count, 0) as play_count
            FROM tracks 
            ORDER BY play_count DESC, added_at DESC 
            LIMIT ?
        ''', (limit,))
        return [dict(r) for r in cursor.fetchall()]

def get_forgotten_favorites(limit=25):
    """
    Fetches favorited tracks that haven't been played in a while or have older last_played.
    """
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.video_id, t.title, t.artist, t.url, t.local_path, t.duration, t.artwork, 1 as is_favorite
            FROM playlist_tracks pt
            JOIN playlists p ON pt.playlist_id = p.id
            JOIN tracks t ON pt.video_id = t.video_id
            WHERE p.name = 'Favorites'
            ORDER BY CASE WHEN t.last_played IS NULL THEN 0 ELSE 1 END ASC, t.last_played ASC
            LIMIT ?
        ''', (limit,))
        return [dict(r) for r in cursor.fetchall()]

def get_daily_mix(limit=25):
    """
    Synthesizes a personalized Daily Mix from user's top played artists and favorites.
    """
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        # Find top 3 artists
        cursor.execute('''
            SELECT artist, SUM(COALESCE(play_count, 1)) as weight
            FROM tracks
            WHERE artist IS NOT NULL AND artist != '' AND artist != 'Unknown Artist'
            GROUP BY artist
            ORDER BY weight DESC
            LIMIT 3
        ''')
        top_artists = [r[0] for r in cursor.fetchall()]
        
        mix_tracks = []
        if top_artists:
            placeholders = ','.join('?' for _ in top_artists)
            cursor.execute(f'''
                SELECT video_id, title, artist, url, local_path, duration, artwork
                FROM tracks
                WHERE artist IN ({placeholders})
                ORDER BY RANDOM()
                LIMIT ?
            ''', (*top_artists, limit))
            mix_tracks = [dict(r) for r in cursor.fetchall()]

        if len(mix_tracks) < 5:
            # Augment with recently played or all tracks
            cursor.execute('''
                SELECT video_id, title, artist, url, local_path, duration, artwork
                FROM tracks
                ORDER BY added_at DESC
                LIMIT ?
            ''', (limit,))
            mix_tracks = [dict(r) for r in cursor.fetchall()]

        return mix_tracks

def get_dynamic_playlist_tracks(playlist_name: str, limit: int = 25):
    """
    Routes dynamic behavioral playlists to real aggregated SQLite data.
    """
    clean_name = playlist_name.strip()
    if clean_name == "On Repeat":
        return get_on_repeat(limit=limit)
    elif clean_name == "Heavy Rotation":
        return get_heavy_rotation(limit=limit)
    elif clean_name == "Forgotten Favorites":
        return get_forgotten_favorites(limit=limit)
    elif clean_name == "Your Daily Mix":
        return get_daily_mix(limit=limit)
    return None

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

def get_continue_listening(limit=5):
    """Fetches recently played tracks for the Continue Listening section."""
    return get_recently_played(limit=limit)

def get_recently_added(limit=10):
    """Fetches newest tracks sorted by creation timestamp."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT video_id, title, artist, url, local_path, duration, artwork 
            FROM tracks 
            ORDER BY added_at DESC 
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]

def get_all_playlists():
    """Fetches all playlist names from the database with track counts."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, p.name, COUNT(pt.video_id) as track_count
            FROM playlists p
            LEFT JOIN playlist_tracks pt ON p.id = pt.playlist_id
            GROUP BY p.id, p.name
            ORDER BY p.name ASC
        ''')
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

def delete_playlist(name):
    """Deletes a playlist and its track associations from the database."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM playlists WHERE name = ?", (name,))
        row = cursor.fetchone()
        if not row:
            return False
        pid = row['id']
        cursor.execute("DELETE FROM playlist_tracks WHERE playlist_id = ?", (pid,))
        cursor.execute("DELETE FROM playlists WHERE id = ?", (pid,))
        conn.commit()
        return True

def get_playlist_tracks(playlist_name):
    """Retrieves all tracks for a given playlist with pre-computed is_favorite status in a single query."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.video_id, t.title, t.artist, t.url, t.local_path, t.duration, t.artwork,
                   CASE WHEN fav.video_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite
            FROM playlist_tracks pt
            JOIN playlists p ON pt.playlist_id = p.id
            JOIN tracks t ON pt.video_id = t.video_id
            LEFT JOIN (
                SELECT pt_fav.video_id
                FROM playlist_tracks pt_fav
                JOIN playlists p_fav ON pt_fav.playlist_id = p_fav.id
                WHERE p_fav.name = 'Favorites'
            ) fav ON t.video_id = fav.video_id
            WHERE p.name = ?
            ORDER BY pt.rowid ASC
        ''', (playlist_name,))
        return [dict(row) for row in cursor.fetchall()]

def get_setting(key, default=None):
    """Retrieves a configuration setting by key from SQLite database."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row is not None else default
        except Exception as e:
            print(f"[get_setting error]: {e}")
            return default

def set_setting(key, value):
    """Saves or updates a configuration setting in SQLite database."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO settings (key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
            ''', (key, str(value) if value is not None else ""))
            conn.commit()
            return True
        except Exception as e:
            print(f"[set_setting error]: {e}")
            return False

def get_all_settings():
    """Retrieves all stored configuration settings as a dict."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT key, value FROM settings")
            return {row[0]: row[1] for row in cursor.fetchall()}
        except Exception:
            return {}

def save_cache_payload(cache_key, payload_dict):
    """Caches JSON data payload to SQLite database for instant offline UI recovery."""
    import json
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            payload_str = json.dumps(payload_dict)
            cursor.execute('''
                INSERT INTO cache_store (cache_key, payload, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(cache_key) DO UPDATE SET payload = excluded.payload, updated_at = CURRENT_TIMESTAMP
            ''', (cache_key, payload_str))
            conn.commit()
            return True
        except Exception as e:
            print(f"[save_cache_payload error]: {e}")
            return False

def load_cache_payload(cache_key, default=None):
    """Loads cached JSON data payload from SQLite database."""
    import json
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT payload FROM cache_store WHERE cache_key = ?", (cache_key,))
            row = cursor.fetchone()
            if row and row[0]:
                return json.loads(row[0])
        except Exception as e:
            print(f"[load_cache_payload error]: {e}")
    return default

def add_track_to_playlist(playlist_name, video_id, track_meta=None):
    """Adds a track to a playlist by name, ensuring track exists in database."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        if track_meta and video_id:
            try:
                cursor.execute('''
                    INSERT INTO tracks (video_id, title, artist, url, artwork, duration, local_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(video_id) DO UPDATE SET
                        title = excluded.title,
                        artist = excluded.artist,
                        url = CASE WHEN excluded.url != '' THEN excluded.url ELSE tracks.url END,
                        artwork = CASE WHEN excluded.artwork != '' AND excluded.artwork != 'album_art.png' THEN excluded.artwork ELSE tracks.artwork END,
                        duration = CASE WHEN excluded.duration > 0 THEN excluded.duration ELSE tracks.duration END,
                        local_path = CASE WHEN excluded.local_path != '' THEN excluded.local_path ELSE tracks.local_path END
                ''', (
                    video_id,
                    sanitize_text(track_meta.get("title", "Unknown Title")),
                    sanitize_text(track_meta.get("artist", "Unknown Artist")),
                    track_meta.get("url", ""),
                    track_meta.get("artwork", ""),
                    track_meta.get("duration", 0),
                    track_meta.get("local_path", "")
                ))
            except Exception as e:
                print(f"[add_track_to_playlist error inserting/updating track]: {e}")

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

def clear_playlist_tracks(playlist_name):
    """Removes all track associations from a playlist."""
    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM playlists WHERE name = ?", (playlist_name,))
        row = cursor.fetchone()
        if not row:
            return False
        playlist_id = row['id']
        cursor.execute("DELETE FROM playlist_tracks WHERE playlist_id = ?", (playlist_id,))
        conn.commit()
        return True

def clean_and_resync_offline_tracks(cache_dir=None):
    """
    Cleans up stale/duplicate offline tracks in SQLite database and resyncs metadata.
    Removes ghost duplicate IDs, resolves canonical 11-char YouTube IDs and file hashes,
    and ensures the 'Offline Songs' playlist contains pristine, accurate titles and artists.
    """
    import re
    import hashlib
    from utils.local_audio_utils import scan_device_offline_songs

    with DB_LOCK:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Scan candidate directories for authentic local audio tracks
        scanned_tracks = scan_device_offline_songs(cache_dir=cache_dir)
        path_to_canonical = {}
        canonical_tracks = {}

        for meta in scanned_tracks:
            c_id = meta["video_id"]
            abs_p = meta.get("local_path", "")
            norm_p = os.path.normcase(os.path.abspath(abs_p)) if abs_p else ""
            if norm_p:
                path_to_canonical[norm_p] = c_id
            if c_id not in canonical_tracks:
                canonical_tracks[c_id] = meta

        # 2. Inspect existing database records and remove stale/duplicate rows
        cursor.execute("SELECT video_id, local_path FROM tracks WHERE local_path IS NOT NULL AND local_path != ''")
        existing_rows = cursor.fetchall()

        for row in existing_rows:
            vid = row['video_id']
            lp = row['local_path']
            norm_lp = os.path.normcase(os.path.abspath(lp)) if lp else ""

            if norm_lp in path_to_canonical:
                canon_id = path_to_canonical[norm_lp]
                if vid != canon_id:
                    cursor.execute("DELETE FROM playlist_tracks WHERE video_id = ?", (vid,))
                    cursor.execute("DELETE FROM tracks WHERE video_id = ?", (vid,))
            else:
                # If local file is not in scanned authentic music tracks, or missing on disk, purge stale row
                if vid.startswith("loc_") or not os.path.exists(lp):
                    cursor.execute("DELETE FROM playlist_tracks WHERE video_id = ?", (vid,))
                    cursor.execute("DELETE FROM tracks WHERE video_id = ?", (vid,))

        # 3. Upsert all canonical tracks with pristine metadata
        for cid, meta in canonical_tracks.items():
            cursor.execute('''
                INSERT INTO tracks (video_id, title, artist, url, artwork, duration, local_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(video_id) DO UPDATE SET
                    title = excluded.title,
                    artist = excluded.artist,
                    artwork = CASE WHEN excluded.artwork != '' AND excluded.artwork != 'album_art.png' THEN excluded.artwork ELSE tracks.artwork END,
                    duration = CASE WHEN excluded.duration > 0 THEN excluded.duration ELSE tracks.duration END,
                    local_path = excluded.local_path
            ''', (
                cid,
                sanitize_text(meta.get("title", "Unknown Title")),
                sanitize_text(meta.get("artist", "Unknown Artist")),
                meta.get("url", ""),
                meta.get("artwork", ""),
                meta.get("duration", 0),
                meta.get("local_path", "")
            ))

        # 4. Clean and repopulate 'Offline Songs' playlist
        cursor.execute("SELECT id FROM playlists WHERE name = 'Offline Songs'")
        p_row = cursor.fetchone()
        if not p_row:
            cursor.execute("INSERT INTO playlists (name) VALUES ('Offline Songs')")
            offline_pid = cursor.lastrowid
        else:
            offline_pid = p_row['id']

        cursor.execute("DELETE FROM playlist_tracks WHERE playlist_id = ?", (offline_pid,))
        for cid in canonical_tracks.keys():
            cursor.execute("INSERT OR IGNORE INTO playlist_tracks (playlist_id, video_id) VALUES (?, ?)", (offline_pid, cid))

        conn.commit()
    return len(canonical_tracks)
