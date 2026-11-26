"""
Dedicated Single-Writer SQLite Database Worker & Unicode-Safe Text Sanitizer (Priority 5).

Concurrency & Integrity Architecture:
- Dedicated single daemon writer thread (`SQLiteWriteWorker`) owns the write connection
  and processes queued mutations sequentially inside explicit transaction boundaries.
- WAL mode (`PRAGMA journal_mode = WAL`), `PRAGMA synchronous = NORMAL`,
  `PRAGMA busy_timeout = 5000`, and `PRAGMA foreign_keys = ON` are enforced on every
  writer and thread-local WAL reader connection.
- UI-thread callers never stall behind slow background filesystem scans (`scan_device_offline_songs`
  executes outside DB transactions) or held locks (`set_setting` / `*_async` writes return in <0.1ms).
- `sanitize_text()` uses `unicodedata` + NFC normalization to preserve Devanagari, Gurmukhi,
  Latin diacritics, and CJK combining marks while removing emojis and control characters.
"""

from __future__ import annotations

import atexit
import gc
import os
import queue
import re
import sqlite3
import threading
import unicodedata
from concurrent.futures import Future
from typing import Any, Callable, Optional

from services.logger import get_logger

logger = get_logger("DatabaseWorker")

_FALLBACK_LOCK = threading.RLock()
_READER_LOCAL = threading.local()

_PRAGMAS = (
    "PRAGMA journal_mode = WAL;",
    "PRAGMA synchronous = NORMAL;",
    "PRAGMA busy_timeout = 5000;",
    "PRAGMA foreign_keys = ON;",
    "PRAGMA temp_store = MEMORY;",
)


def sanitize_text(text: Any) -> str:
    """
    Unicode-safe sanitizer preserving combining diacritics & Indic matras
    (Devanagari, Gurmukhi, Bengali, Tamil, Arabic, Latin accents) while stripping
    control chars, variation selectors, and high-plane emoji/pictograph symbols.
    """
    if not text:
        return "Unknown"
    raw = unicodedata.normalize("NFC", str(text))
    kept = []
    for ch in raw:
        code = ord(ch)
        if code in (9, 10, 13, 32):
            kept.append(" ")
            continue
        # Strip ASCII & Unicode control characters, format chars (e.g. ZWJ U+200D),
        # variation selectors (FE00-FE0F), and non-BMP emojis (>= U+1F000)
        if code >= 0x1F000 or (0xFE00 <= code <= 0xFE0F) or (0x2600 <= code <= 0x27BF):
            continue
        cat = unicodedata.category(ch)
        # Keep Letters (L*), ALL Combining Marks (Mn/Mc/Me -> Indic matras/halants),
        # Numbers (N*), Punctuation (P*), Spaces (Zs), and currency/math symbols (Sc/Sm)
        if cat[0] in ("L", "M", "N", "P") or cat in ("Zs", "Sc", "Sm"):
            kept.append(ch)
        elif cat == "Sk" and code < 0x1F000:
            kept.append(ch)
    cleaned = re.sub(r"\s+", " ", "".join(kept)).strip()
    return cleaned or "Unknown"


def configure_connection(conn: sqlite3.Connection, enforce_fk: bool = True) -> sqlite3.Connection:
    """Apply production SQLite PRAGMAs (WAL, busy_timeout, foreign_keys) onto a connection."""
    conn.row_factory = sqlite3.Row
    for stmt in _PRAGMAS:
        if not enforce_fk and "foreign_keys" in stmt:
            continue
        try:
            conn.execute(stmt)
        except sqlite3.OperationalError:
            # Read-only or locked transiently during pragma init; busy_timeout retries SQL ops
            pass
    return conn


class DatabaseWorker:
    """
    Single-writer thread owning SQLite write transactions cleanly off the Kivy UI thread.
    Supports both synchronous (`wait=True`) and optimistic async (`wait=False`) tasks.
    """

    def __init__(self, db_path_resolver: Callable[[], str]):
        self._resolve_path = db_path_resolver
        self._override_path: Optional[str] = None
        self._queue: queue.Queue = queue.Queue()
        self._control_lock = threading.RLock()
        self._thread: Optional[threading.Thread] = None
        self._writer_conn: Optional[sqlite3.Connection] = None
        self._writer_path: Optional[str] = None
        self._reader_conns: dict[tuple[int, str], sqlite3.Connection] = {}
        self._stopping = False

    def get_active_path(self) -> str:
        with self._control_lock:
            return self._override_path or self._resolve_path()

    def set_db_path(self, db_path: Optional[str]) -> None:
        """Switch active database path (primarily for isolated test fixtures)."""
        new_path = os.path.abspath(db_path) if db_path else None
        current = self.get_active_path()
        if new_path and os.path.abspath(current) == new_path:
            return
        with self._control_lock:
            self._override_path = new_path
        # Close existing connections via worker so next operation opens cleanly
        self.reset_connections()

    def _ensure_started_locked(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stopping = False
        self._thread = threading.Thread(
            target=self._run_loop,
            daemon=True,
            name="SQLiteWriteWorker",
        )
        self._thread.start()

    def _get_writer_conn(self) -> sqlite3.Connection:
        target = self.get_active_path()
        if self._writer_conn is not None and self._writer_path != target:
            try:
                self._writer_conn.close()
            except Exception:
                pass
            self._writer_conn = None
        if self._writer_conn is None:
            parent = os.path.dirname(target)
            if parent:
                os.makedirs(parent, exist_ok=True)
            conn = sqlite3.connect(target, timeout=5.0, isolation_level=None)
            configure_connection(conn, enforce_fk=True)
            self._writer_conn = conn
            self._writer_path = target
        return self._writer_conn

    def _run_loop(self) -> None:
        while True:
            item = self._queue.get()
            if item is None:
                # Drain/close clean shutdown sentinel
                self._close_writer_inline()
                self._queue.task_done()
                break

            op = item[0]
            if op == "__CLOSE_WRITER__":
                _, fut = item
                try:
                    self._close_writer_inline()
                    if not fut.done():
                        fut.set_result(True)
                except Exception as exc:
                    if not fut.done():
                        fut.set_exception(exc)
                finally:
                    self._queue.task_done()
                continue

            fn, fut, transactional = item
            try:
                conn = self._get_writer_conn()
                if transactional:
                    conn.execute("BEGIN IMMEDIATE")
                    try:
                        res = fn(conn)
                        if conn.in_transaction:
                            conn.execute("COMMIT")
                    except Exception:
                        if conn.in_transaction:
                            try:
                                conn.execute("ROLLBACK")
                            except Exception:
                                pass
                        raise
                else:
                    res = fn(conn)
                if not fut.done():
                    fut.set_result(res)
            except Exception as exc:
                if not fut.done():
                    fut.set_exception(exc)
            finally:
                self._queue.task_done()

    def submit_write(
        self,
        fn: Callable[[sqlite3.Connection], Any],
        wait: bool = True,
        transactional: bool = True,
    ) -> Any:
        """
        Enqueue a write closure onto the dedicated SQLite writer thread.
        - wait=True blocks caller until committed and returns result (or raises exception).
        - wait=False returns a `Future` immediately for non-blocking UI writes.
        """
        fut: Future = Future()
        # Re-entrancy check: if already running INSIDE the worker thread, execute inline safely!
        if threading.current_thread() is self._thread:
            try:
                conn = self._get_writer_conn()
                res = fn(conn)
                fut.set_result(res)
                return res if wait else fut
            except Exception as exc:
                fut.set_exception(exc)
                if wait:
                    raise
                return fut

        # Fast-path once worker is running avoids acquiring _control_lock per queued write
        if not (self._thread and self._thread.is_alive()):
            with self._control_lock:
                self._ensure_started_locked()
        self._queue.put((fn, fut, transactional))

        if wait:
            return fut.result()
        return fut

    def flush(self, timeout: float = 5.0) -> bool:
        """Wait until all previously queued writes have committed on the worker thread."""
        with self._control_lock:
            if not self._thread or not self._thread.is_alive():
                return True
        if threading.current_thread() is self._thread:
            return True
        fut = self.submit_write(lambda conn: True, wait=False, transactional=False)
        try:
            fut.result(timeout=timeout)
            return True
        except Exception:
            return False

    def get_read_connection(self, db_path: Optional[str] = None) -> sqlite3.Connection:
        """
        Return a WAL-enabled thread-local connection for non-blocking concurrent reads.
        Safe to call from UI threads and worker threads concurrently.
        """
        target = os.path.abspath(db_path) if db_path else os.path.abspath(self.get_active_path())
        # If called directly from the dedicated writer thread, reuse its active connection cleanly
        if threading.current_thread() is self._thread and (
            not self._writer_path or os.path.abspath(self._writer_path) == target
        ):
            return self._get_writer_conn()

        tid = threading.get_ident()
        key = (tid, target)
        with self._control_lock:
            existing = self._reader_conns.get(key)

        if existing is not None:
            try:
                existing.execute("SELECT 1")
                return existing
            except Exception:
                with self._control_lock:
                    self._reader_conns.pop(key, None)
                try:
                    existing.close()
                except Exception:
                    pass

        parent = os.path.dirname(target)
        if parent:
            os.makedirs(parent, exist_ok=True)
        # Each reader connection is exclusively pinned to `(tid, target)` for WAL reads;
        # check_same_thread=False only enables deterministic `.close()` during reset/shutdown.
        conn = sqlite3.connect(target, timeout=5.0, check_same_thread=False)
        configure_connection(conn, enforce_fk=True)
        with self._control_lock:
            self._reader_conns[key] = conn
        return conn

    def reset_connections(self) -> None:
        """Flush writes, close writer + cached reader connections cleanly without holding _control_lock while waiting."""
        close_fut: Optional[Future] = None
        with self._control_lock:
            for _, c in list(self._reader_conns.items()):
                try:
                    c.close()
                except Exception:
                    pass
            self._reader_conns.clear()

            if self._thread and self._thread.is_alive():
                if threading.current_thread() is self._thread:
                    self._close_writer_inline()
                else:
                    close_fut = Future()
                    self._queue.put(("__CLOSE_WRITER__", close_fut))

        if close_fut is not None:
            try:
                close_fut.result(timeout=5.0)
            except Exception:
                pass
        gc.collect()

    def _close_writer_inline(self, conn: Optional[sqlite3.Connection] = None) -> None:
        if self._writer_conn is not None:
            try:
                self._writer_conn.close()
            except Exception:
                pass
            self._writer_conn = None
            self._writer_path = None

    def shutdown(self, timeout: float = 3.0) -> None:
        """Gracefully flush pending writes and shut down the dedicated worker thread."""
        with self._control_lock:
            if not self._thread or not self._thread.is_alive():
                return
            self._stopping = True
            self._queue.put(None)
            t = self._thread
        t.join(timeout=timeout)
        self.reset_connections()
