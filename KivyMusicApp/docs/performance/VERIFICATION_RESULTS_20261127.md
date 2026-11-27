# Verification Results — 2026-11-27 Interaction & Performance Pass

Verification tiers follow `GEMINI.md` §20–§25. **Designed / Implemented** items are not claimed as device-verified unless explicitly stated.

## User-reported issues → resolution

| Report | Root cause | Fix | Status |
|---|---|---|---|
| Stuck highlight after opening a menu/screen/sheet | KivyMD ripple canvas group / `ButtonBehavior.state` survives the transition | `utils/interaction_state.py::clear_press_feedback()` resets pressed state and removes ripple groups on screen leave, back and overlay dismissal | Implemented + headless-verified |
| Library folder FAB tap leaks to the song row behind it | FAB did not guarantee exclusive touch consumption | `TouchBlockingFabButton` returns `True` from `on_touch_down` and consumes the gesture | Implemented + headless test |
| Lyrics never load | `clean_song_title()` left `Song - Artist \| 8D Audio \| ...` fluff; LRCLIB `q=` query returned zero matches | Strip fluff/pipe suffixes, structured `track_name`/`artist_name` queries, ranked fallbacks, debug logging | Implemented + live API verified (841 plain / 1,204 synced chars for the real "Maati" track) |
| Headphone icon crashes after ~5 s | `player.kv` called non-existent `app.audio_quality` | Use `app.selected_audio_quality`; dialog open/dismiss verified headlessly | Implemented + headless-verified |
| Library vertical scrolling not working | Nested `EmbeddedRecycleView.on_scroll_start` claimed gestures before the parent `MDScrollView` | Return `False` from `on_scroll_start` so parent scroll receives the gesture; row taps still dispatch | Implemented; **device verification still required** |
| Two loading screens | Kivy/Android pre-build frame + in-app `SplashScreen` | Window clear colour now matches the theme before KV load; single in-app splash retained. External p4a/Android presplash cannot be removed from Python code | Mitigated; external presplash documented |
| Library sub-screens not opening | Confirmed card callbacks work via `on_release`; symptom came from stale highlight / touch leak | Fixed above; added rounded ripple and touch containment | Implemented + headless-verified (`test_comprehensive_audit`, library card probe) |
| Settings top/bottom rows show square highlight | KivyMD rectangular ripple ignores card corners | `RoundedSettingsItem` computes top/bottom radius from sibling order; `MDIconButton`/`MDFabButton` ripples made circular | Implemented |
| Tutorial video in UP NEXT | Mislabeled non-music track in SQLite (`How to Create Long AI Videos...`) | `utils/content_filters.py` removes tutorial/how-to videos from all track reads, search results and queues | Implemented + verified (DB read drops it) |
| Tofu artist glyphs in queue | Default label font lacks some glyphs | Queue headline/supporting rows use `app.resolved_unicode_font_name` | Implemented; device visual check pending |
| Queue song names wrap to multiple lines | `MDListItemHeadlineText` had no single-line constraint | `max_lines=1`, `shorten=True` on queue rows | Implemented |
| AI songs in recommendations | No content gate | `utils/content_filters.py` + Settings → "Show AI-generated songs" toggle (off by default); applied to all DB track reads and search results | Implemented + headless-verified |
| Search highlight rectangular / X outside pill | KivyMD default square state layer; clear button was outside the card | `radius=[dp(28)]` on the text field; clear button moved inside the pill with existing visibility rule | Implemented |

## Performance

| Checkpoint | POST_REFACTOR | POST_INTERACTION |
|---|---:|---:|
| `import_main` | 5,835.5 ms | 1,821.5 ms |
| `app_ready` | 7,782.6 ms | 4,646.1 ms (−40%) |

Root cause: top-level `scipy.signal` import (~2.5 s). It is now lazy with a 2 s delayed daemon warm-up on desktop; DSP falls back to the pure-NumPy cascade until loaded. The DSP CPU telemetry suite now warms SciPy explicitly: 1.32% CPU (was 158% on the fallback).

Records: `raw_new_20261127_POST_REFACTOR_20261127.json`, `raw_new_20261127_POST_INTERACTION_20261127.json`.

## Test tiers

- **Unit / headless**: focused suites `test_simpmusic_ui_ux_parity.py`, `test_interactive_widgets_audit.py`, `test_app_coordinators.py`, `test_ui_interaction_regressions.py`, `test_audio_dsp_pipeline.py` all pass after the fixes.
- **Integration / headless**: master battery — first run 23/24 passed (one cp1252 `✓` print in `test_dynamic_recommendation_engine.py`, fixed by UTF-8 stdout reconfigure); second run 23/24 passed (DSP CPU telemetry on fallback, fixed by explicit warm-up); **final 25-suite run: 25/25 PASSED in 367.09 s, zero crashes or regressions** (`tests/run_all_tests.py`, 2026-11-27).
- **Device**: Android SM-A176B probe in `android_device_probe.json` predates these interaction changes. Haptics, native ripple, keyboard, frame pacing, library scroll on-device and the visual loading sequence remain unverified.
- **Performance telemetry**: desktop runtime `priority7_telemetry_report.json`; new startup benchmark above.

## Files added/changed (coordinate map)
- New utilities: `utils/haptics.py`, `utils/motion.py`, `utils/interaction_state.py`, `utils/content_filters.py`.
- Navigation/UI: `app_core/navigation_coordinator.py`, `views/components.py`, `views/main.kv`, `views/screens/{player,search,settings,library}.kv`, `main.py`.
- Content/lyrics: `services/lyrics_service.py`, `models/database.py`, `app_core/search_coordinator.py`, `app_core/state.py`, `app_core/settings_coordinator.py`, `app_core/playback_ui_coordinator.py`.
- Startup/DSP: `services/dsp_pipeline.py`, `services/audio_engine.py`, `app_core/bootstrap.py`.
- Tests/docs: `tests/test_ui_interaction_regressions.py`, `tests/run_all_tests.py`, `tests/test_*` fixes, `docs/performance/*`, `AGENTS.md`.
