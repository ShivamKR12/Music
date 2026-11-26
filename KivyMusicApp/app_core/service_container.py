"""Service Container & Music Repository Boundary (GEMINI.md Section 3)."""

from __future__ import annotations

import sys
from typing import Any, Callable, Optional

from controllers.player_controller import PlayerController
from models import database as db_module
from models.track_model import PlaylistModel
from services.listen_together_service import ListenTogetherService
from services.logger import app_logger, init_logging


def resolve_symbol(name: str, fallback: Any) -> Any:
    """Resolve symbol through `main` when loaded so test/benchmark patches stay honored."""
    main_mod = sys.modules.get("main")
    if main_mod is not None and hasattr(main_mod, name):
        return getattr(main_mod, name)
    return fallback


class MusicRepository:
    """Thin data repository facade sitting above SQLite worker and MusicProviderRouter."""

    def init_storage(self) -> None:
        db_module.init_db()

    def get_all_tracks(self, limit: Optional[int] = None):
        fn: Callable = resolve_symbol("get_all_tracks", db_module.get_all_tracks)
        return fn(limit=limit) if limit is not None else fn()

    def get_playlist_tracks(self, playlist_name: str):
        fn: Callable = resolve_symbol("get_playlist_tracks", db_module.get_playlist_tracks)
        return fn(playlist_name)

    def get_recently_played(self, limit: int = 50):
        fn: Callable = resolve_symbol("get_recently_played", db_module.get_recently_played)
        return fn(limit=limit)

    def get_recently_added(self, limit: int = 30):
        fn: Callable = resolve_symbol("get_recently_added", db_module.get_recently_added)
        return fn(limit=limit)


class ServiceContainer:
    """Owns construction and wiring of core services, repository, and PlayerController."""

    def __init__(self, app: Any):
        self.app = app
        self.repository = MusicRepository()
        self.listen_together_service: Optional[ListenTogetherService] = None
        self.playlist_model: Optional[PlaylistModel] = None
        self.player_controller: Optional[PlayerController] = None
        self._provider_router = None
        self._recommendation_engine = None

    def initialize_core_services(self) -> None:
        """Initialize logging, SQLite DB worker, Listen Together, models, and PlayerController."""
        app = self.app
        init_logging()
        app_logger.info("Initializing MusicApp components...")

        self.listen_together_service = ListenTogetherService()
        app.listen_together_service = self.listen_together_service
        self.listen_together_service.on_state_changed = app.on_listen_together_state_changed
        self.listen_together_service.on_members_updated = app.on_listen_together_members_updated
        self.listen_together_service.on_playback_sync_received = app.on_listen_together_playback_sync
        self.listen_together_service.on_toast_requested = app.show_toast

        self.repository.init_storage()

    def wire_player_stack(self) -> None:
        """Instantiate PlaylistModel and PlayerController after state hydration, and bind UI hooks."""
        app = self.app
        self.playlist_model = PlaylistModel()
        app.playlist_model = self.playlist_model

        self.player_controller = PlayerController()
        app.player_controller = self.player_controller
        self.player_controller.set_playlist(self.playlist_model)
        self.player_controller.set_crossfade_duration(app.crossfade_duration)
        app.apply_audio_eq()
        self.player_controller.bind(active_track=app.on_active_track_change)
        self.player_controller.bind(is_playing=app.on_player_playing_change)
        self.player_controller.bind(current_time=app.on_player_time_change)

    @property
    def provider_router(self):
        if self._provider_router is None:
            from services.music_provider_router import MusicProviderRouter
            self._provider_router = MusicProviderRouter()
        return self._provider_router

    @property
    def recommendation_engine(self):
        if self._recommendation_engine is None:
            from services.recommendation_engine import RecommendationEngine
            self._recommendation_engine = RecommendationEngine()
        return self._recommendation_engine
