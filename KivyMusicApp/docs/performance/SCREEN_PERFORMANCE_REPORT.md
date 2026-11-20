# KivyMusicApp — Screen Performance: Fixes Applied & Re-measurement

Generated: 2026-11-18 · Harness: `tests/benchmark_screen_performance.py`

**Historical records kept alongside this report:**
- `SCREEN_PERFORMANCE_REPORT_BEFORE_FIXES.md` — original analysis
- `raw_new_20261118_BEFORE_FIXES.json`, `raw_classic_20261118_BEFORE_FIXES.json` — original raw data
- `raw_new_20261118_AFTER_FIXES.json`, `raw_classic_20261118_AFTER_FIXES.json` — new raw data
- `raw_new_20261118.json`, `raw_classic_20261118.json` — interim run (same day, pre-fix harness)

Methodology is unchanged: measurement starts at the first line of the harness (before imports), 20 screens, both modes in fresh headless processes, no audio. See the BEFORE report for full per-screen tables and root-cause evidence.

---

## 1. Fixes applied

| # | Fix | Files |
|---|---|---|
| 1 | **Playlists grid converted to a `RecycleView`** with a lightweight `PlaylistTileItem` (recycles ~10 cells instead of eagerly building ~700 widgets); `get_playlist_covers()` fetches all cover art in **one SQL query** instead of 138 `get_playlist_tracks()` calls; grid built **lazily only when the Playlists tab is selected** | `models/database.py`, `views/components.py`, `views/screens/library.kv`, `main.py` |
| 2 | **Startup stage 2 no longer builds the grid** (fallout of #1) | `main.py` |
| 3 | **`yt_dlp` imported lazily** inside `fetch_youtube_metadata()` instead of at module import | `utils/media_utils.py` |
| 4 | **Splash prewarm reduced** from 13 screen trees to 3 high-frequency ones; the other 10 are instantiated one per 1.5 s idle slot **after** the user reaches Home | `main.py` |
| 5 | **Duplicate loaders removed**: analytics & recently_played no longer load in both `switch_screen()` and `on_enter`; podcasts no longer loads twice in `open_podcasts()` | `views/screens.py`, `main.py` |
| 6 | **Loading indicators** on Album/Podcasts screens while their async YouTube data is in flight (property flags set on the main thread / via `Clock.schedule_once`) | `main.py`, `views/screens/album.kv`, `views/screens/podcasts.kv` |

**Regression check:** full master battery **15/15 PASSED**. Total suite wall time dropped from **363 s → 97 s** (~3.7× faster).

---

## 2. Results — New mode

### Startup (cumulative, ms)
| Checkpoint | Before | After | Change |
|---|---:|---:|---:|
| `import_main` | 1,560 | 1,234 | **−326** |
| `app_construct` | 1,707 | 1,313 | −394 |
| `kv_build` | 2,480 | 1,951 | −529 |
| **`app_ready` (splash dismissed, Home populated)** | **5,058** | **2,058** | **−3,000 (−59 %)** |

### Screen transitions (ms, first visit / warm revisit)
| Screen | Before | After | Change |
|---|---:|---:|---:|
| **library** | 5,990 / 6,515 | **69 / 64** | **−99 %** |
| album | 1,629 / 34 | 210 / 30 | −87 % first |
| podcasts | 1,089 / 98 | 569 / 83 | −48 % first |
| recently_played | 659 / 52 | 620 / 44 | similar (one-time tree) |
| settings | 479 / 40 | 329 / 48 | −31 % first |
| equalizer | 415 / 52 | 400 / 83 | ~same (one-time tree) |
| listen_together | 397 / 31 | 303 / 24 | −24 % first |
| artist | 323 / 43 | 108 / 34 | −67 % first |
| analytics | 206 / 58 | 171 / 54 | −17 % first |
| all others | 20–205 | 27–158 | within noise / slight gains |

### Instrumented hot spots
| Function | Before (calls / total ms) | After (calls / total ms) |
|---|---:|---:|
| `refresh_library_data` | 3 / **10,447** | 3 / **105** |
| `_populate_playlists_grid` | 3 / 10,352 | 0 / 0 (lazy; runs only on tab tap) |
| `_stage_2_populate_library_and_history` | 1 / 2,492 | 1 / **26** |
| `get_playlist_tracks` | **433 / 136** | **7 / 8** |
| `load_recently_played_data` | 4 / 306 | **2 / 100** |
| `load_analytics_data` | 4 / 53 | **2 / 28** |
| `fetch_youtube_metadata` (worker thread) | 1 / 2,886 | 1 / 2,267 |

---

## 3. Results — Classic mode

| Metric | Before | After | Change |
|---|---:|---:|---:|
| `app_ready` | 4,133 ms | **2,050 ms** | **−50 %** |
| Library first / warm | 6,112 / 6,434 ms | **73 / 81 ms** | **−99 %** |
| `refresh_library_data` | 3 / 10,178 ms | 3 / **117 ms** | −99 % |
| `_stage_2` | 1 / 2,087 ms | 1 / **24 ms** | −99 % |
| `get_playlist_tracks` | 433 calls | **7 calls** | −98 % |
| `load_analytics_data` | 4 calls | **2 calls** | duplicate removed |
| Album first / Podcasts first | 1,662 / 1,091 ms | 196 / 576 ms | −88 % / −47 % |

Performance parity between modes is preserved — both benefit equally because the fixes are in shared backend code.

---

## 4. What remains

- **First-visit widget construction** still costs ~300–400 ms for `settings`, `equalizer`, `listen_together`, `favorites`. In the animated (non-headless) app these are now built in idle slots after launch; direct first navigation still pays the one-time cost. A loader/skeleton per screen would be the next polish step if desired.
- **Async network waits** (album/podcasts) still take ~2 s of wall time in the worker thread; fix #6 now shows an explicit loading label instead of apparently empty screens.
- Import cost is now ~1.2 s total; remaining contributors are Kivy/KivyMD startup and `PlaylistModel` loading 244+ tracks from SQLite — further gains would require a lighter schema or a background/cached library index.
- Absolute timings vary ~±40 % with machine load (the same code measured `app_ready` 5.06 s and 8.27 s in earlier runs); call counts and deltas are the robust signal.

## 5. Verification

- Master battery: **15/15 PASSED** (`OVERALL RESULT: 100% OF TESTS PASSED WITH ZERO CRASHES OR REGRESSIONS`), suite time 363 s → 97 s.
- Visual: the new `PlaylistTileItem` RecycleView grid renders correctly (Create tile + 143 playlist tiles, 3 columns, artwork and counts).
- Re-run: `python -X utf8 tests\benchmark_screen_performance.py new AFTER_FIXES` (same for `classic`); results saved alongside the baseline files listed above.
