"""
Discord Rich Presence (RPC) Service for KivyMusicApp.
Broadcasts active track metadata, playback status, and elapsed duration to Discord.
Cross-platform guarded:
- Fully supported on Windows, macOS, and Linux when Discord is active.
- Safely no-ops on Android or when pypresence is not installed, with zero overhead.
"""

import time
import threading
from typing import Optional
from kivy.utils import platform
from services.logger import get_logger

logger = get_logger("DiscordRPC")

class DiscordRPCService:
    """Manages connection and presence updates to the local Discord client."""

    DEFAULT_CLIENT_ID = "1136988323819298856"

    def __init__(self, client_id: str = DEFAULT_CLIENT_ID):
        self.client_id = client_id
        self.enabled = (platform != 'android')
        self.connected = False
        self._rpc = None
        self._lock = threading.Lock()
        self._last_state = None

        if self.enabled:
            self._init_rpc_async()

    def _init_rpc_async(self):
        """Asynchronously initialize connection to Discord IPC socket."""
        def _connect():
            try:
                from pypresence import Presence
                rpc = Presence(self.client_id)
                rpc.connect()
                with self._lock:
                    self._rpc = rpc
                    self.connected = True
                logger.info("Connected to Discord Rich Presence IPC socket")
            except Exception as e:
                # Discord client is not running or pypresence not installed
                with self._lock:
                    self.connected = False
                    self._rpc = None
                logger.debug("Discord RPC not connected: %s", e)

        threading.Thread(target=_connect, daemon=True).start()

    def update_track(
        self,
        title: str,
        artist: str = "",
        elapsed: float = 0.0,
        duration: float = 180.0,
        is_playing: bool = True
    ):
        """Broadcasts current playback state to Discord Rich Presence."""
        if not self.enabled or not self.connected:
            return

        def _worker():
            with self._lock:
                if not self._rpc:
                    return
                try:
                    start_time = int(time.time() - elapsed) if is_playing else None
                    end_time = int(start_time + duration) if (is_playing and duration > 0 and start_time) else None
                    state_str = f"by {artist}" if artist else "Streaming Music"
                    details_str = title[:120] if title else "Listening to Music"

                    self._rpc.update(
                        details=details_str,
                        state=state_str,
                        start=start_time,
                        end=end_time,
                        large_image="music_logo",
                        large_text="KivyMusicApp",
                        small_image="play" if is_playing else "pause",
                        small_text="Playing" if is_playing else "Paused"
                    )
                except Exception:
                    pass

        threading.Thread(target=_worker, daemon=True).start()

    def clear(self):
        """Clears Discord Rich Presence."""
        if not self.enabled or not self.connected:
            return

        def _worker():
            with self._lock:
                if self._rpc:
                    try:
                        self._rpc.clear()
                    except Exception:
                        pass

        threading.Thread(target=_worker, daemon=True).start()

    def close(self):
        """Closes Discord RPC connection."""
        if not self.enabled or not self.connected:
            return

        with self._lock:
            if self._rpc:
                try:
                    self._rpc.close()
                except Exception:
                    pass
                self._rpc = None
                self.connected = False
