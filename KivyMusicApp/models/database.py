"""
SQLite Persistence Layer backed by a Dedicated Single-Writer DatabaseWorker (Priority 5).

Key guarantees:
- WAL mode (`PRAGMA journal_mode = WAL`), `PRAGMA synchronous = NORMAL`,
  `PRAGMA busy_timeout = 5000`, and `PRAGMA foreign_keys = ON`.
- All SQLite mutations serialize through a single dedicated writer thread (`_WORKER`)
  inside explicit `BEGIN IMMEDIATE ... COMMIT` transactions with automatic `ROLLBACK`.
- Reads use WAL thread-local connections so background scans/writes never stall UI clicks.
- Settings updates (`set_setting` / `set_setting_async`) update an in-memory write-through
  cache optimistically on the calling thread and persist asynchronously via `_WORKER`.
- Atomic versioned schema migrations (`schema_migrations` + `PRAGMA user_version`).
- Unicode-safe `sanitize_text()` preserving Devanagari/Gurmukhi/Indic matras and combining marks.
"""

from __future__ import annotations

import atexit
import json
import functools
import os
import sqlite3
import threading
import time
from typing import Any, Dict, List, Optional

from kivy.app import App
from kivy.utils import platform

from models.db_worker import DatabaseWorker, sanitize_text
from services.logger import get_logger
from utils.content_filters import filter_tracks as _filter_tracks

logger = get_logger("Database")

DB_LOCK = threading.RLock()
CURRENT_SCHEMA_VERSION = 2

_SETTINGS_LOCK = threading.RLock()
_SETTINGS_CACHE: Dict[str, str] = {}
_SETTINGS_INITIALIZED = False


def get_db_path() -> str:
    app = App.get_running_app()
    if platform == "android" and app:
        return os.path.join(app.user_data_dir, "music_app.db")
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "music_app.db")


_WORKER = DatabaseWorker(get_db_path)


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Return a WAL-configured thread-local connection (or active writer connection if called
    from within the DatabaseWorker thread). Enforces `foreign_keys = ON` and `busy_timeout = 5000`.
    """
    if db_path:
        _WORKER.set_db_path(db_path)
    return _WORKER.get_read_connection(db_path)


get_db_connection = get_connection


def flush_db_writes(timeout: float = 5.0) -> bool:
    """Block cleanly until all queued async SQLite writes have committed to disk."""
    return _WORKER.flush(timeout=timeout)


def get_db_worker_status() -> Dict[str, Any]:
    """Return introspection status for diagnostics and tests."""
    return {
        "db_path": _WORKER.get_active_path(),
        "worker_alive": bool(_WORKER._thread and _WORKER._thread.is_alive()),
        "worker_thread_name": _WORKER._thread.name if _WORKER._thread else None,
        "pending_queue_approx": _WORKER._queue.qsize(),
        "schema_version": _read_user_version(),
    }


def _read_user_version() -> int:
    try:
        row = get_connection().execute("PRAGMA user_version").fetchone()
        return int(row[0]) if row else 0
    except Exception:
        return 0


atexit.register(flush_db_writes)


def _refresh_settings_cache_from_db(conn: sqlite3.Connection) -> None:
    global _SETTINGS_INITIALIZED
    try:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
        with _SETTINGS_LOCK:
            _SETTINGS_CACHE.clear()
            for row in rows:
                _SETTINGS_CACHE[row["key"]] = row["value"]
            _SETTINGS_INITIALIZED = True
    except Exception as exc:
        logger.warning("Failed refreshing settings cache: %s", exc)


# =============================================================================
# Atomic Versioned Schema Migrations
# =============================================================================
def init_db(db_path: Optional[str] = None):
    """Initialize SQLite schema and apply atomic versioned migrations inside DatabaseWorker."""
    if db_path:
        _WORKER.set_db_path(db_path)

    def _run_migrations(conn: sqlite3.Connection) -> None:
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA busy_timeout = 5000;")

        ver_row = conn.execute("PRAGMA user_version").fetchone()
        current_ver = int(ver_row[0]) if ver_row else 0

        # Migration v1: Ensure core tables, telemetry tables, columns, indexes, and seeds
        conn.execute("BEGIN IMMEDIATE")
        try:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    description TEXT NOT NULL,
                    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
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
            for col_stmt in [
                "ALTER TABLE tracks ADD COLUMN play_count INTEGER DEFAULT 0",
                "ALTER TABLE tracks ADD COLUMN source TEXT DEFAULT 'youtube'",
                "ALTER TABLE tracks ADD COLUMN source_id TEXT",
                "ALTER TABLE tracks ADD COLUMN bitrate INTEGER DEFAULT 128",
                "ALTER TABLE tracks ADD COLUMN isrc TEXT",
                "ALTER TABLE tracks ADD COLUMN media_type TEXT DEFAULT 'song'",
                "ALTER TABLE tracks ADD COLUMN album TEXT",
                "ALTER TABLE tracks ADD COLUMN genre TEXT",
                "ALTER TABLE tracks ADD COLUMN release_date TEXT",
                "ALTER TABLE tracks ADD COLUMN description TEXT",
                "ALTER TABLE tracks ADD COLUMN view_count INTEGER DEFAULT 0",
                "ALTER TABLE tracks ADD COLUMN like_count INTEGER DEFAULT 0",
                "ALTER TABLE tracks ADD COLUMN channel TEXT",
                "ALTER TABLE tracks ADD COLUMN channel_id TEXT",
                "ALTER TABLE tracks ADD COLUMN chapters TEXT",
                "ALTER TABLE tracks ADD COLUMN track_number INTEGER DEFAULT 0",
            ]:
                try:
                    conn.execute(col_stmt)
                except Exception:
                    pass

            conn.execute('''
                CREATE TABLE IF NOT EXISTS playlists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS playlist_tracks (
                    playlist_id INTEGER,
                    video_id TEXT,
                    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
                    FOREIGN KEY(video_id) REFERENCES tracks(video_id) ON DELETE CASCADE,
                    UNIQUE(playlist_id, video_id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    query TEXT UNIQUE NOT NULL,
                    searched_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            for k, v in [
                ("theme_style", "Light"),
                ("wifi_only", "False"),
                ("extract_artwork_colors", "True"),
                ("animated_bg_enabled", "True"),
                ("sponsorblock_enabled", "True"),
                ("crossfade_duration", "3"),
                ("autoeq_profile", "None"),
                ("lyrics_offset", "0.0"),
            ]:
                conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))

            conn.execute('''
                CREATE TABLE IF NOT EXISTS cache_store (
                    cache_key TEXT PRIMARY KEY,
                    payload TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS listening_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT NOT NULL,
                    event_type TEXT NOT NULL DEFAULT 'play',
                    listened_seconds REAL DEFAULT 0.0,
                    track_duration REAL DEFAULT 0.0,
                    occurred_at REAL NOT NULL
                )
            ''')
            conn.execute("CREATE INDEX IF NOT EXISTS idx_listening_events_vid_time ON listening_events(video_id, occurred_at)")

            conn.execute('''
                CREATE TABLE IF NOT EXISTS trend_observations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT NOT NULL,
                    source TEXT NOT NULL DEFAULT 'unknown',
                    popularity_metric REAL NOT NULL DEFAULT 0.0,
                    chart_rank INTEGER DEFAULT 0,
                    observed_at REAL NOT NULL
                )
            ''')
            conn.execute("CREATE INDEX IF NOT EXISTS idx_trend_obs_vid_time ON trend_observations(video_id, observed_at)")

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
                ("Late Night",),
                ("Podcasts",),
            ]
            conn.executemany("INSERT OR IGNORE INTO playlists (name) VALUES (?)", dynamic_seed_playlists)

            # Podcast classification hygiene pass
            try:
                existing_rows = conn.execute(
                    "SELECT video_id, title, artist, duration, media_type FROM tracks"
                ).fetchall()
                from utils.media_utils import is_podcast_item
                for row in existing_rows:
                    row_dict = dict(row)
                    if is_podcast_item(row_dict):
                        if row_dict.get("media_type") != "podcast":
                            conn.execute("UPDATE tracks SET media_type = 'podcast' WHERE video_id = ?", (row["video_id"],))
                    elif row_dict.get("media_type") == "podcast":
                        conn.execute("UPDATE tracks SET media_type = 'song' WHERE video_id = ?", (row["video_id"],))

                conn.execute('''
                    DELETE FROM playlist_tracks
                    WHERE playlist_id IN (SELECT id FROM playlists WHERE name != 'Podcasts')
                      AND video_id IN (SELECT video_id FROM tracks WHERE media_type = 'podcast')
                ''')
            except Exception as e:
                logger.warning("Error running podcast separation migration: %s", e)

            # Seed sample tracks if playlist_tracks empty
            cnt_row = conn.execute("SELECT COUNT(*) FROM playlist_tracks").fetchone()
            if cnt_row and cnt_row[0] == 0:
                sample_vids = [
                    r[0] for r in conn.execute(
                        "SELECT video_id FROM tracks WHERE media_type = 'song' OR media_type IS NULL OR media_type = '' LIMIT 4"
                    ).fetchall()
                ]
                if sample_vids:
                    for pl_name in ("Favorites", "Chillwave", "Late Night", "Workout"):
                        prow = conn.execute("SELECT id FROM playlists WHERE name = ?", (pl_name,)).fetchone()
                        if prow:
                            pid = prow[0]
                            for vid in sample_vids:
                                conn.execute(
                                    "INSERT OR IGNORE INTO playlist_tracks (playlist_id, video_id) VALUES (?, ?)",
                                    (pid, vid),
                                )

            if current_ver < 1:
                conn.execute(
                    "INSERT OR IGNORE INTO schema_migrations (version, description) VALUES (1, 'Initial schema & telemetry tables')"
                )
                conn.execute("PRAGMA user_version = 1")
                current_ver = 1
            conn.execute("COMMIT")
        except Exception:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise

        # Migration v2: Upgrade legacy playlist_tracks to ON DELETE CASCADE & scrub orphans atomically
        ddl_row = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='playlist_tracks'"
        ).fetchone()
        ddl_sql = (ddl_row[0] if ddl_row and ddl_row[0] else "").upper()
        needs_fk_rebuild = ("ON DELETE CASCADE" not in ddl_sql) or (current_ver < 2)

        if needs_fk_rebuild:
            # PRAGMA foreign_keys MUST be toggled outside an active transaction in SQLite
            conn.execute("PRAGMA foreign_keys = OFF;")
            conn.execute("BEGIN IMMEDIATE")
            try:
                conn.execute('''
                    DELETE FROM playlist_tracks
                    WHERE playlist_id NOT IN (SELECT id FROM playlists)
                       OR video_id NOT IN (SELECT video_id FROM tracks)
                ''')
                if "ON DELETE CASCADE" not in ddl_sql:
                    conn.execute('''
                        CREATE TABLE playlist_tracks_new (
                            playlist_id INTEGER NOT NULL,
                            video_id TEXT NOT NULL,
                            added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
                            FOREIGN KEY(video_id) REFERENCES tracks(video_id) ON DELETE CASCADE,
                            UNIQUE(playlist_id, video_id)
                        )
                    ''')
                    conn.execute('''
                        INSERT OR IGNORE INTO playlist_tracks_new (playlist_id, video_id, added_at)
                        SELECT pt.playlist_id, pt.video_id, pt.added_at
                        FROM playlist_tracks pt
                        JOIN playlists p ON p.id = pt.playlist_id
                        JOIN tracks t ON t.video_id = pt.video_id
                    ''')
                    conn.execute("DROP TABLE playlist_tracks")
                    conn.execute("ALTER TABLE playlist_tracks_new RENAME TO playlist_tracks")

                conn.execute(
                    "INSERT OR IGNORE INTO schema_migrations (version, description) VALUES (2, 'Enforce ON DELETE CASCADE FKs on playlist_tracks')"
                )
                conn.execute("PRAGMA user_version = 2")
                conn.execute("COMMIT")
            except Exception:
                if conn.in_transaction:
                    conn.execute("ROLLBACK")
                raise
            finally:
                conn.execute("PRAGMA foreign_keys = ON;")
        else:
            conn.execute("PRAGMA foreign_keys = ON;")

        # Populate optimistic settings cache cleanly
        _refresh_settings_cache_from_db(conn)

    _WORKER.submit_write(_run_migrations, wait=True, transactional=False)


# =============================================================================
# Track CRUD Operations (Dedicated Single-Writer + WAL Reads)
# =============================================================================
def _write_add_track(conn: sqlite3.Connection, payload: tuple) -> None:
    conn.execute('''
        INSERT INTO tracks (
            video_id, title, artist, url, local_path, duration, artwork,
            source, source_id, bitrate, isrc, media_type, album, genre,
            release_date, description, view_count, like_count, channel,
            channel_id, chapters, track_number
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            isrc=CASE WHEN excluded.isrc != '' THEN excluded.isrc ELSE tracks.isrc END,
            media_type=CASE WHEN excluded.media_type != '' THEN excluded.media_type ELSE tracks.media_type END,
            album=CASE WHEN excluded.album != '' THEN excluded.album ELSE tracks.album END,
            genre=CASE WHEN excluded.genre != '' THEN excluded.genre ELSE tracks.genre END,
            release_date=CASE WHEN excluded.release_date != '' THEN excluded.release_date ELSE tracks.release_date END,
            description=CASE WHEN excluded.description != '' THEN excluded.description ELSE tracks.description END,
            view_count=CASE WHEN excluded.view_count > 0 THEN excluded.view_count ELSE tracks.view_count END,
            like_count=CASE WHEN excluded.like_count > 0 THEN excluded.like_count ELSE tracks.like_count END,
            channel=CASE WHEN excluded.channel != '' THEN excluded.channel ELSE tracks.channel END,
            channel_id=CASE WHEN excluded.channel_id != '' THEN excluded.channel_id ELSE tracks.channel_id END,
            chapters=CASE WHEN excluded.chapters != '' THEN excluded.chapters ELSE tracks.chapters END,
            track_number=CASE WHEN excluded.track_number > 0 THEN excluded.track_number ELSE tracks.track_number END
    ''', payload)


def _prepare_track_tuple(
    video_id, title, artist, url, duration=0, artwork="", local_path="",
    source="youtube", source_id="", bitrate=128, isrc="", media_type="song",
    album="", genre="", release_date="", description="", view_count=0,
    like_count=0, channel="", channel_id="", chapters="", track_number=0
) -> tuple:
    clean_title = sanitize_text(title)
    clean_artist = sanitize_text(artist)
    from utils.media_utils import is_podcast_item
    if media_type == "song" and is_podcast_item({"title": title, "artist": artist, "duration": duration}):
        media_type = "podcast"
    return (
        video_id, clean_title, clean_artist, url, local_path, duration, artwork,
        source, source_id, bitrate, isrc, media_type, album, genre,
        release_date, description, view_count, like_count, channel,
        channel_id, chapters, track_number,
    )


def add_track(
    video_id, title, artist, url, duration=0, artwork="", local_path="",
    source="youtube", source_id="", bitrate=128, isrc="", media_type="song",
    album="", genre="", release_date="", description="", view_count=0,
    like_count=0, channel="", channel_id="", chapters="", track_number=0
):
    """Inserts or updates a track record via the single-writer DatabaseWorker."""
    payload = _prepare_track_tuple(
        video_id, title, artist, url, duration, artwork, local_path,
        source, source_id, bitrate, isrc, media_type, album, genre,
        release_date, description, view_count, like_count, channel,
        channel_id, chapters, track_number,
    )
    try:
        _WORKER.submit_write(lambda conn: _write_add_track(conn, payload), wait=True)
    except Exception as e:
        logger.error("Database error in add_track: %s", e)


def add_track_async(
    video_id, title, artist, url, duration=0, artwork="", local_path="",
    source="youtube", source_id="", bitrate=128, isrc="", media_type="song",
    album="", genre="", release_date="", description="", view_count=0,
    like_count=0, channel="", channel_id="", chapters="", track_number=0
):
    """Non-blocking track upsert queued onto DatabaseWorker."""
    payload = _prepare_track_tuple(
        video_id, title, artist, url, duration, artwork, local_path,
        source, source_id, bitrate, isrc, media_type, album, genre,
        release_date, description, view_count, like_count, channel,
        channel_id, chapters, track_number,
    )
    return _WORKER.submit_write(lambda conn: _write_add_track(conn, payload), wait=False)


def get_all_tracks(media_type="song"):
    """Retrieves tracks stored in database filtered by media_type ('song', 'podcast', 'all')."""
    conn = get_connection()
    cols = (
        "video_id, title, artist, url, local_path, duration, artwork, source, "
        "source_id, bitrate, isrc, media_type, album, genre, release_date, "
        "description, view_count, like_count, channel, channel_id, chapters, track_number"
    )
    if media_type == "all":
        cur = conn.execute(f"SELECT {cols} FROM tracks ORDER BY added_at DESC")
    elif media_type == "podcast":
        cur = conn.execute(f"SELECT {cols} FROM tracks WHERE media_type = 'podcast' ORDER BY added_at DESC")
    else:
        cur = conn.execute(
            f"SELECT {cols} FROM tracks WHERE media_type = 'song' OR media_type IS NULL OR media_type = '' ORDER BY added_at DESC"
        )
    return [dict(row) for row in cur.fetchall()]


def get_all_podcasts():
    """Retrieves all podcast episodes stored in the database."""
    return get_all_tracks(media_type="podcast")


def get_track(video_id):
    """Retrieves metadata for a specific track by video ID."""
    conn = get_connection()
    cols = (
        "video_id, title, artist, url, local_path, duration, artwork, source, "
        "source_id, bitrate, isrc, media_type, album, genre, release_date, "
        "description, view_count, like_count, channel, channel_id, chapters, track_number"
    )
    row = conn.execute(f"SELECT {cols} FROM tracks WHERE video_id = ?", (video_id,)).fetchone()
    return dict(row) if row else None


def get_library_analytics_summary() -> Dict[str, Any]:
    """Read-only WAL snapshot query returning library summary metrics for AnalyticsScreen."""
    conn = get_connection()
    total_tracks = (conn.execute("SELECT COUNT(*) FROM tracks").fetchone() or [0])[0] or 0
    total_artists = (
        conn.execute("SELECT COUNT(DISTINCT artist) FROM tracks WHERE artist IS NOT NULL AND artist != ''").fetchone()
        or [0]
    )[0] or 0
    total_sec = (
        conn.execute("SELECT SUM(duration) FROM tracks WHERE duration IS NOT NULL").fetchone() or [0]
    )[0] or 0
    row = conn.execute(
        "SELECT title, artist FROM tracks WHERE last_played IS NOT NULL ORDER BY last_played DESC LIMIT 1"
    ).fetchone()
    if not row:
        row = conn.execute("SELECT title, artist FROM tracks LIMIT 1").fetchone()
    top_artists_rows = conn.execute('''
        SELECT artist, COUNT(*) as c
        FROM tracks
        WHERE artist IS NOT NULL AND artist != '' AND artist != 'Unknown Artist'
        GROUP BY artist
        ORDER BY c DESC
        LIMIT 3
    ''').fetchall()
    dow_rows = conn.execute(
        "SELECT strftime('%w', last_played) as dow, COUNT(*) as c FROM tracks WHERE last_played IS NOT NULL GROUP BY dow"
    ).fetchall()
    return {
        "total_tracks": int(total_tracks),
        "total_artists": int(total_artists),
        "total_seconds": int(total_sec),
        "top_track": dict(row) if row else None,
        "top_artists": [dict(r) for r in top_artists_rows],
        "dow_counts": {str(r[0]): r[1] for r in dow_rows},
    }


def update_local_track_path(video_id, local_path, duration=None, wait: bool = False):
    """Updates local file path and duration once an asset is cached on disk."""
    def _write(conn: sqlite3.Connection):
        if duration is not None and duration > 0:
            conn.execute(
                "UPDATE tracks SET local_path = ?, duration = ? WHERE video_id = ?",
                (local_path, duration, video_id),
            )
        else:
            conn.execute(
                "UPDATE tracks SET local_path = ? WHERE video_id = ?",
                (local_path, video_id),
            )
    return _WORKER.submit_write(_write, wait=wait)


def update_track_artwork(video_id, artwork_path, wait: bool = False):
    """Updates the artwork path for a track in the database."""
    return _WORKER.submit_write(
        lambda conn: conn.execute("UPDATE tracks SET artwork = ? WHERE video_id = ?", (artwork_path, video_id)),
        wait=wait,
    )


def mark_track_played(video_id, listened_seconds=0.0, track_duration=0.0, event_type="play", wait: bool = True):
    """Records play timestamp, increments play_count, and logs an event into listening_events."""
    if not video_id:
        return None
    now_ep = time.time()

    def _write(conn: sqlite3.Connection):
        conn.execute(
            '''
            UPDATE tracks
            SET last_played = CURRENT_TIMESTAMP,
                play_count = COALESCE(play_count, 0) + 1
            WHERE video_id = ?
            ''',
            (video_id,),
        )
        conn.execute(
            '''
            INSERT INTO listening_events (video_id, event_type, listened_seconds, track_duration, occurred_at)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (video_id, str(event_type or "play"), float(listened_seconds or 0.0), float(track_duration or 0.0), now_ep),
        )

    return _WORKER.submit_write(_write, wait=wait)


def mark_track_played_async(video_id, listened_seconds=0.0, track_duration=0.0, event_type="play"):
    return mark_track_played(
        video_id,
        listened_seconds=listened_seconds,
        track_duration=track_duration,
        event_type=event_type,
        wait=False,
    )


def record_track_skip(video_id, listened_seconds=0.0, track_duration=0.0, wait: bool = True):
    """Records a user skip event into listening_events for recommendation anti-fatigue ranking."""
    if not video_id:
        return None
    now_ep = time.time()
    return _WORKER.submit_write(
        lambda conn: conn.execute(
            '''
            INSERT INTO listening_events (video_id, event_type, listened_seconds, track_duration, occurred_at)
            VALUES (?, 'skip', ?, ?, ?)
            ''',
            (video_id, float(listened_seconds or 0.0), float(track_duration or 0.0), now_ep),
        ),
        wait=wait,
    )


def record_track_skip_async(video_id, listened_seconds=0.0, track_duration=0.0):
    return record_track_skip(video_id, listened_seconds=listened_seconds, track_duration=track_duration, wait=False)


def get_listening_event_stats():
    """Aggregates per-track play counts, skip counts, and listening time from listening_events."""
    conn = get_connection()
    try:
        rows = conn.execute('''
            SELECT video_id,
                   SUM(CASE WHEN event_type IN ('play', 'complete') THEN 1 ELSE 0 END) AS play_count,
                   SUM(CASE WHEN event_type = 'skip' THEN 1 ELSE 0 END) AS skip_count,
                   SUM(COALESCE(listened_seconds, 0.0)) AS total_listen_seconds,
                   MAX(occurred_at) AS last_event_epoch
            FROM listening_events
            GROUP BY video_id
        ''').fetchall()
        return {row["video_id"]: dict(row) for row in rows}
    except Exception:
        return {}


def get_top_genres(limit=10):
    """Aggregates preferred genres from played library tracks weighted by play_count."""
    conn = get_connection()
    try:
        rows = conn.execute(
            '''
            SELECT genre, SUM(COALESCE(play_count, 1)) AS weight
            FROM tracks
            WHERE genre IS NOT NULL AND genre != ''
            GROUP BY genre
            ORDER BY weight DESC
            LIMIT ?
            ''',
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
    except Exception:
        return []


def record_trend_observations(entries, observed_at=None, default_source="unknown", wait: bool = True):
    """Persists timestamped popularity observations into `trend_observations`."""
    if not entries:
        return 0
    ts = float(observed_at if observed_at is not None else time.time())
    rows = []
    for idx, item in enumerate(entries):
        if not item or not isinstance(item, dict):
            continue
        vid = str(item.get("video_id") or "").strip()
        if not vid:
            continue
        rank = int(item.get("chart_rank") or (idx + 1))
        views = float(item.get("view_count") or 0.0)
        metric = views if views > 0 else float(max(1, 51 - rank) * 100)
        src = str(item.get("source") or default_source)
        rows.append((vid, src, metric, rank, ts))
    if not rows:
        return 0

    def _write(conn: sqlite3.Connection) -> int:
        conn.executemany(
            '''
            INSERT INTO trend_observations (video_id, source, popularity_metric, chart_rank, observed_at)
            VALUES (?, ?, ?, ?, ?)
            ''',
            rows,
        )
        cutoff = ts - (14 * 86400.0)
        conn.execute("DELETE FROM trend_observations WHERE observed_at < ?", (cutoff,))
        return len(rows)

    try:
        return _WORKER.submit_write(_write, wait=wait)
    except Exception as exc:
        logger.warning("record_trend_observations error: %s", exc)
        return 0


def get_trending_velocity_map(min_dt_seconds=60.0):
    """Computes per-track multi-timestamp trending velocity [0.0, 1.0] from trend_observations."""
    from services.recommendation_scoring import compute_trending_velocity
    conn = get_connection()
    try:
        rows = conn.execute('''
            SELECT video_id, observed_at, popularity_metric
            FROM trend_observations
            ORDER BY video_id ASC, observed_at ASC
        ''').fetchall()
        grouped: Dict[str, List[Any]] = {}
        for row in rows:
            grouped.setdefault(row["video_id"], []).append((row["observed_at"], row["popularity_metric"]))
        return {
            vid: compute_trending_velocity(obs, min_dt_seconds=min_dt_seconds)
            for vid, obs in grouped.items()
        }
    except Exception:
        return {}


# =============================================================================
# Behavioral Playlist Read Queries (Non-Blocking WAL Reads)
# =============================================================================
def get_on_repeat(limit=25, media_type="song"):
    conn = get_connection()
    m_filter = (
        "AND (media_type = 'song' OR media_type IS NULL OR media_type = '')"
        if media_type == "song"
        else ("AND media_type = 'podcast'" if media_type == "podcast" else "")
    )
    rows = conn.execute(
        f'''
        SELECT video_id, title, artist, url, local_path, duration, artwork,
               COALESCE(play_count, 0) as play_count, last_played, genre, view_count, media_type
        FROM tracks
        WHERE play_count >= 2 {m_filter}
        ORDER BY play_count DESC, last_played DESC
        LIMIT ?
        ''',
        (limit,),
    ).fetchall()
    out = [dict(r) for r in rows]
    if len(out) < 3:
        return get_recently_played(limit=limit, media_type=media_type)
    return out


def get_heavy_rotation(limit=25, media_type="song"):
    conn = get_connection()
    m_filter = (
        "WHERE (media_type = 'song' OR media_type IS NULL OR media_type = '')"
        if media_type == "song"
        else ("WHERE media_type = 'podcast'" if media_type == "podcast" else "")
    )
    rows = conn.execute(
        f'''
        SELECT video_id, title, artist, url, local_path, duration, artwork,
               COALESCE(play_count, 0) as play_count, last_played, genre, view_count, media_type
        FROM tracks
        {m_filter}
        ORDER BY play_count DESC, added_at DESC
        LIMIT ?
        ''',
        (limit,),
    ).fetchall()
    return [dict(r) for r in rows]


def get_forgotten_favorites(limit=25, media_type="song"):
    conn = get_connection()
    m_filter = (
        "AND (t.media_type = 'song' OR t.media_type IS NULL OR t.media_type = '')"
        if media_type == "song"
        else ("AND t.media_type = 'podcast'" if media_type == "podcast" else "")
    )
    rows = conn.execute(
        f'''
        SELECT t.video_id, t.title, t.artist, t.url, t.local_path, t.duration, t.artwork,
               1 as is_favorite, t.last_played, t.genre, t.view_count, t.media_type
        FROM playlist_tracks pt
        JOIN playlists p ON pt.playlist_id = p.id
        JOIN tracks t ON pt.video_id = t.video_id
        WHERE p.name = 'Favorites' {m_filter}
        ORDER BY CASE WHEN t.last_played IS NULL THEN 0 ELSE 1 END ASC, t.last_played ASC
        LIMIT ?
        ''',
        (limit,),
    ).fetchall()
    return [dict(r) for r in rows]


def get_daily_mix(limit=25, media_type="song"):
    conn = get_connection()
    m_filter = "AND (media_type = 'song' OR media_type IS NULL OR media_type = '')" if media_type == "song" else ""
    top_artists = [
        r[0]
        for r in conn.execute(
            f'''
            SELECT artist, SUM(COALESCE(play_count, 1)) as weight
            FROM tracks
            WHERE artist IS NOT NULL AND artist != '' AND artist != 'Unknown Artist' {m_filter}
            GROUP BY artist
            ORDER BY weight DESC
            LIMIT 3
            '''
        ).fetchall()
    ]
    mix_tracks = []
    if top_artists:
        placeholders = ",".join("?" for _ in top_artists)
        rows = conn.execute(
            f'''
            SELECT video_id, title, artist, url, local_path, duration, artwork,
                   COALESCE(play_count, 0) as play_count, last_played, genre, view_count, media_type
            FROM tracks
            WHERE artist IN ({placeholders}) {m_filter}
            ORDER BY RANDOM()
            LIMIT ?
            ''',
            (*top_artists, limit),
        ).fetchall()
        mix_tracks = [dict(r) for r in rows]

    if len(mix_tracks) < 5:
        rows = conn.execute(
            f'''
            SELECT video_id, title, artist, url, local_path, duration, artwork,
                   COALESCE(play_count, 0) as play_count, last_played, genre, view_count, media_type
            FROM tracks
            WHERE 1=1 {m_filter}
            ORDER BY added_at DESC
            LIMIT ?
            ''',
            (limit,),
        ).fetchall()
        mix_tracks = [dict(r) for r in rows]
    return mix_tracks


def get_top_artists(limit=10, media_type="song"):
    conn = get_connection()
    m_filter = (
        "AND (media_type = 'song' OR media_type IS NULL OR media_type = '')"
        if media_type == "song"
        else ("AND media_type = 'podcast'" if media_type == "podcast" else "")
    )
    rows = conn.execute(
        f'''
        SELECT artist, COUNT(*) as track_count, SUM(COALESCE(play_count, 0)) as total_plays
        FROM tracks
        WHERE artist IS NOT NULL AND artist != '' AND artist != 'Unknown' AND artist != 'Unknown Artist' {m_filter}
        GROUP BY artist
        ORDER BY total_plays DESC, track_count DESC
        LIMIT ?
        ''',
        (limit,),
    ).fetchall()
    return [dict(r) for r in rows]


def get_local_library_tracks(limit=25, media_type="song"):
    conn = get_connection()
    m_filter = (
        "AND (media_type = 'song' OR media_type IS NULL OR media_type = '')"
        if media_type == "song"
        else ("AND media_type = 'podcast'" if media_type == "podcast" else "")
    )
    rows = conn.execute(
        f'''
        SELECT video_id, title, artist, url, local_path, duration, artwork,
               COALESCE(play_count, 0) as play_count, last_played, genre, view_count, media_type
        FROM tracks
        WHERE local_path IS NOT NULL AND local_path != '' {m_filter}
        ORDER BY last_played DESC, added_at DESC
        LIMIT ?
        ''',
        (limit,),
    ).fetchall()
    return [dict(r) for r in rows]


def get_dynamic_playlist_tracks(playlist_name: str, limit: int = 25):
    clean_name = playlist_name.strip()
    if clean_name == "On Repeat":
        return get_on_repeat(limit=limit)
    elif clean_name == "Heavy Rotation":
        return get_heavy_rotation(limit=limit)
    elif clean_name == "Forgotten Favorites":
        return get_forgotten_favorites(limit=limit)
    elif clean_name == "Your Daily Mix":
        return get_daily_mix(limit=limit)
    try:
        from services.recommendation_engine import DynamicRecommendationEngine
        return DynamicRecommendationEngine().get_dynamic_playlist(clean_name, limit=limit)
    except Exception:
        return None


def get_recently_played(limit=10, media_type="song"):
    conn = get_connection()
    m_filter = (
        "AND (media_type = 'song' OR media_type IS NULL OR media_type = '')"
        if media_type == "song"
        else ("AND media_type = 'podcast'" if media_type == "podcast" else "")
    )
    rows = conn.execute(
        f'''
        SELECT video_id, title, artist, url, local_path, duration, artwork,
               COALESCE(play_count, 0) as play_count, last_played, genre, view_count, media_type
        FROM tracks
        WHERE last_played IS NOT NULL {m_filter}
        ORDER BY last_played DESC
        LIMIT ?
        ''',
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


def get_continue_listening(limit=5, media_type="song"):
    return get_recently_played(limit=limit, media_type=media_type)


def get_recently_added(limit=10, media_type="song"):
    conn = get_connection()
    m_filter = (
        "WHERE (media_type = 'song' OR media_type IS NULL OR media_type = '')"
        if media_type == "song"
        else ("WHERE media_type = 'podcast'" if media_type == "podcast" else "")
    )
    rows = conn.execute(
        f'''
        SELECT video_id, title, artist, url, local_path, duration, artwork, media_type
        FROM tracks
        {m_filter}
        ORDER BY added_at DESC
        LIMIT ?
        ''',
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


# =============================================================================
# Playlist & Settings & Cache Store Operations
# =============================================================================
def get_all_playlists():
    conn = get_connection()
    rows = conn.execute('''
        SELECT p.id, p.name, COUNT(pt.video_id) as track_count
        FROM playlists p
        LEFT JOIN playlist_tracks pt ON p.id = pt.playlist_id
        GROUP BY p.id, p.name
        ORDER BY p.name ASC
    ''').fetchall()
    return [dict(row) for row in rows]


def get_playlist_covers():
    conn = get_connection()
    rows = conn.execute('''
        SELECT name, artwork FROM (
            SELECT p.name AS name,
                   t.artwork AS artwork,
                   ROW_NUMBER() OVER (PARTITION BY p.id ORDER BY pt.added_at DESC) AS rn
            FROM playlists p
            LEFT JOIN playlist_tracks pt ON pt.playlist_id = p.id
            LEFT JOIN tracks t ON t.video_id = pt.video_id
        ) WHERE rn = 1
    ''').fetchall()
    return {row["name"]: row["artwork"] or "" for row in rows}


def add_playlist(name):
    clean_name = sanitize_text(name)
    if not clean_name:
        return None

    def _write(conn: sqlite3.Connection):
        try:
            cur = conn.execute("INSERT INTO playlists (name) VALUES (?)", (clean_name,))
            return cur.lastrowid
        except sqlite3.IntegrityError:
            return None

    return _WORKER.submit_write(_write, wait=True)


def delete_playlist(name):
    def _write(conn: sqlite3.Connection) -> bool:
        row = conn.execute("SELECT id FROM playlists WHERE name = ?", (name,)).fetchone()
        if not row:
            return False
        pid = row["id"]
        conn.execute("DELETE FROM playlist_tracks WHERE playlist_id = ?", (pid,))
        conn.execute("DELETE FROM playlists WHERE id = ?", (pid,))
        return True

    return _WORKER.submit_write(_write, wait=True)


def get_playlist_tracks(playlist_name, media_type=None):
    conn = get_connection()
    clean_name = playlist_name.strip() if playlist_name else ""
    if clean_name == "Podcasts" or media_type == "podcast":
        type_filter = "AND t.media_type = 'podcast'"
    elif media_type == "all":
        type_filter = ""
    else:
        type_filter = "AND (t.media_type = 'song' OR t.media_type IS NULL OR t.media_type = '')"

    rows = conn.execute(
        f'''
        SELECT t.video_id, t.title, t.artist, t.url, t.local_path, t.duration, t.artwork,
               t.source, t.source_id, t.bitrate, t.isrc, t.media_type, t.album, t.genre,
               t.release_date, t.description, t.view_count, t.like_count, t.channel,
               t.channel_id, t.chapters, t.track_number,
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
        WHERE p.name = ? {type_filter}
        ORDER BY pt.rowid ASC
        ''',
        (clean_name,),
    ).fetchall()
    return [dict(row) for row in rows]


def get_setting(key, default=None):
    """Retrieve setting using optimistic write-through cache backed by WAL SQLite reads."""
    with _SETTINGS_LOCK:
        if key in _SETTINGS_CACHE:
            return _SETTINGS_CACHE[key]
    conn = get_connection()
    try:
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        if row is not None:
            val = row[0]
            with _SETTINGS_LOCK:
                _SETTINGS_CACHE[key] = val
            return val
        return default
    except Exception as e:
        logger.warning("get_setting error for '%s': %s", key, e)
        return default


def set_setting(key, value, flush: bool = False):
    """
    Optimistically updates the in-memory settings state and persists asynchronously
    via the dedicated DatabaseWorker (zero blocking on the Kivy UI thread).
    """
    val_str = str(value) if value is not None else ""
    with _SETTINGS_LOCK:
        _SETTINGS_CACHE[key] = val_str

    def _write(conn: sqlite3.Connection) -> bool:
        conn.execute(
            '''
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            ''',
            (key, val_str),
        )
        return True

    try:
        res = _WORKER.submit_write(_write, wait=bool(flush))
        return bool(res) if flush else True
    except Exception as e:
        logger.warning("set_setting error for '%s': %s", key, e)
        return False


set_setting_async = set_setting


def get_all_settings():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
        merged = {row[0]: row[1] for row in rows}
    except Exception:
        merged = {}
    with _SETTINGS_LOCK:
        merged.update(_SETTINGS_CACHE)
    return merged


def save_cache_payload(cache_key, payload_dict, wait: bool = False):
    try:
        payload_str = json.dumps(payload_dict)
    except Exception as e:
        logger.warning("save_cache_payload serialization error for '%s': %s", cache_key, e)
        return False

    def _write(conn: sqlite3.Connection) -> bool:
        conn.execute(
            '''
            INSERT INTO cache_store (cache_key, payload, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(cache_key) DO UPDATE SET payload = excluded.payload, updated_at = CURRENT_TIMESTAMP
            ''',
            (cache_key, payload_str),
        )
        return True

    try:
        res = _WORKER.submit_write(_write, wait=wait)
        return bool(res) if wait else True
    except Exception as e:
        logger.warning("save_cache_payload error for '%s': %s", cache_key, e)
        return False


def load_cache_payload(cache_key, default=None):
    conn = get_connection()
    try:
        row = conn.execute("SELECT payload FROM cache_store WHERE cache_key = ?", (cache_key,)).fetchone()
        if row and row[0]:
            return json.loads(row[0])
    except Exception as e:
        logger.warning("load_cache_payload error for '%s': %s", cache_key, e)
    return default


def add_track_to_playlist(playlist_name, video_id, track_meta=None):
    """Adds a track to a playlist atomically within DatabaseWorker, preserving FK integrity."""
    def _write(conn: sqlite3.Connection) -> bool:
        if track_meta and video_id:
            conn.execute(
                '''
                INSERT INTO tracks (video_id, title, artist, url, artwork, duration, local_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(video_id) DO UPDATE SET
                    title = excluded.title,
                    artist = excluded.artist,
                    url = CASE WHEN excluded.url != '' THEN excluded.url ELSE tracks.url END,
                    artwork = CASE WHEN excluded.artwork != '' AND excluded.artwork != 'album_art.png' THEN excluded.artwork ELSE tracks.artwork END,
                    duration = CASE WHEN excluded.duration > 0 THEN excluded.duration ELSE tracks.duration END,
                    local_path = CASE WHEN excluded.local_path != '' THEN excluded.local_path ELSE tracks.local_path END
                ''',
                (
                    video_id,
                    sanitize_text(track_meta.get("title", "Unknown Title")),
                    sanitize_text(track_meta.get("artist", "Unknown Artist")),
                    track_meta.get("url", ""),
                    track_meta.get("artwork", ""),
                    track_meta.get("duration", 0),
                    track_meta.get("local_path", ""),
                ),
            )

        row = conn.execute("SELECT id FROM playlists WHERE name = ?", (playlist_name,)).fetchone()
        if not row:
            cur = conn.execute("INSERT INTO playlists (name) VALUES (?)", (playlist_name,))
            playlist_id = cur.lastrowid
        else:
            playlist_id = row["id"]

        conn.execute(
            "INSERT OR IGNORE INTO playlist_tracks (playlist_id, video_id) VALUES (?, ?)",
            (playlist_id, video_id),
        )
        return True

    try:
        return bool(_WORKER.submit_write(_write, wait=True))
    except Exception as e:
        logger.error("add_track_to_playlist error (%s -> %s): %s", video_id, playlist_name, e)
        return False


def remove_track_from_playlist(playlist_name, video_id):
    def _write(conn: sqlite3.Connection) -> bool:
        row = conn.execute("SELECT id FROM playlists WHERE name = ?", (playlist_name,)).fetchone()
        if not row:
            return False
        conn.execute(
            "DELETE FROM playlist_tracks WHERE playlist_id = ? AND video_id = ?",
            (row["id"], video_id),
        )
        return True

    return bool(_WORKER.submit_write(_write, wait=True))


def is_favorite(video_id):
    conn = get_connection()
    row = conn.execute(
        '''
        SELECT 1
        FROM playlist_tracks pt
        JOIN playlists p ON pt.playlist_id = p.id
        WHERE p.name = 'Favorites' AND pt.video_id = ?
        ''',
        (video_id,),
    ).fetchone()
    return row is not None


def toggle_favorite(video_id):
    """Toggles favorite status atomically in DatabaseWorker and returns the new status."""
    def _write(conn: sqlite3.Connection) -> bool:
        row = conn.execute("SELECT id FROM playlists WHERE name = 'Favorites'").fetchone()
        if not row:
            fav_id = conn.execute("INSERT INTO playlists (name) VALUES ('Favorites')").lastrowid
        else:
            fav_id = row["id"]

        is_fav = (
            conn.execute(
                "SELECT 1 FROM playlist_tracks WHERE playlist_id = ? AND video_id = ?",
                (fav_id, video_id),
            ).fetchone()
            is not None
        )
        if is_fav:
            conn.execute(
                "DELETE FROM playlist_tracks WHERE playlist_id = ? AND video_id = ?",
                (fav_id, video_id),
            )
            return False
        conn.execute(
            "INSERT INTO playlist_tracks (playlist_id, video_id) VALUES (?, ?)",
            (fav_id, video_id),
        )
        return True

    return bool(_WORKER.submit_write(_write, wait=True))


def add_search_history(query, wait: bool = True):
    clean_query = str(query).strip()
    if not clean_query:
        return None
    return _WORKER.submit_write(
        lambda conn: conn.execute(
            "INSERT OR REPLACE INTO search_history (query, searched_at) VALUES (?, CURRENT_TIMESTAMP)",
            (clean_query,),
        ),
        wait=wait,
    )


def add_search_history_async(query):
    return add_search_history(query, wait=False)


def get_search_history(limit=10):
    conn = get_connection()
    rows = conn.execute(
        "SELECT query FROM search_history ORDER BY searched_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [row["query"] for row in rows]


def clear_search_history(wait: bool = True):
    return _WORKER.submit_write(
        lambda conn: conn.execute("DELETE FROM search_history"),
        wait=wait,
    )


def clear_search_history_async():
    return clear_search_history(wait=False)


def clear_playlist_tracks(playlist_name):
    def _write(conn: sqlite3.Connection) -> bool:
        row = conn.execute("SELECT id FROM playlists WHERE name = ?", (playlist_name,)).fetchone()
        if not row:
            return False
        conn.execute("DELETE FROM playlist_tracks WHERE playlist_id = ?", (row["id"],))
        return True

    return bool(_WORKER.submit_write(_write, wait=True))


def clean_and_resync_offline_tracks(cache_dir=None):
    """
    Rescans local audio files OUTSIDE any database transaction or lock so UI settings/reads
    never freeze during filesystem scans, then applies atomic SQLite reconciliation via
    DatabaseWorker in one fast transaction.
    """
    from utils.local_audio_utils import extract_local_audio_metadata, scan_device_offline_songs

    # 1. Heavy filesystem & mutagen I/O strictly off the writer queue and UI thread
    scanned_tracks = scan_device_offline_songs(cache_dir=cache_dir)
    path_to_canonical = {}
    canonical_tracks = {}

    for meta in scanned_tracks:
        c_id = meta["video_id"]
        abs_p = meta.get("local_path", "")
        norm_p = os.path.normcase(os.path.realpath(os.path.abspath(abs_p))) if abs_p else ""
        if norm_p:
            path_to_canonical[norm_p] = c_id
        if c_id not in canonical_tracks:
            canonical_tracks[c_id] = meta

    # 2. Check existing local rows via non-blocking WAL read snapshot
    read_conn = get_connection()
    existing_rows = [
        dict(r)
        for r in read_conn.execute(
            "SELECT video_id, local_path FROM tracks WHERE local_path IS NOT NULL AND local_path != ''"
        ).fetchall()
    ]

    delete_vids = []
    for row in existing_rows:
        vid = row["video_id"]
        lp = row["local_path"]
        norm_lp = os.path.normcase(os.path.realpath(os.path.abspath(lp))) if lp else ""
        if norm_lp in path_to_canonical:
            if vid != path_to_canonical[norm_lp]:
                delete_vids.append(vid)
        else:
            if not lp or not os.path.exists(lp):
                delete_vids.append(vid)
            elif os.path.exists(lp) and vid not in canonical_tracks:
                try:
                    canonical_tracks[vid] = extract_local_audio_metadata(lp, cache_dir=cache_dir)
                except Exception:
                    pass

    # 3. Execute atomic fast write transaction inside DatabaseWorker
    def _apply_offline_sync(conn: sqlite3.Connection) -> int:
        for vid in delete_vids:
            conn.execute("DELETE FROM playlist_tracks WHERE video_id = ?", (vid,))
            conn.execute("DELETE FROM tracks WHERE video_id = ?", (vid,))

        for cid, meta in canonical_tracks.items():
            conn.execute(
                '''
                INSERT INTO tracks (video_id, title, artist, url, artwork, duration, local_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(video_id) DO UPDATE SET
                    title = excluded.title,
                    artist = excluded.artist,
                    artwork = CASE WHEN excluded.artwork != '' AND excluded.artwork != 'album_art.png' THEN excluded.artwork ELSE tracks.artwork END,
                    duration = CASE WHEN excluded.duration > 0 THEN excluded.duration ELSE tracks.duration END,
                    local_path = excluded.local_path
                ''',
                (
                    cid,
                    sanitize_text(meta.get("title", "Unknown Title")),
                    sanitize_text(meta.get("artist", "Unknown Artist")),
                    meta.get("url", ""),
                    meta.get("artwork", ""),
                    meta.get("duration", 0),
                    meta.get("local_path", ""),
                ),
            )

        p_row = conn.execute("SELECT id FROM playlists WHERE name = 'Offline Songs'").fetchone()
        if not p_row:
            offline_pid = conn.execute("INSERT INTO playlists (name) VALUES ('Offline Songs')").lastrowid
        else:
            offline_pid = p_row["id"]

        conn.execute("DELETE FROM playlist_tracks WHERE playlist_id = ?", (offline_pid,))
        for cid in canonical_tracks.keys():
            conn.execute(
                "INSERT OR IGNORE INTO playlist_tracks (playlist_id, video_id) VALUES (?, ?)",
                (offline_pid, cid),
            )
        return len(canonical_tracks)

    return _WORKER.submit_write(_apply_offline_sync, wait=True)

# ---- Content-quality gate: keep tutorials/AI songs out of every track read ----
def _apply_content_quality_filter(fn):
    @functools.wraps(fn)
    def _wrapped(*args, **kwargs):
        rows = fn(*args, **kwargs)
        if not isinstance(rows, list) or not rows or not isinstance(rows[0], dict):
            return rows
        try:
            include_ai = bool(get_setting("show_ai_songs", False))
        except Exception:
            include_ai = False
        podcast = rows[0].get("media_type") == "podcast"
        return _filter_tracks(rows, include_ai=include_ai, filter_non_music=not podcast)
    return _wrapped


for _filtered_read in (
    "get_all_tracks", "get_on_repeat", "get_heavy_rotation",
    "get_forgotten_favorites", "get_daily_mix", "get_top_artists",
    "get_local_library_tracks", "get_dynamic_playlist_tracks",
    "get_recently_played", "get_continue_listening", "get_recently_added",
    "get_playlist_tracks",
):
    _original = globals().get(_filtered_read)
    if _original is not None:
        globals()[_filtered_read] = _apply_content_quality_filter(_original)