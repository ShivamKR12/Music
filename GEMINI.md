# Project Rules & Guidelines

These rules must be strictly followed when working on this workspace:

## 1. API Documentation First
**Always read the API markdown files** before making any changes related to the core libraries. Do not guess API methods or configuration options. Use the specific tool to read these files when needed:
- `docs/api/kivy_api.md` (for Kivy UI and Core API)
- `docs/api/kivymd_api.md` (for KivyMD Material Design components)
- `docs/api/yt-dlp_api.md` (for yt-dlp downloading and extraction options)

## 2. Assess Overall Impact
**Check and read all relevant code** before modifying any existing file. 
- You must understand the overall architecture and how your proposed changes will impact other interconnected files (e.g., how modifying a model affects the controller and the views).
- Use code search and file reading tools to trace where functions and classes are being utilized across the app before editing them.

## 3. Architecture & Structure
- **Maintain MVC/Modular Structure & Single-Responsibility Boundaries:** Keep UI definitions (Views), state/controllers, repositories, database workers, and media pipelines separate. Do **not** keep expanding monoliths (`main.py` or a god-object `AudioEngine`). Gradually decompose `main.py` into focused coordinators (`AppBootstrap`, `ServiceContainer`, `NavigationCoordinator`, `ApplicationLifecycle`, `AppState`) and decompose audio into `PlaybackCoordinator`, `DecoderManager`, `BufferManager`, and `DSPPipeline`, sitting behind a `MusicRepository` layer above `MusicProviderRouter`.
- **Asynchronous Execution:** Heavy operations (downloading media, stream resolution via `MusicProviderRouter`/`yt-dlp`, image quantization, filesystem scans, and database writes) must never execute on the main Kivy UI thread. Always use background workers or a dedicated asynchronous executor, and marshal UI updates via `Clock.schedule_once`.

## 4. Coding Standards
- **Follow PEP 8:** Write clean, readable, and consistent Python code.
- **Preserve Documentation:** Maintain all existing comments and docstrings. If a function is updated, update its docstring to reflect the new behavior.
- **Robust Error Handling:** Always anticipate and catch potential errors (network failures, invalid URLs, missing files) to prevent the app from crashing.

## 5. Safe Modifications
- Use scratch scripts to safely test logic (e.g., scraping, parsing, or library behavior) before modifying the actual application files.
- Keep file modifications atomic and heavily focused on the user's explicit request.

## 6. Mandatory Visual, Layout & Geometry Verification
Whenever any UI modification is made (in `.kv` or Python UI components), you MUST verify that no visual glitches, clipping, or overlaps exist before concluding the task:
- **Zero-Overlap Stacked Heights:** Never rely on `minimum_height` for top-level bars (`MDNavigationBar`, `mini_player`, `MDTopAppBar`). In KivyMD 2.0, `minimum_height` evaluates to 0 when child navigation items have `size_hint_y: 1.0`, collapsing the container and causing overlapping widgets at $y=0$. Set explicit heights (e.g. `dp(80)`, `dp(72)`) and verify that sibling bounding boxes do not overlap: $(y_1 + h_1 \le y_2)$.
- **Bottom Navigation Padding:** All scrollable content (`MDScrollView`, `RecycleView`) must have bottom padding (minimum `32dp`, or `88dp` if an `MDFabButton` or persistent bar is present) so the last element can be fully scrolled into view without clipping.
- **Scroll Container Spacing:** Ensure horizontal chip bars or card strips (`MDScrollView`, `RecycleView`) have explicit heights (e.g. `48dp` for chips) and internal box padding (`padding: ["8dp", "8dp", "8dp", "8dp"]`) so elements never touch scroll indicators or screen borders.
- **Carousel & Pager Containment:** Carousels (`Carousel`, `MDCarousel`) must have slide dimensions cleanly constrained (`size_hint: (1, 1)` with centered, fixed-dimension cards) to prevent adjacent slides from peeking or clipping into the viewport.

## 7. Touch-Stealing Prevention & Visibility Invariants
- **Disabled State on Hidden Containers:** In Kivy, setting `opacity: 0` or `height: 0` on a parent does NOT prevent children with explicit sizes from intercepting touch events! Whenever a floating, pinned, or bottom overlay (such as `mini_player` or `bottom_nav`) is conditionally hidden, you MUST set `disabled: True` (e.g., `disabled: False if screen_manager.current in [...] else True`). Kivy completely halts touch dispatch for disabled widgets and all their descendants.
- **Interactive Control Completeness:** Every interactive widget (buttons, list items, sliders, chips) must have a concrete, bound event handler (`on_release`, `on_touch_down`, `on_value`) wired to controller methods, modal dialogs, or bottom sheets. Never leave interactive widgets inert.

## 8. Alignment, Sizing & Centering Standards
- **Box Layout Centering (`adaptive_size`):** For centered horizontal button rows or action bars, always use `adaptive_size: True` (which sets both `adaptive_width` and `adaptive_height` to `True`) with `pos_hint: {"center_x": .5}`. Never use `adaptive_height: True` alone, as `size_hint_x: 1.0` defaults to expanding the full width and anchors child buttons to the left edge ($x=0$), causing severe spacing asymmetry.
- **Touch Target Sizing:** All touchable elements must satisfy the minimum $48 \times 48\text{dp}$ touch target requirement.

## 9. Directional Gesture Arbitration Invariant
- **Nested Scrolling Rule:** Standard Kivy `ScrollView` and `RecycleView` absorb `on_scroll_move` and return `True` even for un-scrolled axes (`do_scroll_y: False`), locking parent vertical scrollviews.
- **Mandatory Custom Containers:** Whenever placing a horizontal scroll container inside a vertical scrollview, you MUST use `DirectionalHorizontalScrollView` or `DirectionalHorizontalRecycleView` (powered by `DirectionalHorizontalScrollMixin`):
  - In `on_scroll_start`: forward mouse wheel scrolling (`scrollup`, `scrolldown`) to the parent vertical scrollview.
  - In `on_scroll_move`: if $\lvert dy \rvert > 1.1 \times \lvert dx \rvert$ and movement exceeds touch slop ($8\text{dp}$), return `False` so the parent vertical scrollview can scroll vertically.

## 10. Performance & Main-Thread Preservation
- **Debounced & Cached Dynamic Theming:** Material You wallpaper/album art quantization (`theme_cls.path_to_wallpaper`) is synchronous and heavy. Always debounce theme updates via `Clock.schedule_once`, cache the active image path, and avoid triggering theme updates multiple times on screen switches.
- **Startup Async Sequencing:** Schedule background data population (`load_data_async`) promptly on startup ($0.05\text{s}$) rather than on a delayed timer (e.g. $1.0\text{s}$) to avoid freezing the UI while the user is actively navigating.

## 11. Four-Tier Verification Discipline (Never Equate Headless Mocks with Production Proof)
Always separate and report verification strictly across these **four testing categories**, clearly stating scope, mocks used, and limitations:
1. **Unit Tests:** Verify pure algorithms, recommendation/novelty math (with boundary tests), LRC parsers, queue state transitions, and serialization (`to_dict`/`from_dict`).
2. **Integration Tests (Headless / Mocked):** After any UI or controller change, run the headless verification battery (`KIVY_HEADLESS=1`, `tests/run_all_tests.py`), asserting:
   - Zero exceptions during startup and screen navigation across all screens (`NoTransition()`).
   - Bounding-box non-overlap across stacked bars and screens, symmetrical alignment (`< 1.0dp`), touch routing (sheets open, hidden overlays disabled), directional scroll delegation, and screenshot captures.
   - **Explicit limitation:** Headless/mock tests **never** establish real Opus/AAC/MP3 audio playback reliability, DSP filter execution, hardware decoder behavior, packet-loss buffering, GPU frame pacing, memory leaks over long sessions, Android background lifecycle, or live external provider resilience.
3. **Device Tests (Real Windows Audio & Real Android APK via `adb`):** Verify actual playback on physical/emulated hardware, runtime permissions, Android `ForegroundService` / `MediaSession` lock-screen controls, headphone/Bluetooth route changes, incoming call audio focus, and real network conditions.
4. **Performance Telemetry:** Measure and log real runtime metrics rather than guessing responsiveness:
   - **Cold startup** (time to first usable screen), **Time to first audio** (tap play -> audible output), **Buffering stalls** (count & total stall duration), **Frame pacing** (missed frames / percentiles via Android Studio / Perfetto), **Long-session RAM usage**, **DSP CPU load**, **Network throughput/retransmissions**, and **Provider crash/failure rates**.

## 12. Zero-Mock & Dynamic Live Streaming Invariant
- **No Hardcoded Mock Content:** Production screens (Artist, Album, Podcasts, Browse) must never display hardcoded dummy cards, fake album titles (*"Future Echoes"*, *"Midnight Drive"*), or fake podcast episodes (*"The Sound Architecture"*).
- **No Unrelated Fallback Data:** If an artist or category has no local tracks, never grab arbitrary songs from other artists. Show an authentic loading or empty state and immediately query YouTube asynchronously (`yt-dlp`).
- **Live YouTube Integration:** Always extract real metadata (video ID, title, uploader/artist, duration, thumbnail) via `fetch_youtube_metadata(..., extract_flat=True)` and stream real audio.

## 13. Main-Thread UI Dispatch & Thread-Safety Invariant
- **Zero Graphics Calls on Background Threads:** Never modify UI widgets, properties, `RecycleView.data`, or start animations from background threads. Doing so raises fatal OpenGL/SDL2 exceptions (`Cannot create graphics instruction outside the main Kivy thread`).
- **Mandatory `Clock.schedule_once` Marshalling:** Every thread completion must schedule UI mutations back on the main thread loop: `Clock.schedule_once(lambda dt: update_ui(), 0)`.
- **Bidirectional Serialization:** Any data model (`TrackModel`) passed across threads or cached in SQLite/JSON must implement both `from_dict()` and `to_dict()`.

## 14. Settings Persistence, Database Worker Concurrency & Trailing Toggle Invariant
- **Non-Blocking SQLite Persistence (Dedicated Database Worker):** Do **not** execute synchronous SQLite writes (`set_setting`, `add_track`, `mark_track_played`) under a blocking global lock on the Kivy UI thread. Settings toggles must update observable app state optimistically on the UI thread and persist asynchronously through a dedicated single-writer **Database Worker** (using `PRAGMA journal_mode=WAL`, `PRAGMA foreign_keys=ON`, `busy_timeout`, explicit transaction boundaries, and atomic schema migrations) so background scans never freeze UI clicks.
- **Unicode-Safe Sanitization:** Text sanitization for SQLite/display must preserve Unicode combining diacritics/matras (Devanagari, Gurmukhi, etc.) rather than stripping `\p{M}` characters.
- **Default Theme is Light:** The default theme style must strictly be `Light` unless the user explicitly toggles Dark Mode (and default fallbacks in `main.py` and `database.py` must agree).
- **Passive Trailing Checkboxes:** In list items with toggle checkboxes, trailing widgets must use `disabled: True` (`PassiveTrailingCheckbox`) so touches dispatch cleanly to the parent `MDListItem.on_release` without event hijacking.

## 15. Synced Lyrics Engine & Centered Viewport Standards
- **Vertical Centering Math:** The currently active lyric line must always be centered in the viewport: $y_{\text{target}} = y_{\text{line}} - \frac{H_{\text{viewport}} - H_{\text{line}}}{2}$.
- **User Scroll Detection & Debounce:** Any user drag gesture on lyrics must pause auto-scroll (`user_scrolling = True`). A 3.0-second debounced timer must verify the user has finished interacting before resuming auto-scroll.
- **Track Transition Reset:** When changing songs or looping, immediately reset `scroll_y = 1.0`, line index to 0, and clear `user_scrolling = False`.
- **Teardown Animation Safety:** On bottom sheet close, always cancel in-flight scroll animations (`Animation.stop_all(self, 'scroll_y')`) to prevent callbacks from firing on dismantled widgets.

## 16. Cross-Platform Unicode Font Fallback
- **Missing Glyph Prevention:** Standard Roboto lacks glyphs for international scripts (Hindi, Devanagari, Japanese, Chinese, Cyrillic, emoji), causing "tofu" squares.
- **Dynamic System Resolution:** Inspect host font directories (Windows `segoeui.ttf` / `Nirmala.ttf`, Android `/system/fonts/NotoSansDevanagari-Regular.ttf` / `Roboto-Regular.ttf`, Linux `/usr/share/fonts/`) and register the resolved font in `LabelBase.register(DEFAULT_FONT, ...)` on startup.

## 17. Unobstructed Header Artwork Invariant
- In playlist, album, and favorites headers, never overlay icons, badges, or circular cards directly in the middle of album artwork.
- Header artwork must be prominent, centered, and unobstructed (`180x180dp`, radius `16dp`). Status indicators (like Verified Artist) belong in the metadata subtitle section below the title.

## 18. Queue Synchronization & Offline Audio Precision
- The "Up Next" queue bottomsheet must strictly reflect the active playback context (`player_controller.queue`). When playing offline songs or custom playlists, call `set_custom_queue(...)` so queue reflects all active tracks.
- Audio durations for offline songs must be accurately read from file headers (`mutagen` or `ffprobe` / binary header parser) rather than defaulting to arbitrary 5:00 fallbacks.

## 19. ScreenManager Lifecycle & Transition Arbitration
- In headless test suites, splash screen completion (`_splash_completed`) and screen slide transitions take non-zero time. Always use `NoTransition()` or schedule assertions after frame completion.
- The splash screen fadeout callback (`_on_fade_complete`) must only switch to `"home"` if the current screen is still `"splash"`, preventing it from overriding user navigations.

## 20. Ground-Truth Reporting Contract: Designed vs. Implemented vs. Verified
- **Never Blur Status States:** In all docs, architecture reviews, and responses to the user, strictly separate:
  1. **Designed:** What the architecture intends or proposes.
  2. **Implemented:** Only what genuinely exists in inspected source code (exact files, symbols, hardcoded shortcuts, and incomplete paths). Never claim a module implements behavior (e.g. equal-power crossfade, PCM EQ convolution, WebSockets, or ML vector scoring) without reading the file to prove it exists.
  3. **Verified:** Only what has actually been proven by tests covering that exact code path, tagged by tier (**Unit**, **Integration/Headless**, **Device**, **Performance**). Never imply "guaranteed uninterrupted streaming" or "100% app reliability" from unit/headless passes alone.
- **Spotify / Multi-Source Honesty:** Always distinguish explicitly between *Spotify public metadata/playlist lookup* and *actual audio playback source* (JioSaavn or YouTube). Avoid claiming Spotify audio streaming, and avoid brittle scraping where official APIs/integrations apply.
- **Viewport Adaptation Beyond 360×640:** Treat 360×640 dp as the **reference design viewport**, while ensuring layouts are constraint-based, scrollable, and tolerant of varying aspect ratios, display cutouts, Android system bars/insets, and accessibility font scaling.

## 21. Audio Pipeline, Progressive Buffering & DSP Standards
- **Explicit PCM Processing Path:** Real-time EQ, headphone AutoEq convolution, and crossfade headroom require a verified PCM audio path (`Compressed Audio -> Decoder -> PCM Samples -> DSP Processing -> Volume / Mixing -> Audio Output`). Never assume Kivy `SoundLoader` (`SoundAndroidPlayer` / `SoundFFPy`) supports FFmpeg filter graphs without empirical runtime verification (e.g., `ffpyplayer.player.MediaPlayer` has no `set_filter`, and Android builds exclude `ffpyplayer`).
- **True Streaming vs Partial `.part` Hacks:** Progressive buffering must be treated as an independent subsystem (`BufferManager`) rather than opening a growing file mid-download alongside a destructive postprocessor. Track three distinct metrics:
  1. **Download Progress:** Bytes retrieved / total bytes (`Content-Length` + HTTP `Range` verification).
  2. **Playable Buffer:** Actual decodable seconds buffered.
  3. **Buffer Safety:** Seconds of playable audio strictly ahead of the current playhead.
- **Completion Semantics:** Never mark `is_downloaded = True` or persist final `local_path` to SQLite until the full audio stream and container finalization/remux succeed.
- **Equal-Power Crossfade Testing:** Any equal-power (`cos`/`sin`) crossfade must manage output headroom and be tested with real overlapping audio frames to catch correlated-signal clipping.

## 22. External Provider Resilience & Security Boundaries
- **No "Guaranteed" YouTube Extraction:** Never assume `player_client` or `formats: ['missing_pot']` bypasses BotGuard / PO-Token requirements permanently. Design extraction as: `Extractor -> Client Selection -> PO-Token Provider Hook -> Format Validation -> Signed Stream URL -> Playback Engine`, backed by URL expiration detection, stream re-resolution, exponential backoff retries, error classification (never silence warnings/errors in `SilentLogger`), and fail-safe queue protection so failed extracts never crash playback.
- **Security & Redaction:** Securely store any external API credentials/tokens, enforce WebSocket/room host authorization and payload validation, redact signed stream URLs and tokens from all logs, and isolate desktop-only IPC (Discord RPC) from Android builds.

## 23. Android Runtime Lifecycle & Scoped Storage Compliance
- **Native Media Playback Lifecycle:** Declaring manifest permissions (`FOREGROUND_SERVICE`, `FOREGROUND_SERVICE_MEDIA_PLAYBACK`, `WAKE_LOCK`) is insufficient without native Android lifecycle integration: foreground media playback service, notification + lock-screen transport controls, `MediaSession`, audio focus negotiation, noisy/headphone disconnect pausing, phone-call interruptions, Bluetooth routing changes, and process-recreation state restoration.
- **Modern Android Storage (`API 33+`):** Declare and check `READ_MEDIA_AUDIO` (not just legacy external-storage permissions) and prefer `MediaStore` queries over raw recursive `os.walk` traversal where scoped storage applies.

## 24. Recommendation Contracts & Mathematical Verification
- **Explicit Data Contracts:** Clearly define where track features (`popularity`, `genre`, or any future `energy`/`valence`/`tempo`) and listener features (`play history`, `artist affinity`, `skip behavior`, `listening time`) actually originate (multi-timestamp observations for trending rather than single view counts).
- **Mandatory Math Boundary Tests:** Any scoring or ranking formula must have explicit boundary unit tests matching intended directionality (e.g., recency novelty must start low at $\Delta t = 0$ and increase as time elapsed since last play grows: $H_i = 1 - \exp(-\Delta t/\tau)$ or subtracting a decay penalty, never adding $\exp(-\Delta t/\tau)$ positively).

## 25. Feature Scope & Priority Execution Roadmap
Resist expanding parallel 80%-complete features. Prioritize stabilizing the core systems in strict order:
1. **Priority 1:** Validate the real audio & PCM DSP pipeline (playback reliability first).
2. **Priority 2:** Redesign progressive buffering (`BufferManager` state machine + true buffer metrics + real Opus/M4A/MP3 tests).
3. **Priority 3:** Harden YouTube extraction (PO-token hook, retries, URL refresh, explicit error taxonomy).
4. **Priority 4:** Establish clean recommendation data contracts & tested ranking math.
5. **Priority 5:** Move SQLite to a dedicated non-blocking **Database Worker** (WAL mode, FK enforcement, Unicode-safe sanitization).
6. **Priority 6:** Implement real Android native media lifecycle (`ForegroundService`, `MediaSession`, audio focus, `MediaStore`).
7. **Priority 7:** Introduce real Device-level & Performance Telemetry testing (`adb`, Perfetto/profiler metrics).
8. **Priority 8:** Decompose `main.py` incrementally into clean coordinators & repository boundaries.
