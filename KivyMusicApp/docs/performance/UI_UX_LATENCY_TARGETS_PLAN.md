# UI/UX Latency Targets — Comparison with Measured Performance & Achievement Plan

Updated: 2026-11-27 · Companion records: `SCREEN_PERFORMANCE_REPORT.md`, `raw_new_20261118_*.json`, `raw_new_20261127_POST_REFACTOR_20261127.json`, `raw_new_20261127_POST_INTERACTION_20261127.json`.

**Verification tiers:** statuses below are **Designed / Implemented** unless explicitly marked **Verified (headless)** or **Verified (device)**. Headless benchmark passes prove work/timing logic only — haptic onset, native ripple, keyboard appearance and true 60/120 Hz drag still need device proof.

---

## 1. What the measurements cover

`tests/benchmark_screen_performance.py new [TAG]` measures blocking work from the **first line of code (imports included)** through cold start and every first-visit / warm-revisit screen hop in headless mode, with no audio playback. It does not measure animation paint, ripple onset, haptics, keyboard or frame-by-frame drag latency.

Measured cold start (first line → app ready):

| Run | `import_main` | `app_ready` | Note |
|---|---:|---:|---|
| Pre-refactor 2026-11-18 | ~1,200 ms | ~2,058 ms | before coordinator/DSP refactor |
| `POST_REFACTOR_20261127` | 5,835.5 ms | 7,782.6 ms | regression from top-level `scipy.signal` import |
| `POST_INTERACTION_20261127` | **1,821.5 ms** | **4,646.1 ms** | lazy SciPy + interaction fixes; ~40% faster than post-refactor |

First-visit / warm revisit in the latest run (ms):

| Screen | first visit | `switch_screen()` call | warm revisit |
|---|---:|---:|---:|
| Search | 60.9 | 3.4 | 38.9 |
| Home (baseline) | 0 | 0 | 0 |
| Player | 719.1 | 644.6 | 34.3 |
| Library | 245.3 | 225.3 | 290.1 |
| Favorites | 472.9 | 409.5 | 50.4 |
| Settings | 1,950.9 | 1,432.0 | 47.1 |
| Equalizer | 947.0 | 826.1 | 28.3 |
| Podcasts | 1,403.2 | 168.4 | 231.4 |

Warm tab work remains inside the 100–200 ms budget; first visits on heavy sub-screens (settings/equalizer/listen-together) are still above budget and are the next performance target.

---

## 2. Target-by-target status (2026-11-27)

| # | Target | Status | Evidence / files |
|---|---|---|---|
| T1 | Play/pause & skip icon morph + haptic 50–100 ms | **Implemented** (headless-verified wiring; device unverified) | `utils/haptics.py` (Android Vibrator API 26+, no-op desktop), `utils/motion.py` canvas-scale pop, `main.py:pop_icon`, `on_press` bindings in `player.kv` / `main.kv`, haptics in `controllers/player_controller.py` |
| T2 | Scrubber follows finger 60–120 Hz, no smoothing lag | **Implemented** (device frame pacing unverified) | `PlayerTimelineSlider` `handle_anim_duration=0`, linear easing, 0.05 s seek-release hold; engine progress tick 1/30 s |
| T3 | Like/shuffle/repeat pop + colour 100–150 ms | **Implemented** | Optimistic flag flip first, async DB persistence with rollback in `toggle_favorite`; haptic confirm + pop on all toggles |
| T4 | Touch ripple < 50 ms | **Likely met, unverified on device** | KivyMD ripple on `on_touch_down`; stale highlights now explicitly cleared on navigation |
| T5 | Bottom-nav tabs 100–200 ms crossfade, no horizontal slide | **Implemented + Verified (headless)** | `NavigationCoordinator.switch_screen()` uses `FadeTransition(duration=0.18)` for tab pairs; `test_simpmusic_ui_ux_parity.py::test_02` asserts fade + direction |
| T6 | Search focus/clear < 150 ms; live non-blocking autocomplete | **Implemented** | `search.kv` `on_text` bound; `SearchCoordinator.on_search_text_change` is O(1) with a 120 ms debounce and local-history/library suggestions; history writes async; clear button moved inside the pill |
| T7 | Swipe-to-like / swipe-to-queue ≤ 150 ms | **Implemented** | `TrackListItem.on_touch_down/move/up` with 12 dp slop / 56 dp threshold, optimistic tint + haptic + toast; `PlayerController.enqueue_track()` |
| T8 | Track menu & Up Next sheet open ~200 ms / dismiss ~150 ms | **Implemented** | `opening_time=0.2`, `closing_time=0.15`, 20-row chunked build in `PlaybackUICoordinator.show_queue_sheet()` |
| T9 | Optimistic UI < 100 ms for playback/library actions | **Mostly implemented** | Favorite/history/DB writes async; `play_selected_track()` still performs some synchronous model/queue work before the screen switch — remaining gap |

**Headline:** cold start is down 3.1 s from the post-refactor regression; all nine interaction targets are implemented or mostly implemented. Remaining risks are first-visit heavy screens and device-only feedback/frame-pacing proof.

---

## 3. Work completed since the previous plan

- **Startup:** `services/dsp_pipeline.py` no longer imports `scipy.signal` at module load. An optional daemon-thread warmup starts 2 s after app start on desktop; DSP chunks use the vectorized path once ready and the pure-NumPy fallback until then.
- **Stale highlights:** `utils/interaction_state.py::clear_press_feedback()` resets Kivy button state and removes ripple canvas groups when leaving a screen or dismissing an overlay (`NavigationCoordinator`).
- **Touch pass-through:** `TouchBlockingFabButton` consumes its own touches; the library FAB no longer leaks taps to song rows behind it.
- **Rounded feedback:** `MDIconButton`/`MDFabButton` ripples now follow circular geometry; `RoundedSettingsItem` rounds the first/last row ripple to the settings card; the search pill and its inline clear button use 28 dp radius.
- **Lyrics:** `clean_song_title()` strips `|`-separated video fluff and `Song - Artist` prefixes; LRCLIB is queried with structured `track_name`/`artist_name` parameters plus ranked fallbacks and debug logging. Verified against the real library title `Maati - MC Square (8D Audio) | Use Headphones | Darken Nights` (841 chars plain / 1,204 chars synced).
- **Content quality:** `utils/content_filters.py` removes tutorial/how-to videos and (by default) AI-generated songs from all track reads, search results and recommendations; Settings → "Show AI-generated songs" re-enables them.
- **Queue sheet:** rows use single-line truncated headline/artist labels with the app's Unicode font (fixes multi-line names and tofu glyphs); the mislabeled tutorial video no longer appears because DB reads are filtered.
- **Latency harness:** debounced suggestions, haptics, icon pops, tab fade and swipe actions are covered by the existing headless suites (UI parity, interactive widgets, coordinator contracts).

---

## 4. Encoded durations — current state

| Encoded value | Location | Target | Verdict |
|---|---|---|---|
| `FadeTransition(duration=0.18)` for tabs | `app_core/navigation_coordinator.py` | T5 | Fixed (was 0.22 s horizontal slide) |
| `SlideTransition(duration=0.18)` for drill-down/back | `app_core/navigation_coordinator.py` | T5 | Fixed (0.22 s on back → 0.18 s) |
| Engine tick `1/30 s` | `services/audio_engine.py` | T2 | Fixed (was 0.1 s / 10 Hz) |
| Slider `handle_anim_duration=0`, linear | `views/components.py`, `player.kv` | T2 | Fixed |
| Seek `is_seeking` hold `0.05 s` | `views/components.py` | T2 | Fixed (was 0.2 s) |
| Sheet `opening_time=0.2`, `closing_time=0.15` | `app_core/playback_ui_coordinator.py`, `catalog_coordinator.py`, `playlist_options_coordinator.py` | T8 | Fixed |
| Suggestion debounce `0.12 s` | `app_core/search_coordinator.py` | T6 | Fixed (was synchronous per keystroke) |
| Stale highlight reset on navigation | `utils/interaction_state.py` | T4 | Fixed |
| Android `VIBRATE` permission + haptics | `buildozer.spec`, `utils/haptics.py` | T1/T3 | Implemented (device verify pending) |
| Ripple radius for icons/settings rows/search pill | `views/components.py`, `settings.kv`, `search.kv` | T4 | Implemented |

---

## 5. Verification status

- **Unit / headless:** full 24-suite battery re-run after the changes; result recorded in `docs/performance/VERIFICATION_RESULTS_20261127.md`. Focused suites (`test_simpmusic_ui_ux_parity.py`, `test_interactive_widgets_audit.py`, `test_app_coordinators.py`) pass with the new fade, haptic/pop bindings and UI classes.
- **Performance telemetry:** `raw_new_20261127_POST_INTERACTION_20261127.json` (headless, 21 screens, no audio). Earlier device probe: `android_device_probe.json`, desktop runtime: `priority7_telemetry_report.json`.
- **Device (not yet proven):** haptic onset, Android ripple paint, soft-keyboard appearance, 60/120 Hz drag frame pacing, library scroll gesture on a real panel, and two-loading-screen visual sequence. Record with 120 fps capture / `adb shell dumpsys` before release.

---

## 6. Remaining work

1. Optimize first-visit cost of settings/equalizer/listen-together (>900 ms) by pre-warming their heavy controls during `deferred_screen_prewarm`.
2. Make `play_selected_track()` fully optimistic (T9) by deferring non-visual model/queue work.
3. Add a dedicated `tests/benchmark_ui_interactions.py` harness that measures callback → paint frames, complementing the screen benchmark.
4. Device-verify all Tier-1 feedback items and library vertical scrolling; capture screenshots alongside the existing `verified_*.png` history.
