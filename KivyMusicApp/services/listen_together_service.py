"""
Listen Together Real-Time Synchronization Service.
Enables host-listener music party sessions with real-time playback state synchronization
over local network (LAN / localhost) TCP sockets.
"""

import os
import sys
import json
import socket
import select
import random
import threading
import time
from typing import Dict, Any, List, Optional, Callable
from kivy.clock import Clock
from services.logger import get_logger

logger = get_logger("ListenTogether")


class ListenTogetherService:
    """
    Manages peer-to-peer real-time playback synchronization.
    Supports hosting a session, connecting to an active session,
    broadcasting track state, seeking, play/pause, and member roster management.
    """

    DEFAULT_PORT = 8765

    def __init__(self):
        self.is_host: bool = False
        self.is_connected: bool = False
        self.room_code: str = ""
        self.host_ip: str = "127.0.0.1"
        self.port: int = self.DEFAULT_PORT
        self.client_id: str = f"user_{random.randint(1000, 9999)}"
        self.user_name: str = "You"
        
        # Members roster: list of dicts {"id": str, "name": str, "role": str, "is_host": bool}
        self.members: List[Dict[str, Any]] = []

        # Sockets & Threading
        self._server_socket: Optional[socket.socket] = None
        self._client_socket: Optional[socket.socket] = None
        self._connected_clients: List[socket.socket] = []
        self._stop_event = threading.Event()
        self._server_thread: Optional[threading.Thread] = None
        self._client_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        # Callbacks (dispatched safely to Kivy main thread)
        self.on_state_changed: Optional[Callable[[str, str], None]] = None  # (status, room_code)
        self.on_members_updated: Optional[Callable[[List[Dict[str, Any]]], None]] = None
        self.on_playback_sync_received: Optional[Callable[[Dict[str, Any]], None]] = None
        self.on_toast_requested: Optional[Callable[[str], None]] = None

    def create_room(self, user_name: str = "Host") -> str:
        """Starts hosting a Listen Together session on an available local port."""
        self.leave_room()

        self.is_host = True
        self.user_name = user_name
        # Generate 4-digit room code
        code_num = random.randint(1000, 9999)
        self.room_code = f"#{code_num}"
        self._stop_event.clear()

        # Find available port
        self.port = self.DEFAULT_PORT
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_sock.bind(("0.0.0.0", self.port))
        except Exception:
            # Fallback to random free port
            server_sock.bind(("0.0.0.0", 0))
            self.port = server_sock.getsockname()[1]

        server_sock.listen(5)
        server_sock.settimeout(0.5)
        self._server_socket = server_sock

        # Detect local LAN IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.host_ip = s.getsockname()[0]
            s.close()
        except Exception:
            self.host_ip = "127.0.0.1"

        self.members = [{
            "id": self.client_id,
            "name": f"{self.user_name} (Host)",
            "role": "Host • Playback Controller",
            "icon": "crown",
            "color": [1, 0.8, 0.2, 1],
            "is_host": True
        }]
        self.is_connected = True

        self._server_thread = threading.Thread(target=self._server_worker, daemon=True)
        self._server_thread.start()

        self._dispatch_status("HOSTING", self.room_code)
        self._dispatch_members(self.members)
        return self.room_code

    def join_room(self, room_code: str, host_ip: str = "127.0.0.1", port: Optional[int] = None, user_name: str = "Listener") -> bool:
        """Connects to an active Listen Together session as a listener client."""
        self.leave_room()

        self.is_host = False
        self.room_code = room_code.strip() if room_code.startswith("#") else f"#{room_code.strip()}"
        self.user_name = user_name
        self.host_ip = host_ip.strip() or "127.0.0.1"
        self.port = port or self.DEFAULT_PORT
        self._stop_event.clear()

        try:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock.settimeout(3.0)
            client_sock.connect((self.host_ip, self.port))
            client_sock.settimeout(0.5)
            self._client_socket = client_sock
            self.is_connected = True

            # Send join handshake
            join_msg = {
                "type": "join",
                "client_id": self.client_id,
                "name": self.user_name,
                "room_code": self.room_code
            }
            self._send_raw(client_sock, join_msg)

            self.members = [
                {"id": "host", "name": "Host", "role": "Playback Controller", "icon": "crown", "color": [1, 0.8, 0.2, 1], "is_host": True},
                {"id": self.client_id, "name": f"{self.user_name} (You)", "role": "Listener • Synced", "icon": "account", "color": [0.4, 0.7, 1, 1], "is_host": False}
            ]

            self._client_thread = threading.Thread(target=self._client_worker, daemon=True)
            self._client_thread.start()

            self._dispatch_status("CONNECTED", self.room_code)
            self._dispatch_members(self.members)
            return True
        except Exception as e:
            self._dispatch_toast(f"Could not connect to {self.host_ip}:{self.port} ({e})")
            self.leave_room()
            return False

    def broadcast_playback_sync(self, track_info: Dict[str, Any], elapsed: float, is_paused: bool):
        """Host broadcasts current track and playback position to all connected clients."""
        if not self.is_host or not self.is_connected:
            return

        payload = {
            "type": "sync_state",
            "track": track_info,
            "elapsed": float(elapsed),
            "paused": bool(is_paused),
            "timestamp": time.time(),
            "room_code": self.room_code
        }

        with self._lock:
            disconnected = []
            for client in self._connected_clients:
                try:
                    self._send_raw(client, payload)
                except Exception:
                    disconnected.append(client)
            for d in disconnected:
                if d in self._connected_clients:
                    self._connected_clients.remove(d)

    def add_demo_peer(self, peer_name: str = "Alex R."):
        """Adds a simulated demo listener peer to the room to showcase multi-user synchronization."""
        if not self.is_connected:
            return
        demo_id = f"demo_{len(self.members) + 1}"
        new_peer = {
            "id": demo_id,
            "name": peer_name,
            "role": "Listener • Mobile Client",
            "icon": "cellphone",
            "color": [0.3, 0.85, 0.5, 1],
            "is_host": False
        }
        self.members.append(new_peer)
        self._dispatch_members(self.members)
        self._dispatch_toast(f"{peer_name} joined room {self.room_code}")

    def leave_room(self):
        """Gracefully disconnects from session, stops server/client sockets, and resets state."""
        self._stop_event.set()

        # Close client socket
        if self._client_socket:
            try:
                self._send_raw(self._client_socket, {"type": "leave", "client_id": self.client_id})
                self._client_socket.close()
            except Exception:
                pass
            self._client_socket = None

        # Close connected host clients
        with self._lock:
            for c in self._connected_clients:
                try:
                    c.close()
                except Exception:
                    pass
            self._connected_clients.clear()

        # Close server socket
        if self._server_socket:
            try:
                self._server_socket.close()
            except Exception:
                pass
            self._server_socket = None

        self.is_host = False
        self.is_connected = False
        self.room_code = ""
        self.members = []

        self._dispatch_status("Disconnected", "")
        self._dispatch_members([])

    # Internal Socket Workers
    def _server_worker(self):
        while not self._stop_event.is_set():
            try:
                readable, _, _ = select.select([self._server_socket] + self._connected_clients, [], [], 0.5)
            except Exception:
                break

            for sock in readable:
                if sock is self._server_socket:
                    try:
                        client_sock, addr = self._server_socket.accept()
                        client_sock.settimeout(0.5)
                        with self._lock:
                            self._connected_clients.append(client_sock)
                    except Exception:
                        pass
                else:
                    # Message from connected client
                    try:
                        data = self._read_raw(sock)
                        if not data:
                            self._remove_client(sock)
                            continue
                        msg = json.loads(data)
                        self._handle_server_message(sock, msg)
                    except Exception:
                        self._remove_client(sock)

    def _client_worker(self):
        buffer = ""
        while not self._stop_event.is_set():
            if not self._client_socket:
                break
            try:
                readable, _, _ = select.select([self._client_socket], [], [], 0.5)
                if not readable:
                    continue
                data = self._read_raw(self._client_socket)
                if not data:
                    self._dispatch_toast("Disconnected from host.")
                    self.leave_room()
                    break
                # Each message ends with newline
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if line:
                        msg = json.loads(line)
                        self._handle_client_message(msg)
            except Exception:
                break

    def _remove_client(self, client_sock: socket.socket):
        with self._lock:
            if client_sock in self._connected_clients:
                self._connected_clients.remove(client_sock)
        try:
            client_sock.close()
        except Exception:
            pass

    def _handle_server_message(self, client_sock: socket.socket, msg: Dict[str, Any]):
        mtype = msg.get("type")
        if mtype == "join":
            c_name = msg.get("name", "Peer")
            c_id = msg.get("client_id", str(random.randint(100, 999)))
            new_member = {
                "id": c_id,
                "name": c_name,
                "role": "Listener • Synced",
                "icon": "account",
                "color": [0.4, 0.7, 1, 1],
                "is_host": False
            }
            with self._lock:
                self.members.append(new_member)
            self._dispatch_members(self.members)
            self._dispatch_toast(f"{c_name} joined the listening party!")

            # Welcome client with current room info and member list
            welcome_msg = {
                "type": "welcome",
                "room_code": self.room_code,
                "members": self.members
            }
            self._send_raw(client_sock, welcome_msg)

        elif mtype == "leave":
            c_id = msg.get("client_id")
            with self._lock:
                self.members = [m for m in self.members if m["id"] != c_id]
            self._dispatch_members(self.members)

    def _handle_client_message(self, msg: Dict[str, Any]):
        mtype = msg.get("type")
        if mtype == "sync_state":
            # Pass to app callback on main thread
            if self.on_playback_sync_received:
                Clock.schedule_once(lambda dt: self.on_playback_sync_received(msg), 0)
        elif mtype == "welcome":
            members = msg.get("members", [])
            if members:
                self.members = members
                self._dispatch_members(self.members)

    def _send_raw(self, sock: socket.socket, obj: Dict[str, Any]):
        raw = json.dumps(obj) + "\n"
        sock.sendall(raw.encode("utf-8"))

    def _read_raw(self, sock: socket.socket) -> str:
        data = sock.recv(4096)
        return data.decode("utf-8") if data else ""

    # Dispatch helpers to Kivy main thread
    def _dispatch_status(self, status: str, room_code: str):
        if self.on_state_changed:
            Clock.schedule_once(lambda dt: self.on_state_changed(status, room_code), 0)

    def _dispatch_members(self, members: List[Dict[str, Any]]):
        if self.on_members_updated:
            Clock.schedule_once(lambda dt: self.on_members_updated(list(members)), 0)

    def _dispatch_toast(self, message: str):
        if self.on_toast_requested:
            Clock.schedule_once(lambda dt: self.on_toast_requested(message), 0)
