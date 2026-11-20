# UI/UX Latency Targets — Comparison with Measured Performance & Achievement Plan

Generated: 2026-11-18 · Companion documents: `SCREEN_PERFORMANCE_REPORT.md` (post-fix results), `SCREEN_PERFORMANCE_REPORT_BEFORE_FIXES.md` (baseline), `raw_*_BEFORE_FIXES.json`, `raw_*_AFTER_FIXES.json`

---

## 1. What the existing measurements actually cover

The screen benchmark measured **work/blocking time from process start and per navigation** (first visit / warm revisit / `switch_screen()` call) in headless mode, for both modes. It did **not** measure animation durations, ripple onset, keyboard focus, frame-by-frame drag latency, or haptics. Those must be measured with a new interaction harness (§5) — the comparison below is therefore explicitly split into **measured** and **not-yet-measured** items.

Post-fix measured navigation (new mode, headless, ms):

| Screen | first visit | `switch_screen()` call | warm revisit |
|---|---:|---:|---:|
| Home (baseline) | 0 | 0 | 0 |
| Search | 42 | 0.7 | 28 |
| Library | 69 | 44 | 64 |
| Player | 155 | 118 | 44 |
| Album | 210 | 158 | 30 |
| Settings | 329 | 285 | 48 |
| Equalizer | 400 | 314 | 83 |
| Podcasts | 569 | 63 | 83 |
| Favorites | 385 | 358 | 51 |

Startup: first line of code → Home populated = **2,058 ms** (splash covers this); library grid rebuild eliminated (6,000 ms → 69 ms); 15/15 tests pass; battery 363 s → 97 s.

---

## 2. Target-by-target comparison

| # | Target | Evidence from measurements | Status |
|---|---|---|---|
| T1 | Play/pause & skip icon morph + haptic **50–100 ms**, independent of audio buffering | Not timed in benchmarks. Audit: icon bindings are already **optimistic** (`audio_engine.start_play()` returns immediately, `player_controller.py:233`); no haptic code exists anywhere and no pop animation. | **Partial** — add haptics + pop |
| T2 | Seek bar/scrubber follows finger at **60–120 Hz (8.3–16.6 ms/frame)**, zero smoothing lag | Not timed. Audit found KivyMD `MDSlider.handle_anim_duration = 0.2 s` default → **200 ms thumb lag**; audio progress tick `0.1 s` = **10 Hz**; `is_seeking` hold `0.2 s`. | **Fails (3 configured delays)** |
| T3 | Like/shuffle/repeat toggle pop/color change **100–150 ms** | Not timed. Color/icon KV rebind is instant, but favorite does a **synchronous SQLite write before flipping `is_favorite`** (`player_controller.py:159-160`); no pop animation, no haptics. | **Partial** |
| T4 | Touch ripple begins **< 50 ms** on finger contact | Not timed. KivyMD native ripple on touch-down; no app-level delay or config. | Likely met — verify |
| T5 | Bottom nav Home/Search/Library switching **100–200 ms**, crossfade 150–200 ms, **no horizontal slide** | Warm work 28–64 ms (good), but code uses `SlideTransition(duration=0.22)` **horizontally** for tabs (`main.py:1015-1024`). | **Fails (type + 20 ms over)** |
| T6 | Search bar focus + keyboard/clear **< 150 ms**; live autocomplete non-blocking | Search warm nav 28 ms / call 0.7 ms (container instant); network results already threaded + `Clock.schedule_once`. But there is **no `on_text` binding at all** — search fires only on Enter, no live suggestions; no keyboard config. | **Fails (autocomplete absent)** |
| T7 | Swipe-to-queue / swipe-to-like **execute or snap back within 100–150 ms of release** | No swipe recognizers on track rows exist (`TrackListItem` has `on_release` only). | **Fails (feature absent)** |
| T8 | 3-dot track menu & Up Next queue sheet open ~**200 ms**, dismiss ~**150 ms** | Not timed. Audit: KivyMD `opening_time=0.2` (on target), `closing_time=0.2` (**50 ms over**); queue rows pre-chunked at 0.03 s; track-options sheet leaks on every open. | **Open OK, dismiss fails** |
| T9 | Optimistic UI updates **< 100 ms** for playback/library actions | Not timed. Play flags are optimistic; favorite DB write, search-history insert, and `play_selected_track()` do synchronous DB/engine work before visual updates. | **Partial** |

**Headline:** the post-fix backend numbers already satisfy the *work* budget of every Tier-2 target (warm navigation 28–83 ms). The remaining risk is entirely in **animation, gesture, and feedback layers** — which the previous harness did not time. That is where the plan below focuses.

---

## 3. Implementation plan

### Tier 1 — micro-interactions

**T1 — Play/pause & skip icon morph + haptic (50–100 ms, optimistic)**
- **Current gap:** icon bindings are **already optimistic** — `audio_engine.start_play()` returns `True` immediately and spawns its download in a worker (`services/audio_engine.py:126-181`), so `is_playing` flips in the same frame (`controllers/player_controller.py:233`); pause flips immediately too (`:249`). The actual misses are: **no haptic feedback anywhere in the app** and **no icon morph/pop animation** (icon is a plain KV conditional at `views/main.kv:120-130` and `views/screens/player.kv:125-138`). Inline Discord RPC calls on the tap path (`:234-240`, `:250-257`) add avoidable work.
- **Haptics:** add a tiny `utils/haptics.py` using pyjnius `Vibrator.vibrate(10 ms)` on Android (add `VIBRATE` permission to `buildozer.spec`), no-op on desktop; call it synchronously in the icon's `on_release` before engine work (main thread only).
- **Change:** reuse the `pop_icon()` helper from T3 on the play/pause and skip buttons (scale 1.15 → 1.0 in ~100 ms total so the morph is visible, not just a static icon swap); keep the optimistic flag flip exactly where it is; move Discord RPC updates into a `Clock.schedule_once` callback so they never sit on the tap path.
- **Acceptance:** with the audio engine artificially delayed 2 s in a test hook, tap → icon change + haptics call ≤ 100 ms.

**T2 — Seek bar / scrubber (60–120 Hz, no smoothing lag)**
- **Current:** `views/components.py:694-770` `PlayerTimelineSlider` tracks the finger and only issues `seek()` on release. Three configured delays break the target: (1) KivyMD's default **`handle_anim_duration = 0.2 s`** with `out_circ` easing makes the thumb lag touch by ~200 ms (vendored doc `docs/api/kivymd_api.md:6306-6311`), (2) the audio-engine progress tick is **`Clock.schedule_interval(..., 0.1)` = 10 Hz** (`services/audio_engine.py:463`), (3) `is_seeking` is held for **0.2 s** after release (`views/components.py:767`). It also writes `current_time`/`formatted_current_time` twice per frame (`on_value` 711-721 and `on_touch_move` 742-753) and re-fetches `MDApp.get_running_app()` per event.
- **Change:** set `handle_anim_duration: 0` and `handle_anim_transition: "linear"` on `PlayerTimelineSlider` (in `__init__` defaults at `:704-709` and in `player.kv:89-98`) so the thumb equals the finger in the same frame; raise the engine tick toward 1/60 s (or interpolate between decoder polls) so idle progress is smooth; shorten the release hold to ~0.05 s; keep one write path (`on_value` only), cache the controller in `__init__`, and let KV format the time label instead of allocating a string per frame.
- **Acceptance:** during a scripted drag, value change and thumb position occur in the same `Clock.tick()`; frame time ≤ 16.6 ms (60 Hz), target ≤ 8.3 ms on 120 Hz devices. Measure on device with `Clock.get_fps()`/high-speed capture.

**T3 — Like / shuffle / repeat pop (100–150 ms)**
- **Current:** icons are KV bindings to controller booleans (`player.kv:36-39, 114-119, 140-145`; mini player `main.kv:113-118`) so the color swap is immediate once the flag flips, but `toggle_favorite()` (`player_controller.py:153-164`) does a **synchronous SQLite write before** setting `is_favorite`, and shuffle/repeat do inline state/audio work. No pop animation and no haptics.
- **Change:** flip the property first, then write SQLite / update engine / Discord via `Clock.schedule_once` (worker for DB), reverting only on failure. Add a reusable `pop_icon(widget)` helper: `Animation(scale=1.2, duration=0.05) + Animation(scale=1.0, duration=0.10)` (~150 ms total) invoked from the three toggle callbacks, plus the haptic tick from T1.
- **Acceptance:** tap → visible color/icon change ≤ 100 ms; pop animation completes ≤ 150 ms even with a mocked 2 s DB/network delay.

**T4 — Ripple / press state (< 50 ms)**
- **Current:** `MDCard` with `ripple_behavior: True` is used on the mini player (`views/main.kv:66-73`), Up Next pill (`player.kv:148-158`), genre tiles (`search.kv:169-351`) and other cards; `MDIconButton`/`MDFabButton`/`MDListItem`/`MDChip` carry KivyMD ripples automatically. KivyMD starts the ripple on `on_touch_down` with no app-level delay — likely compliant, but unmeasured.
- **Change:** verification-first. Audit that every actionable widget still has `ripple_behavior: True` and is not covered by a transparent/disabled overlay; if a measured onset exceeds 50 ms, subclass the widget to paint an immediate full-opacity highlight circle in `on_touch_down` (zero-frame onset) and let KivyMD's ripple play over it.
- **Acceptance:** touch-down → ripple visual ≤ 50 ms (high-speed capture on device; headless can only verify no scheduling delay in the handler chain).

### Tier 2 — rapid navigation

**T5 — Bottom-nav tabs (100–200 ms, crossfade, no horizontal slide)** ← *confirmed gap*
- **Current:** `main.py:switch_screen()` uses a `SlideTransition(duration=0.22)` from `views/main.kv:51`, re-applied at `:1015-1016`, and tab-to-tab switches explicitly set `direction = "left"/"right"` via `tab_indices` (`:1018, 1023-1024`) — a 220 ms **horizontal slide**, wrong type and 20 ms over. Player entry/exit uses up/down (fine). `go_back()` also uses the slide (`:1096-1102`).
- **Change:** when both `old_screen` and `screen_name` are in the tab set, use `FadeTransition(duration=0.18)` (inside 150–200 ms, no horizontal motion); keep directional slides for drill-down/back. Update `views/main.kv:51` default to `FadeTransition(duration=0.18)` if universal crossfade is wanted, and set `indicator_duration: 0.15` on `NavBarItem` to match. Measured warm tab work is already 28–64 ms, so total stays under 200 ms. Update the direction assertion in `tests/test_simpmusic_ui_ux_parity.py:57-104` to accept the fade for tabs.

**T6 — Search focus/clear (< 150 ms) + live non-blocking autocomplete**
- **Current:** search field `views/screens/search.kv:27-40` has **no `on_text` binding** — search only fires on Enter via `on_text_validate: app.perform_search(self.text)` (`:36`); classic mode only has static suggestion chips. Clear button (`:41-47`) calls `app.clear_search_input()` instantly (`main.py:731-742`). Network results are already non-blocking (worker + `Clock.schedule_once` in `main.py:3697-3699, 3778-3786`), but `add_search_history(q)` is a synchronous DB write on the main thread (`:3633`). No keyboard/softinput config.
- **Change:** add `on_text: app.on_search_text(self.text)` with `Clock.unschedule`/`Clock.schedule_once(..., 0.12)` debounce; run a local-library prefix match instantly in the callback and optional remote suggestions on a worker marshalled back to a `RecycleView`; move history inserts off-thread. Set `multiline: False` and `Window.softinput_mode = "below_target"`, focus the field via `Clock.schedule_once(..., 0)` when the tab is entered. Keep clear optimistic.
- **Acceptance:** focus + keyboard request ≤ 150 ms; per-keystroke handler ≤ 16 ms; suggestions appear without input stalls.

**T7 — Swipe to queue / swipe to like (execute/snap-back ≤ 100–150 ms)**
- **Current:** **no swipe recognizers on track rows** — `TrackListItem` (`views/components.py:355-386`), `HomeCardItem`, `QuickPicksItem` only implement `on_release`; `DirectionalHorizontalScrollMixin` (`:254-307`) arbitrates scroll direction (slop `dp(8)`) but has no action threshold. The only content swipe is the album-art `Carousel` → track change (`player.kv:52-56`).
- **Change:** add `on_touch_down/move/up` to `TrackListItem` with a `dp(40)` horizontal threshold; on crossing, flip the visual like/enqueue state optimistically + haptic; on release, either execute the action or animate snap-back with `Animation(x=orig_x, duration=0.12)`. Grab the touch so the parent RV doesn't also scroll, respecting `EmbeddedRecycleView` arbitration (`:309-346`).
- **Acceptance:** finger-up → action or settled snap-back ≤ 150 ms.

### Tier 3 — brisk overlays

**T8 — 3-dot track menu & Up Next queue sheet (open ~200 ms, dismiss ~150 ms)**
- **Current:** 3-dot menu `main.py:2580-2619` builds a fresh `MDBottomSheet` per open (`height="360dp"`, `Window.add_widget` at `:2615`) and never removes it — a widget leak. Up Next `main.py:4188-4268` caches its sheet (`460dp`), builds 20 rows synchronously and the rest in `0.03 s` chunks (`:4250-4266`). Both inherit KivyMD `opening_time = 0.2 s` (on target) and **`closing_time = 0.2 s` (50 ms over target)** from `navigationdrawer.py:1288,1304`.
- **Change:** set `closing_time: 0.15` on both sheet instances before opening (keep `opening_time: 0.2`); cache/reuse the options sheet and remove it from `Window` on dismiss; prebuild queue rows before the open animation so no work overlaps the 200 ms slide. Ensure outside-tap and swipe-down dismissal use the same fast close path.
- **Acceptance:** measured open ≈ 200 ms, dismiss ≈ 150 ms; no frame >16.6 ms during the slide.

**T9 — Optimistic UI (< 100 ms) for playback/library actions**
- **Current:** playback flags are optimistic (`player_controller.py:200,233,249`), but non-visual work runs synchronously on tap: `toggle_favorite()` DB write before flag flip (`:159-160`), `perform_search()` history insert (`main.py:3633`), and `play_selected_track()` (`main.py:1894-1911`) does `add_track`, `set_track` (which runs `is_favorite`/`mark_track_played` queries + engine cleanup), then `switch_screen()` and `play()` — with the 4.2 MB dev DB this can exceed 100 ms on first touch.
- **Change:** introduce `utils/optimistic.py` with `apply_then_confirm(flag_setter, work_fn, rollback)` — flip the KV-bound visual state and show confirmation immediately, then schedule engine/DB work on a worker via `Clock.schedule_once` marshalling; revert only on error. Apply to favorite, play/add-to-playlist, search history, and the non-visual parts of `play_selected_track()`.
- **Acceptance:** with a mocked 2 s engine/DB delay, tap → icon/confirmation ≤ 100 ms in all four actions.

---

## 4. Code audit findings — encoded durations that must change

| Encoded value | Location | Target | Verdict |
|---|---|---|---|
| `SlideTransition(duration=0.22)`, horizontal on tabs | `views/main.kv:51`; `main.py:1015-1024, 1096-1102` | T5 | **Fails** — replace with `FadeTransition(0.18)` for tabs |
| Engine progress tick `0.1 s` (10 Hz) | `services/audio_engine.py:463` | T2 | **Fails** — raise toward 60 Hz / interpolate |
| `MDSlider.handle_anim_duration = 0.2 s` (default), `out_circ` | KivyMD default, `docs/api/kivymd_api.md:6306-6311` | T2 | **Fails** — set 0 / linear |
| Seek `is_seeking` hold `0.2 s` | `views/components.py:767` | T2 | Reduce to ~0.05 s |
| `MDBottomSheet` open `0.2 s` / close `0.2 s` | KivyMD `navigationdrawer.py:1288,1304` | T8 | Open OK; close → `0.15` |
| `MDNavigationItem.indicator_duration = 0.1 s` | `docs/api/kivymd_api.md:4096-4100` | T5 | OK / align to 0.15 |
| No haptic code / no `VIBRATE` permission | whole app, `buildozer.spec` | T1, T3 | **Missing** |
| No pop `Animation` on control icons | `player.kv`, `main.kv` | T1, T3 | **Missing** |
| No `on_text` autocomplete binding | `views/screens/search.kv:27-40` | T6 | **Missing** |
| No swipe action recognizers on rows | `views/components.py:355-386` | T7 | **Missing** |
| Track-options sheet never removed from `Window` | `main.py:2615` | T8 | Leak — fix alongside duration |

Cross-cutting notes from the audit:
- **Threading is already correct** — worker threads marshal UI updates with `Clock.schedule_once`; no background-thread graphics calls. Fixes must preserve this discipline.
- **A global `Animation._update` monkey-patch** exists at `main.py:95-154` (Python 3.12+ re-entrancy fix); all new animations use normal Kivy `Animation` and are compatible.
- **No latency assertions exist in tests** — the first deliverable of the verification phase is a harness that measures touch-to-paint, not just widget presence/direction.
- Lyrics recenter (0.35 s), tracker (0.25 s / 4 Hz), home refresh debounce (0.4 s) are outside the stated targets but are low-frequency and can be left as-is.

---

## 5. Verification plan (new interaction harness)

The existing `tests/benchmark_screen_performance.py` measures screen work, not interaction feedback. Add a companion **`tests/benchmark_ui_interactions.py`**:

1. Start `perf_counter` at the first line (same convention), boot headless, pump to `app_ready`.
2. Instrument app callbacks (favorite/play/pause/skip/toggles, sheet open/close, search focus/clear, swipe handlers) with count/total/max timing wrappers.
3. For each target, record:
   - `call_ms` — synchronous callback time to observable state change (icon/color/data),
   - `frames` — number of `Clock.tick()` pumps until the state settles,
   - `total_ms` — wall time until the visual state is ready,
   - the animation duration configured in code (introspected from `Animation`/transition objects).
4. Check encoded animation values statically (KV/Python) for each target: transition durations, `Animation(duration=...)`, ripple settings, debounce intervals.
5. Non-headless pass for bottom-nav crossfade and overlay slide: capture with `Clock` frame timing and confirm no horizontal `SlideTransition` on tab switches.
6. On-device-only items (haptic onset, native Android ripple, keyboard appearance, true 60/120 Hz drag) get a documented manual measurement protocol (high-speed screen recording at 120 fps / Android `adb shell dumpsys` input latency) — headless numbers cannot prove those.

**Acceptance rule:** each target's measured `call_ms` + configured animation duration must fall inside its stated window; any item above its ceiling gets a named owner fix from §3 before release.

---

## 6. Rollout order

**Phase 0 — single-property wins (minutes of work, biggest impact):**
`handle_anim_duration=0` / linear on the scrubber (T2), `FadeTransition(0.18)` for tab switches (T5), `closing_time=0.15` on both sheets (T8). Then re-measure those three and confirm.

**Phase 1 — optimistic state & feedback (low risk, high perceived speed):**
Optimistic favorite/DB writes + rollback helper (T3/T9), icon pop animations and Android haptics with `VIBRATE` permission (T1/T3), ripple audit (T4), defer inline DB work in `play_selected_track()`/`perform_search()` (T9).

**Phase 2 — missing interactions (medium effort):**
Live search autocomplete with debounce + keyboard focus config (T6), swipe-to-like/queue on track rows with directional arbitration (T7), sheet reuse/leak fix and prebuilt queue rows (T8).

**Phase 3 — frame-critical polish (needs device validation):**
Raise decoder progress cadence toward 60 Hz and verify the thumb tracks the finger within one frame at 60/120 Hz (T2).

After each phase: run the full 15-suite battery to protect the backend gains, then the new interaction harness and both screen benchmarks; keep results as additional timestamped/tagged records in `docs/performance/`.
