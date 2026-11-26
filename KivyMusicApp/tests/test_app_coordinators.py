"""Priority 8 Modular Coordinator Architecture & Delegation Tests.

Verifies:
1. `main.py` decomposition bounds (< 600 lines; no duplicate method definitions).
2. Presence and isolation of all GEMINI.md §3 coordinators (`AppBootstrap`,
   `ServiceContainer`, `NavigationCoordinator`, `ApplicationLifecycle`, `AppState`)
   plus domain coordinators under `app_core/`.
3. 100% resolution of every `app.<method>()` binding across all `.kv` files on `MusicApp`.
4. Standalone coordinator unit behavior (`NavigationCoordinator`, `AppState`,
   `ApplicationLifecycle`, `MusicRepository`, `CatalogCoordinator`) with stubbed `app`.
"""

import ast
import os
import re
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

os.environ["KIVY_HEADLESS"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app_core import (
    AppBootstrap,
    ApplicationLifecycle,
    AppState,
    CatalogCoordinator,
    LyricsCoordinator,
    MusicRepository,
    NavigationCoordinator,
    PlaybackUICoordinator,
    PlaylistOptionsCoordinator,
    SearchCoordinator,
    ServiceContainer,
    SettingsCoordinator,
)
from main import MusicApp


def test_main_monolith_reduction_and_no_duplicates():
    main_path = os.path.join(ROOT, "main.py")
    src = open(main_path, "r", encoding="utf-8").read()
    lines = src.splitlines()
    assert len(lines) < 600, f"Expected slim main.py < 600 lines, got {len(lines)}"

    tree = ast.parse(src)
    music_cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "MusicApp")
    method_names = [n.name for n in music_cls.body if isinstance(n, ast.FunctionDef)]
    dups = {m for m in method_names if method_names.count(m) > 1}
    assert not dups, f"Duplicate methods found in MusicApp: {dups}"
    print(f"[PASS] main.py reduced cleanly to {len(lines)} lines with 0 duplicate methods")


def test_kv_bindings_and_coordinator_wiring():
    kv_dir = os.path.join(ROOT, "views")
    missing = []
    checked = 0
    app_dir_set = set(dir(MusicApp))
    for root, _, files in os.walk(kv_dir):
        for fname in files:
            if not fname.endswith(".kv"):
                continue
            txt = open(os.path.join(root, fname), "r", encoding="utf-8").read()
            for m in re.finditer(r"app\.([a-zA-Z0-9_]+)\(", txt):
                meth = m.group(1)
                checked += 1
                if meth not in app_dir_set and not hasattr(MusicApp, meth):
                    missing.append((fname, meth))
    assert not missing, f"Missing MusicApp bindings for .kv: {missing}"
    print(f"[PASS] Verified {checked} .kv app.<method>() calls exist on MusicApp")


def test_unit_coordinators_standalone():
    # NavigationCoordinator standalone with lightweight stub app & ScreenManager
    sm = SimpleNamespace(
        current="home",
        width=360,
        height=640,
        transition=None,
        has_screen=lambda name: name in ("home", "settings", "analytics"),
        get_screen=lambda name: SimpleNamespace(ids={}),
    )
    class _Ids(dict):
        def __getattr__(self, key):
            try:
                return self[key]
            except KeyError as exc:
                raise AttributeError(key) from exc

    stub_app = SimpleNamespace(
        root=SimpleNamespace(ids=_Ids(screen_manager=sm)),
        screen_history=[],
        active_tab_name="home",
        mini_player_visible=False,
        mini_player_dismissed=False,
    )
    stub_app.sync_nav_bar = lambda name: setattr(stub_app, "active_tab_name", name)
    stub_app.load_analytics_data = MagicMock()
    stub_app.ensure_player_carousel = MagicMock()
    stub_app.load_recently_played_data = MagicMock()
    stub_app.load_podcasts_data = MagicMock()
    stub_app.refresh_library_data = MagicMock()
    stub_app.refresh_cache_size = MagicMock()

    nav = NavigationCoordinator(stub_app)
    stub_app.go_back = nav.go_back
    nav.switch_screen("analytics")
    assert sm.current == "analytics", sm.current
    assert stub_app.screen_history == ["home"], stub_app.screen_history
    stub_app.load_analytics_data.assert_called_once()

    nav.go_back()
    assert sm.current == "home", sm.current
    assert stub_app.active_tab_name == "home"

    # CatalogCoordinator pure helper assertions
    assert CatalogCoordinator.is_user_library_playlist("My Chill Roadtrip") is True
    assert CatalogCoordinator.is_user_library_playlist("Favorites") is False
    assert CatalogCoordinator.is_user_library_playlist("Top Charts") is False

    # ApplicationLifecycle pause/resume/close safety with stub controller
    stub_pc = SimpleNamespace(
        active_track=None,
        is_playing=False,
        current_time=0.0,
        duration=180.0,
        persist_session_snapshot=MagicMock(),
        fade_out_and_stop=MagicMock(),
        stop=MagicMock(),
    )
    stub_app.player_controller = stub_pc
    stub_app._telemetry_sample_frame = lambda dt: None
    stub_app._telemetry_sample_memory = lambda dt: None
    lc = ApplicationLifecycle(stub_app)
    assert lc.on_pause() is True
    stub_pc.persist_session_snapshot.assert_called_once()
    lc.on_stop()
    stub_pc.stop.assert_called_once()

    # MusicRepository basic read contract
    repo = MusicRepository()
    assert isinstance(repo.get_all_tracks(), list)
    print("[PASS] Standalone coordinator contracts & MusicRepository passed")


def test_musicapp_coordinator_instances():
    app = MusicApp()
    assert isinstance(app.app_state, AppState)
    assert isinstance(app.services, ServiceContainer)
    assert isinstance(app.bootstrap, AppBootstrap)
    assert isinstance(app.lifecycle, ApplicationLifecycle)
    assert isinstance(app.navigation, NavigationCoordinator)
    assert isinstance(app.settings_coord, SettingsCoordinator)
    assert isinstance(app.playback_ui, PlaybackUICoordinator)
    assert isinstance(app.lyrics_coord, LyricsCoordinator)
    assert isinstance(app.playlist_options, PlaylistOptionsCoordinator)
    assert isinstance(app.catalog, CatalogCoordinator)
    assert isinstance(app.search_coord, SearchCoordinator)
    assert app.get_telemetry_snapshot()["cold_startup"] is not None
    app.on_stop()
    print("[PASS] MusicApp coordinator composition verified cleanly")


if __name__ == "__main__":
    test_main_monolith_reduction_and_no_duplicates()
    test_kv_bindings_and_coordinator_wiring()
    test_unit_coordinators_standalone()
    test_musicapp_coordinator_instances()
    print("ALL APP COORDINATOR MODULARIZATION TESTS PASSED")
