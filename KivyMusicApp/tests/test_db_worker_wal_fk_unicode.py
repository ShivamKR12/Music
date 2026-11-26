"""
Priority 5 Verification Battery: Dedicated Single-Writer SQLite DatabaseWorker,
WAL Concurrency, Foreign Key Enforcement, Atomic Schema Migrations, & Unicode Preservation.

Uses isolated temporary SQLite databases so tests verify real disk persistence,
migration upgrades from legacy schemas, concurrent read/write contention, and
lossless Devanagari/Gurmukhi matra preservation without mutating production data.
"""

import os
import sqlite3
import sys
import tempfile
import threading
import time

os.environ["KIVY_HEADLESS"] = "1"
os.environ["KIVY_LOG_MODE"] = "PYTHON"

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from models import database as db
from models.db_worker import sanitize_text


def test_1_unit_unicode_safe_sanitize_text():
    print("\n--- [Unit] 1. Unicode-Safe sanitize_text (Devanagari, Gurmukhi, Diacritics, Emojis) ---")
    samples = [
        "केसरिया तेरा इश्क़ है पिया",
        "आँखें खुली हो या हो बंद",
        "ਮੁੰਡਾ ਪੰਜਾਬੀ ਗੀਤ",
        "ਦਿੱਲ ਦੀਆਂ ਗੱਲਾਂ",
        "東京夜曲 — Night Drive",
    ]
    for s in samples:
        out = sanitize_text(s)
        assert out == s, f"Unicode corruption in sanitize_text({s!r}) -> {out!r}"

    # Combining Latin diacritics normalize cleanly to NFC without dropping accents
    decomposed = "Cafe\u0301 Mu\u0308ller"
    norm_out = sanitize_text(decomposed)
    assert norm_out == "Café Müller", f"Expected NFC Latin accents preserved, got {norm_out!r}"

    # Emojis & control characters removed while preserving readable words/punctuation
    noisy = "Trending Hit 🔥🎵\x00 (Remix)!"
    clean = sanitize_text(noisy)
    assert "🔥" not in clean and "🎵" not in clean and "\x00" not in clean
    assert "Trending Hit" in clean and "(Remix)!" in clean
    assert sanitize_text("") == "Unknown"
    print("  [PASS] Devanagari/Gurmukhi matras, CJK, NFC accents preserved; emojis/controls scrubbed.")


def test_2_integration_atomic_migration_wal_and_fk_enforcement():
    print("\n--- [Integration] 2. Legacy Schema Atomic Migration, WAL Mode, & FK Enforcement ---")
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = os.path.join(tmpdir, "legacy_upgrade.db")
        # Create legacy DB missing ON DELETE CASCADE and containing a dangling orphan row
        legacy_conn = sqlite3.connect(db_file)
        legacy_conn.execute('''
            CREATE TABLE tracks (
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
        legacy_conn.execute('''
            CREATE TABLE playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        legacy_conn.execute('''
            CREATE TABLE playlist_tracks (
                playlist_id INTEGER,
                video_id TEXT,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(playlist_id) REFERENCES playlists(id),
                FOREIGN KEY(video_id) REFERENCES tracks(video_id),
                UNIQUE(playlist_id, video_id)
            )
        ''')
        legacy_conn.execute("INSERT INTO playlists (name) VALUES ('Favorites')")
        legacy_conn.execute("INSERT INTO tracks (video_id, title, artist) VALUES ('real_1', 'Valid Song', 'Artist')")
        legacy_conn.execute("INSERT INTO playlist_tracks (playlist_id, video_id) VALUES (1, 'real_1')")
        # Inject broken orphan pointer that would violate FK once enabled
        legacy_conn.execute("INSERT INTO playlist_tracks (playlist_id, video_id) VALUES (1, 'ghost_orphan_vid')")
        legacy_conn.commit()
        legacy_conn.close()

        orig_path = db._WORKER.get_active_path()
        try:
            db.init_db(db_file)
            status = db.get_db_worker_status()
            assert status["worker_alive"] is True
            assert status["schema_version"] == 2, f"Expected schema_version=2, got {status['schema_version']}"

            conn = db.get_connection()
            jm = (conn.execute("PRAGMA journal_mode").fetchone() or [""])[0]
            fk = (conn.execute("PRAGMA foreign_keys").fetchone() or [0])[0]
            bt = (conn.execute("PRAGMA busy_timeout").fetchone() or [0])[0]
            assert str(jm).lower() == "wal", f"Expected WAL journal_mode, got {jm}"
            assert int(fk) == 1, f"Expected foreign_keys=1, got {fk}"
            assert int(bt) >= 5000, f"Expected busy_timeout>=5000, got {bt}"

            # Verify orphan was scrubbed cleanly during Migration v2
            favs = db.get_playlist_tracks("Favorites")
            assert [r["video_id"] for r in favs] == ["real_1"], f"Unexpected upgraded rows: {favs}"

            # Strict FK check: linking nonexistent video_id without track_meta MUST fail safely
            ok_orphan = db.add_track_to_playlist("Favorites", "nonexistent_fk_vid")
            assert ok_orphan is False, "Expected PRAGMA foreign_keys=ON to reject dangling playlist_tracks insert"

            # ON DELETE CASCADE check: deleting real_1 removes its playlist_tracks link automatically
            def _del(wconn):
                wconn.execute("DELETE FROM tracks WHERE video_id = 'real_1'")
            db._WORKER.submit_write(_del, wait=True)
            assert db.get_playlist_tracks("Favorites") == []

            # Unicode Indic track round-trip in SQLite
            db.add_track("hi_1", "केसरिया इश्क़", "अरिजीत सिंह", "https://example.com/hi", duration=240)
            db.add_track("pa_1", "ਮੁੰਡਾ ਪੰਜਾਬੀ", "ਦਿਲਜੀਤ ਦੋਸਾਂਝ", "https://example.com/pa", duration=210)
            assert db.get_track("hi_1")["title"] == "केसरिया इश्क़"
            assert db.get_track("pa_1")["artist"] == "ਦਿਲਜੀਤ ਦੋਸਾਂਝ"

            print("  [PASS] Legacy schema migrated atomically (v2), WAL/FK active, orphan scrubbed, Unicode lossless.")
        finally:
            db.flush_db_writes()
            db._WORKER.set_db_path(orig_path)
            db.init_db(orig_path)


def test_3_integration_concurrent_stress_and_nonblocking_settings():
    print("\n--- [Integration + Telemetry] 3. Concurrent Readers/Writers & Non-Blocking Optimistic Settings ---")
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = os.path.join(tmpdir, "concurrency.db")
        orig_path = db._WORKER.get_active_path()
        try:
            db.init_db(db_file)
            errors = []
            read_counts = [0]

            # 4 concurrent stress threads (2 async writers + 2 concurrent WAL readers)
            def _writer_worker(wid: int):
                try:
                    for i in range(60):
                        vid = f"cw_{wid}_{i}"
                        db.add_track_async(vid, f"Track {wid}-{i}", f"Artist {wid}", "", duration=180 + i)
                        db.mark_track_played_async(vid, listened_seconds=45.0, track_duration=180.0)
                except Exception as exc:
                    errors.append(exc)

            def _reader_worker():
                try:
                    for _ in range(80):
                        _ = db.get_all_tracks()
                        _ = db.get_all_playlists()
                        read_counts[0] += 1
                        time.sleep(0.001)
                except Exception as exc:
                    errors.append(exc)

            threads = [
                threading.Thread(target=_writer_worker, args=(1,)),
                threading.Thread(target=_writer_worker, args=(2,)),
                threading.Thread(target=_reader_worker),
                threading.Thread(target=_reader_worker),
            ]
            for t in threads:
                t.start()

            # Measure optimistic UI-thread settings toggles WHILE concurrent batch writes run!
            t0 = time.perf_counter()
            for idx in range(20):
                db.set_setting("theme_style", "Dark" if idx % 2 == 0 else "Light")
                db.set_setting("crossfade_duration", str(idx % 9))
            ui_ms = (time.perf_counter() - t0) * 1000.0

            # Immediate read-your-writes consistency without blocking
            assert db.get_setting("theme_style") == "Light"
            assert db.get_setting("crossfade_duration") == "1"

            for t in threads:
                t.join(timeout=10.0)
            assert db.flush_db_writes(timeout=10.0) is True
            assert not errors, f"Concurrent DB worker encountered errors: {errors}"

            # Verify durable disk persistence in a completely independent raw sqlite3 connection
            raw_conn = sqlite3.connect(db_file)
            row_theme = raw_conn.execute("SELECT value FROM settings WHERE key = 'theme_style'").fetchone()
            row_xf = raw_conn.execute("SELECT value FROM settings WHERE key = 'crossfade_duration'").fetchone()
            cnt_tracks = (raw_conn.execute("SELECT COUNT(*) FROM tracks WHERE video_id LIKE 'cw_%'").fetchone() or [0])[0]
            raw_conn.close()

            assert row_theme and row_theme[0] == "Light", f"Disk durability mismatch for theme_style: {row_theme}"
            assert row_xf and row_xf[0] == "1", f"Disk durability mismatch for crossfade_duration: {row_xf}"
            assert cnt_tracks == 120, f"Expected 120 tracks flushed to disk, got {cnt_tracks}"
            assert ui_ms < 25.0, f"40 optimistic set_setting calls took too long ({ui_ms:.2f}ms)"

            print(
                f"  [PASS] 40 optimistic UI settings toggles took {ui_ms:.2f}ms total; "
                f"120 concurrent writes + {read_counts[0]} WAL reads finished with 0 errors."
            )
        finally:
            db.flush_db_writes()
            db._WORKER.set_db_path(orig_path)
            db.init_db(orig_path)


if __name__ == "__main__":
    print("=" * 72)
    print("PRIORITY 5 DATABASE WORKER, WAL, FK & UNICODE SANITIZATION TESTS")
    print("=" * 72)
    test_1_unit_unicode_safe_sanitize_text()
    test_2_integration_atomic_migration_wal_and_fk_enforcement()
    test_3_integration_concurrent_stress_and_nonblocking_settings()
    print("\nALL DATABASE WORKER, WAL, FK & UNICODE CHECKS PASSED.")
