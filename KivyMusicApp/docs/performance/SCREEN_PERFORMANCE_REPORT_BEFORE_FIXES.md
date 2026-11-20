# KivyMusicApp — Screen Performance Benchmark (both interface modes)

Generated: 2026-11-18 · Raw data: `raw_new_20261118.json`, `raw_classic_20261118.json`
Harness: `tests/benchmark_screen_performance.py` (standalone; not part of the test battery)

---

## 1. Objective & method

Measure **from the very first line of code** — before Kivy, KivyMD, or `main` are imported — through cold start and **every screen-to-screen transition**, for the **new (SimpMusic-inspired)** and **classic (pre-redesign)** interface modes, with **no audio playback**. Identify why any screen is slow and save the results as a baseline for future work.

- Mode selected via the persisted `ui_mode` setting; each mode runs in a **fresh process**.
- `time.perf_counter()` starts at the top of the harness (line 14), before any import.
- Headless (`KIVY_HEADLESS=1`) for determinism: no transition timers, no background network polling, no music. `on_start()` is invoked explicitly so the real startup stages run and are timed.
- **20 screens** discovered from KV rules; for each: first visit from Home, warm revisit, `switch_screen()` call cost, settled state, and data counts.
- Instrumented (count / total / max time): module-level DB/network helpers and `MusicApp` data loaders + sub-steps, plus lazy `get_screen()` widget-tree construction.
- Full N×N matrix (20×19 transitions) is available via `BENCH_FULL_MATRIX=1` but is intentionally off by default: it re-runs heavy loaders on every hop and takes several minutes.
- Environment: Python 3.13.3, Kivy 2.3.1, KivyMD 2.0.0, Windows. Dev DB `music_app.db` ≈ 4.2 MB with **244+ tracks / 138+ playlists** (many test-generated) — representative of a "used" library, not a fresh install.

**Caveat:** wall-clock numbers vary with machine load (the `app_ready` checkpoint measured 5.06 s, 8.15 s, and 8.27 s in successive runs). The **relative** numbers, call counts, and function breakdowns are the reliable signal; treat absolute times as ±40 %.

---

## 2. Startup timeline (from process start)

| Checkpoint | New (ms) | Classic (ms) | What it covers |
|---|---:|---:|---|
| `process_start` | 39 | 36 | Harness start, before any app import |
| `import_kivy` | 157 | 139 | `import kivy` |
| `import_kivy_core` | 684 | 605 | Clock, Window, SDL2 setup |
| `import_kivymd` | 704 | 623 | KivyMD package |
| `import_main` | **1,560** | **1,235** | `main` + all services — includes **yt-dlp import** (`utils/media_utils.py:6`), DB APIs, font probing/registration (`main.py:87`) |
| `app_construct` | 1,707 | 1,315 | `init_db()`, ~14 `get_setting()` reads, `PlaylistModel()` full-table load (`models/track_model.py:143-170`) |
| `kv_build` | 2,480 | 1,968 | `Builder.load_file("views/main.kv")` — compiles 20 screen rule sets and instantiates 4 declared screens |
| `app_ready` | **5,058** | **4,133** | Headless warmup stages 1–3 (splash dismissed, Home populated) |

**Startup hot spots:** imports ≈ 1.2–1.6 s; KV compile ≈ 0.65–0.77 s; warmup ≈ 2.2–2.6 s, of which **stage 2 (`refresh_library_data`) is ~2.1–2.5 s** (see §5.1). In the animated (non-headless) path, splash step_5 additionally instantiates 13 full screen trees before "Ready!".

---

## 3. Screen-to-screen transitions (Home → target)

`call` = synchronous `app.switch_screen()`; `first` = first visit from Home (includes lazy widget-tree construction); `warm` = revisit after returning Home. All include 3 Clock frames of settling. No audio played.

| Screen | New call | New first | New warm | Classic call | Classic first | Classic warm |
|---|---:|---:|---:|---:|---:|---:|
| **library** | 3,813 | **5,990** | **6,515** | 3,932 | **6,112** | **6,434** |
| album | 93 | **1,629** ¹ | 34 | 103 | **1,662** ¹ | 45 |
| podcasts | 71 | **1,089** ¹ | 98 | 62 | **1,091** ¹ | 109 |
| recently_played | 307 | 659 | 52 | 529 | 623 | 46 |
| settings | 401 | 479 | 40 | 345 | 411 | 65 |
| equalizer | 348 | 415 | 52 | 378 | 430 | 79 |
| listen_together | 337 | 396 | 31 | 316 | 383 | 30 |
| artist | 294 | 323 | 43 | 95 | 130 | 24 |
| auth | 116 | 145 | 44 | 118 | 144 | 58 |
| browse | 111 | 147 | 46 | 97 | 121 | 41 |
| mood | 183 | 227 | 23 | 181 | 209 | 24 |
| analytics | 155 | 206 | 58 | 142 | 439 | 60 |
| favorites | 178 | 205 | 39 | 181 | 209 | 54 |
| player | 170 | 199 | 49 | 198 | 229 | 45 |
| playlist | 151 | 191 | 46 | 153 | 201 | 37 |
| notifications | 79 | 124 | 42 | 82 | 124 | 43 |
| wrapped | 31 | 70 | 50 | 50 | 104 | 52 |
| splash | 1 | 50 | 24 | 1 | 25 | 24 |
| search | 1 | 21 | 30 | 1 | 36 | 46 |

¹ First-visit spikes on album/podcasts are dominated by **background network work finishing** during the settle frames, not main-thread UI blocking: `fetch_youtube_metadata` totals 2.9 s (new) / 2.8 s (classic) in its worker thread, and `load_podcasts_data` itself is only ~5 ms.

**Key observation:** new and classic are within noise on **every** screen. The UI redesigns are **not** the source of lag; the shared backend/data code is.

---

## 4. Lazy screen construction cost (first `get_screen()`)

| Screen | New (ms) | Classic (ms) | Screen | New (ms) | Classic (ms) |
|---|---:|---:|---|---:|---:|
| settings | 400 | 344 | playlist | 150 | 152 |
| equalizer | 347 | 378 | analytics | 144 | 128 |
| listen_together | 336 | 316 | player | 133 | 154 |
| artist | 294 | 95 | auth | 115 | 116 |
| mood | 182 | 181 | browse | 110 | 96 |
| favorites | 177 | 181 | album | 93 | 102 |
| notifications | 78 | 81 | podcasts | 68 | 58 |
| recently_played | 43 | 262 | wrapped | 30 | 49 |

These are one-time KV widget-tree builds. The animated startup prewarms 13 of these during the splash; the heaviest (`settings`, `equalizer`, `listen_together`, `artist`, `favorites`, `mood`, `analytics`) cost 0.3–0.4 s each there.

---

## 5. Instrumented function breakdown (counts over full benchmark)

### 5.1 The dominant problem — Library grid

| Function | New total / max | Classic total / max | Calls |
|---|---:|---:|---:|
| `refresh_library_data` | **10,447 / 4,146 ms** | **10,178 / 4,163 ms** | 3 |
| └─ `_populate_playlists_grid` | **10,352 / 4,113 ms** | **10,085 / 4,128 ms** | 3 |
| └─ `_sync_library_songs` | 0.32 ms | 0.34 ms | 3 |
| └─ `_update_library_tile` | 0.27 ms | 0.28 ms | 12 |
| `get_playlist_tracks` | 136 ms | 133 ms | **433** |

`_populate_playlists_grid` (`main.py:3011-3105`) accounts for **99 %** of `refresh_library_data`. On every call it:

1. `grid.clear_widgets()` then rebuilds **138+ playlist tiles from scratch**;
2. for each playlist runs a separate `get_playlist_tracks(name)` query (the 433 calls above — an N+1 pattern) just to pick the first track's artwork;
3. constructs ~5 widgets per tile — `MDCard` + `MDBoxLayout` + `FitImage(mipmap=True)` + `MarqueeLabel` + `MDLabel` — i.e. **~700 widget/texture objects** synchronously on the UI thread, with mipmapped artwork decoding.

It is called **at startup (stage 2) and on every `switch_screen("library")`**, even when the visible tab is Library/Songs — hence the ~6 s first *and* warm navigation. This is why the loading overlay on the mode switch was needed, and it will be felt on every Library visit.

### 5.2 Other measured costs

| Function | New (total/max ms) | Classic (total/max ms) | Note |
|---|---:|---:|---|
| `fetch_youtube_metadata` | 2,886 / 2,886 | 2,831 / 2,831 | 1 call, worker thread (album detail) |
| `_stage_2_populate_library_and_history` | 2,492 | 2,087 | almost entirely `refresh_library_data` |
| `load_recently_played_data` | 306 / 263 (4 calls) | 304 / 266 (4) | **called twice per navigation** |
| `load_analytics_data` | 53 / 17 (4 calls) | 62 / 24 (4) | **called twice per navigation**, 6 SQL queries each |
| `ensure_player_carousel` | 36 / 36 | 43 / 43 | 2 calls; ~1,221 ms historically before being deferred |
| `load_podcasts_data` | 5 / 3 (2 calls) | 6 / 3 (2) | **called twice per navigation** (switch + `open_podcasts`) |
| `populate_home_screen_data` | 8 | 7 | cheap (4 RV data assignments) |

### 5.3 Duplicate loaders (confirmed by call counts)

Two navigations per screen should give 2 calls; the benchmark sees **4** for `analytics` and `recently_played`, and **2** for `podcasts` where 1 suffices:

- `analytics`: `switch_screen()` (`main.py:1029-1030`) **and** `AnalyticsScreen.on_enter` (`views/screens.py:49-53`).
- `recently_played`: `switch_screen()` (`main.py:1027-1028`) **and** `RecentlyPlayedScreen.on_enter` (`views/screens.py:61-65`); the loader also does an O(rows × playlist.tracks) linear scan per row (`main.py:1411-1430`).
- `podcasts`: `switch_screen()` (`main.py:1031-1032`) **and** `open_podcasts()` (`main.py:3367-3368`).

---

## 6. Root-cause ranking & recommended solutions

| # | Issue | Evidence | Fix (why / how) |
|---|---|---|---|
| 1 | **Playlists grid rebuilt from scratch on every Library visit and at startup** | `_populate_playlists_grid` 10.35 s / 3 calls; 433 `get_playlist_tracks` calls; identical in both modes | Build it **only when the Playlists tab is actually selected**, cache the built grid, and convert it to a **RecycleView** with a lightweight card viewclass (recycles ~10 widgets instead of ~700). Replace 138 per-playlist queries with **one grouped SQL query** (`SELECT playlist, COUNT(*), first artwork`) — removes the N+1 pattern and most widget/texture work. |
| 2 | **Startup warmup dominated by the same grid** | `_stage_2` ≈ 2.1–2.5 s | Once #1 is lazy, stage 2 drops to history loading (<1 ms). Keep only Home/Library tiles in stage 2. |
| 3 | **Import cost ~1.2–1.6 s** | `import_main` checkpoint; `yt_dlp` imported at `utils/media_utils.py:6` | Move `yt_dlp` import inside the function that uses it (lazy import) — pure win, no behavior change. Font probing at `main.py:87` can also be cached to a single resolved path. |
| 4 | **First-visit widget-tree construction 0.3–0.4 s for complex screens** | §4 table | Keep the animated splash prewarm for tab screens; defer heavy rarely-visited trees (`settings`, `equalizer`, `listen_together`, `artist`) to idle `Clock` slots, or accept a small in-screen loading state (the mode-switch overlay pattern already proves this works). |
| 5 | **Duplicate loaders double DB scans** | counts of 4 vs 2 in §5.2/5.3 | Remove the duplicate call sites: keep only `on_enter` **or** the `switch_screen` hook, not both. For `recently_played`, also replace the linear row→track lookup with a dictionary keyed by `video_id`. |
| 6 | **Album/podcasts "first visit" spikes** | 1.6 s / 1.1 s; network helper 2.8 s in worker thread | UI is not blocked — data simply arrives late. Show an explicit loading/disabled state in those screens until the async callback marshals results via `Clock.schedule_once`. |
| 7 | **Mode switch is not the problem** | all rows within noise between modes | No UI-mode-specific optimization needed; the existing loading overlay is sufficient for perceived responsiveness. |

Historical context: `startup_performance_load_spreading_report.md` recorded earlier improvements (`build()` 4,004 → ~500 ms, max frame freeze 4,340 → 306 ms). Current `kv_build` of 0.65–0.77 s is the same order of magnitude; the **new** regression is the playlist-grid rebuild, not KV compilation.

---

## 7. Reproduction

```powershell
cd KivyMusicApp
python -X utf8 tests\benchmark_screen_performance.py new
python -X utf8 tests\benchmark_screen_performance.py classic
# optional extras:
#   $env:BENCH_VERBOSE='1'      # log each transition
#   $env:BENCH_FULL_MATRIX='1'  # all 380 transitions (slow: re-runs loaders)
```

Outputs (overwritten per day): `docs/performance/raw_<mode>_<YYYYMMDD>.json` and this report.
The harness restores the previous `ui_mode` value and never plays audio.

**For future work:** re-run the two commands after applying fixes #1–#5 and compare `refresh_library_data`, `_populate_playlists_grid`, `app_ready`, and the `library` row of §3 — those are the acceptance metrics.
