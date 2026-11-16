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
- **Maintain MVC/Modular Structure:** Keep business logic, UI definitions (Views), and Controllers separate. Do not pollute UI widgets with complex background logic.
- **Asynchronous Execution:** Heavy operations (like downloading videos or fetching metadata via `yt-dlp`) must never block the main Kivy UI thread. Always use asynchronous tasks, threading, or Kivy's `Clock`.

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

## 11. Automated Headless Verification Battery
- After any UI change, execute an automated verification script in headless mode (`KIVY_HEADLESS=1`).
- The test suite must assert:
  1. Zero exceptions during startup and screen navigation across all screens.
  2. Bounding-box non-overlap across all stacked bars and screens.
  3. Correct touch routing (sheets open on click, hidden overlays do not steal touches).
  4. Symmetrical alignment (difference $< 1.0\text{dp}$ on centered rows).
  5. Directional scrolling delegation (vertical swipe over horizontal container scrolls parent).
  6. Screenshot captures saved for visual regression review.

## 12. Zero-Mock & Dynamic Live Streaming Invariant
- **No Hardcoded Mock Content:** Production screens (Artist, Album, Podcasts, Browse) must never display hardcoded dummy cards, fake album titles (*"Future Echoes"*, *"Midnight Drive"*), or fake podcast episodes (*"The Sound Architecture"*).
- **No Unrelated Fallback Data:** If an artist or category has no local tracks, never grab arbitrary songs from other artists. Show an authentic loading or empty state and immediately query YouTube asynchronously (`yt-dlp`).
- **Live YouTube Integration:** Always extract real metadata (video ID, title, uploader/artist, duration, thumbnail) via `fetch_youtube_metadata(..., extract_flat=True)` and stream real audio.

## 13. Main-Thread UI Dispatch & Thread-Safety Invariant
- **Zero Graphics Calls on Background Threads:** Never modify UI widgets, properties, `RecycleView.data`, or start animations from background threads. Doing so raises fatal OpenGL/SDL2 exceptions (`Cannot create graphics instruction outside the main Kivy thread`).
- **Mandatory `Clock.schedule_once` Marshalling:** Every thread completion must schedule UI mutations back on the main thread loop: `Clock.schedule_once(lambda dt: update_ui(), 0)`.
- **Bidirectional Serialization:** Any data model (`TrackModel`) passed across threads or cached in SQLite/JSON must implement both `from_dict()` and `to_dict()`.

## 14. Settings Persistence & Trailing Toggle Invariant
- **Instant SQLite Persistence:** Every setting toggle (theme style, Wi-Fi only, background animation, SponsorBlock, EQ, audio quality) must immediately persist to disk via `set_setting(...)` and apply to the active theme/engine.
- **Default Theme is Light:** The default theme style must strictly be `Light` unless the user explicitly toggles Dark Mode.
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
- Audio durations for offline songs must be accurately read from file headers (`mutagen` or `ffprobe`) rather than defaulting to arbitrary 5:00 fallbacks.

## 19. ScreenManager Lifecycle & Transition Arbitration
- In headless test suites, splash screen completion (`_splash_completed`) and screen slide transitions take non-zero time. Always use `NoTransition()` or schedule assertions after frame completion.
- The splash screen fadeout callback (`_on_fade_complete`) must only switch to `"home"` if the current screen is still `"splash"`, preventing it from overriding user navigations.
