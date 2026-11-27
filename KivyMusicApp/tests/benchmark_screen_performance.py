"""
KivyMusicApp — screen performance benchmark (standalone, not part of the test battery).

Measures from the FIRST line of code (imports included) through cold start and
every screen-to-screen transition in the SimpMusic UI. No audio is played.

Usage (from KivyMusicApp/):
    python tests/benchmark_screen_performance.py new

Raw JSON + a Markdown report are written to docs/performance/.
"""
import time
_T0 = time.perf_counter()  # measurement starts here — before any app import
import os
import sys
import json
import glob
import re
import statistics
from datetime import datetime

MODE = sys.argv[1] if len(sys.argv) > 1 else "new"
if MODE != "new":
    raise SystemExit("usage: benchmark_screen_performance.py new [output-tag]")
TAG = sys.argv[2] if len(sys.argv) > 2 else ""

APP_DIR = r"C:\Users\Shivam\Desktop\Music\KivyMusicApp"
OUT_DIR = os.path.join(APP_DIR, "docs", "performance")
os.makedirs(OUT_DIR, exist_ok=True)
os.chdir(APP_DIR)
sys.path.insert(0, APP_DIR)
os.environ["KIVY_HEADLESS"] = "1"  # deterministic; no transitions timers / network polling

checkpoints = []
def mark(label):
    t = time.perf_counter()
    prev = checkpoints[-1]["t_ms"] if checkpoints else 0.0
    checkpoints.append({"label": label, "t_ms": round((t - _T0) * 1000, 2),
                        "delta_ms": round((t - _T0) * 1000 - prev, 2)})
    print(f"[bench] {label}: {checkpoints[-1]['t_ms']:.1f}ms (+{checkpoints[-1]['delta_ms']:.1f})", flush=True)

mark("process_start")
try:
    import psutil
    _proc = psutil.Process()
    def rss_mb():
        return round(_proc.memory_info().rss / (1024 * 1024), 1)
except Exception:
    def rss_mb():
        return -1.0

checkpoints[-1]["rss_mb"] = rss_mb()

import kivy
mark("import_kivy")

from kivy.clock import Clock
from kivy.core.window import Window
Window.size = (360, 640)
mark("import_kivy_core")

import kivymd
mark("import_kivymd")

t = time.perf_counter()
from main import MusicApp
import main as main_module
mark("import_main")

# Discover every screen name from the KV rules (class + name pair)
SCREEN_NAMES = []
for path in glob.glob(os.path.join(APP_DIR, "views", "screens", "*.kv")):
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    for m in re.finditer(r"<(\w+Screen)>:\s*\n(?:(?!\n<).){0,400}?name:\s*[\"']([\w_]+)[\"']", text, re.S):
        SCREEN_NAMES.append(m.group(2))
SCREEN_NAMES = sorted(set(SCREEN_NAMES + ["splash"]))
print(f"[bench] discovered {len(SCREEN_NAMES)} screens: {SCREEN_NAMES}", flush=True)

# Instrument main-module data loaders / heavy helpers (main.py imported them by name).
calls = {}
def instrument(module, func_name):
    fn = getattr(module, func_name, None)
    if not callable(fn):
        return
    def wrapper(*a, **kw):
        t0 = time.perf_counter()
        try:
            return fn(*a, **kw)
        finally:
            rec = calls.setdefault(func_name, {"count": 0, "total_ms": 0.0, "max_ms": 0.0})
            dt = (time.perf_counter() - t0) * 1000
            rec["count"] += 1
            rec["total_ms"] += dt
            rec["max_ms"] = max(rec["max_ms"], dt)
    setattr(module, func_name, wrapper)

for f in ("get_all_tracks", "get_playlist_tracks", "get_recently_played", "get_continue_listening",
          "get_on_repeat", "get_heavy_rotation", "get_search_history", "get_recently_added",
          "get_playlists", "get_all_playlists", "fetch_youtube_metadata",
          "update_theme_from_image", "ensure_artworks_downloaded"):
    instrument(main_module, f)

# ---- cold start ----
t = time.perf_counter()
app = MusicApp()
mark("app_construct")

root = app.build()
app.root = root
mark("kv_build")

# Instrument MusicApp methods that load per-screen data (bound at instance level so
# self.method() calls from switch_screen/on_enter are captured too).
import types
def instrument_method(obj, name):
    fn = getattr(obj, name, None)
    if not callable(fn):
        return
    orig = getattr(fn, "__func__", fn)  # unbound function; wrapper receives self

    def wrapper(self, *a, **kw):
        t0 = time.perf_counter()
        try:
            return orig(self, *a, **kw)
        finally:
            rec = calls.setdefault(name, {"count": 0, "total_ms": 0.0, "max_ms": 0.0})
            dt = (time.perf_counter() - t0) * 1000
            rec["count"] += 1
            rec["total_ms"] += dt
            rec["max_ms"] = max(rec["max_ms"], dt)
    setattr(obj, name, types.MethodType(wrapper, obj))

for meth in ("populate_home_screen_data", "refresh_library_data", "load_search_history_from_db",
             "load_recently_played_data", "load_analytics_data", "load_podcasts_data",
             "sync_favorites_screen", "ensure_player_carousel", "sync_active_playlist_screen",
             "show_auth_dialog", "_update_library_tile", "_populate_playlists_grid",
             "_sync_library_songs", "_stage_1_populate_home", "_stage_2_populate_library_and_history",
             "_stage_3_apply_initial_theme", "_render_podcasts_list", "_render_album_tracks"):
    instrument_method(app, meth)

sm = root.ids.screen_manager

# Instrument lazy screen creation
creation = {}
orig_get_screen = sm.get_screen
def timed_get_screen(name, *a, **kw):
    existed = sm.has_screen(name)
    t0 = time.perf_counter()
    try:
        return orig_get_screen(name, *a, **kw)
    finally:
        if not existed:
            creation[name] = round((time.perf_counter() - t0) * 1000, 2)
sm.get_screen = timed_get_screen

def pump(n=3):
    for _ in range(n):
        Clock.tick()

# Warm up until the splash pipeline completes (headless = synchronous pipeline)
# on_start() is normally invoked by app.run(); call it explicitly so the real
# startup stages are exercised and timed here.
app.on_start()
frames_to_ready = 0
t_ready_start = time.perf_counter()
while frames_to_ready < 240 and not (getattr(app, "_splash_completed", False) and sm.current != "splash"):
    pump(1)
    frames_to_ready += 1
mark("app_ready")
checkpoints[-1]["frames"] = frames_to_ready

# ---- navigation measurements ----
def data_counts():
    out = {}
    try:
        home = sm.get_screen("home")
        for key in ("quick_picks_list", "listen_again_list", "trending_list", "featured_list"):
            if key in home.ids:
                out[key] = len(home.ids[key].data)
        lib = sm.get_screen("library")
        if "songs_list" in lib.ids:
            out["library_songs"] = len(lib.ids["songs_list"].data)
        if "search_results_list" in sm.get_screen("search").ids:
            out["search_results"] = len(sm.get_screen("search").ids["search_results_list"].data)
    except Exception:
        pass
    return out

def navigate(target, settle_frames=3):
    if os.environ.get("BENCH_VERBOSE") == "1":
        print(f"[bench] -> {target}", flush=True)
    t0 = time.perf_counter()
    try:
        app.switch_screen(target)
        call_ms = (time.perf_counter() - t0) * 1000
        pump(settle_frames)
        total_ms = (time.perf_counter() - t0) * 1000
        ok = sm.current == target
        return {"call_ms": round(call_ms, 2), "total_ms": round(total_ms, 2),
                "settled": ok, "data": data_counts()}
    except Exception as e:
        return {"call_ms": -1, "total_ms": -1, "settled": False, "error": str(e)}

results = {
    "mode": MODE,
    "generated_at": datetime.now().isoformat(timespec="seconds"),
    "python": sys.version.split()[0],
    "screen_count": len(SCREEN_NAMES),
    "screens": SCREEN_NAMES,
    "checkpoints": checkpoints,
    "startup_frames_to_ready": frames_to_ready,
    "screen_creation_ms": creation,
    "instrumented_calls": calls,
    "nav_from_home": {},
    "nav_warm_revisit": {},
    "transition_matrix": {},
}

# Baseline: return home and settle
app.switch_screen("home")
pump(3)

# Phase 1: home -> each screen (first visit)
for name in SCREEN_NAMES:
    if name == "home":
        continue
    results["nav_from_home"][name] = navigate(name)
    app.switch_screen("home")
    pump(2)

# Phase 2: warm revisit
for name in SCREEN_NAMES:
    if name == "home":
        continue
    results["nav_warm_revisit"][name] = navigate(name)
    app.switch_screen("home")
    pump(2)

# Phase 3: full transition matrix (opt-in — it re-runs heavy loaders on every hop,
# e.g. 6 SQL queries x2 for analytics, so a complete NxN pass takes minutes).
if os.environ.get("BENCH_FULL_MATRIX") == "1":
    for src in SCREEN_NAMES:
        app.switch_screen(src)
        pump(2)
        row = {}
        for dst in SCREEN_NAMES:
            if dst == src:
                continue
            row[dst] = navigate(dst, settle_frames=1)["total_ms"]
        results["transition_matrix"][src] = row
else:
    results["transition_matrix"]["note"] = "opt-in via BENCH_FULL_MATRIX=1; per-screen home->target and warm revisit measured above"

# ---- persist raw results ----
stamp = datetime.now().strftime("%Y%m%d")
suffix = f"_{TAG}" if TAG else ""
raw_path = os.path.join(OUT_DIR, f"raw_{MODE}_{stamp}{suffix}.json")
with open(raw_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"[bench] {MODE}: startup {checkpoints[-1]['t_ms']:.0f}ms; raw -> {raw_path}", flush=True)
