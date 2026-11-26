"""Modular core coordinators for KivyMusicApp.

Breaks the monolithic MusicApp God-object cleanly into single-responsibility
components matching GEMINI.md Sections 3 and 25:
- AppState: Settings schema, defaults, preset tables, and DB state hydration
- ServiceContainer & MusicRepository: Model/service/controller/provider lifecycle
- AppBootstrap: Font resolution, Kivy theme/textures, cooperative splash warmup
- ApplicationLifecycle: Pause/resume/session-restore/smooth-exit/stop handling
- NavigationCoordinator: ScreenManager stack, transitions, hardware back & nav bar
- SettingsCoordinator, PlaybackUICoordinator, LyricsCoordinator,
  PlaylistOptionsCoordinator, CatalogCoordinator, SearchCoordinator
"""

from app_core.bootstrap import AppBootstrap, resolve_and_register_system_fonts
from app_core.catalog_coordinator import CatalogCoordinator
from app_core.lifecycle import ApplicationLifecycle
from app_core.lyrics_coordinator import LyricsCoordinator
from app_core.navigation_coordinator import NavigationCoordinator
from app_core.playback_ui_coordinator import PlaybackUICoordinator
from app_core.playlist_options_coordinator import PlaylistOptionsCoordinator
from app_core.search_coordinator import SearchCoordinator
from app_core.service_container import MusicRepository, ServiceContainer
from app_core.settings_coordinator import SettingsCoordinator
from app_core.state import AppState

__all__ = [
    "AppState",
    "ServiceContainer",
    "MusicRepository",
    "AppBootstrap",
    "ApplicationLifecycle",
    "NavigationCoordinator",
    "SettingsCoordinator",
    "PlaybackUICoordinator",
    "LyricsCoordinator",
    "PlaylistOptionsCoordinator",
    "CatalogCoordinator",
    "SearchCoordinator",
    "resolve_and_register_system_fonts",
]
