---
name: kivy-music-player-engineering
description: Expert engineering guide, debugging runbooks, architectural patterns, and testing protocols for Python Kivy and KivyMD music streaming and player applications. Use when implementing or diagnosing audio playback, synchronized lyrics, gesture arbitration, touch routing, dynamic YouTube ingestion, Material 3 theming, SQLite persistence, and headless test automation.
---

# Kivy Music Player Engineering Skill

This skill provides comprehensive architectural patterns, debugging runbooks, mathematical models, and verification protocols for developing and maintaining production-grade music applications built with Kivy and KivyMD.

---

## 1. Core Architectural Pillars

### 1.1 Strict Threading & Main-Loop Boundary
- **Rule**: Kivy graphics instructions (`Canvas`, `Color`, `Rectangle`, `Mesh`) and widget tree mutations (`add_widget`, `remove_widget`, `RecycleView.data`, property setters) **CANNOT** run on background threads (`threading.Thread`).
- **Fatal Error**: `Cannot create graphics instruction outside the main Kivy thread`.
- **Solution Pattern**:
  ```python
  def fetch_data_async(self, query):
      def _worker():
          # Heavy I/O, network requests, yt-dlp metadata extraction
          raw_data = fetch_youtube_metadata(query, extract_flat=True)
          track_objs = [TrackModel.from_dict(d) for d in raw_data]
          
          # Marshal UI update back to main thread
          def _update_ui(dt):
              self.active_tracks = track_objs
              self.root.ids.track_list.data = [{"track_obj": t, ...} for t in track_objs]
          Clock.schedule_once(_update_ui, 0)
      threading.Thread(target=_worker, daemon=True).start()
  ```

### 1.2 Two-Way Model Serialization (`TrackModel`)
- Any model object passed across threads, stored in SQLite, or cached in JSON payloads **MUST** implement symmetric bidirectional serialization:
  - `TrackModel.from_dict(data: dict) -> TrackModel`
  - `track_instance.to_dict() -> dict`
- Omitting `to_dict()` causes fatal `AttributeError: 'TrackModel' object has no attribute 'to_dict'` when saving cache payloads or transferring state across threads.

---

## 2. Touch Routing & Gesture Arbitration Runbook

### 2.1 Touch-Stealing by Hidden Overlays
- **Problem**: Setting `opacity: 0` or `height: 0` in Kivy does **NOT** prevent child widgets with explicit sizes from receiving and intercepting touch events! A hidden mini player or bottom nav will quietly steal clicks intended for items behind it.
- **Invariant**:
  ```kv
  # ALWAYS set disabled: True whenever a container is conditionally hidden:
  opacity: 1 if screen_manager.current in [...] else 0
  disabled: False if screen_manager.current in [...] else True
  ```

### 2.2 Passive Checkboxes & Trailing Widget Event Collisions
- **Problem**: In `MDListItem` with `MDListItemTrailingCheckbox`, clicking the checkbox or right edge causes the checkbox to intercept the touch without firing the item's `on_release`, creating a desynchronized UI state where the checkbox visually toggles but the application setting/database is never updated.
- **Solution**: Use `PassiveTrailingCheckbox` with `disabled: True`. The checkbox becomes purely visual, while the parent `MDListItem.on_release` handles the toggle and updates the underlying model/database atomically:
  ```python
  class PassiveTrailingCheckbox(MDListItemTrailingCheckbox):
      def __init__(self, **kwargs):
          kwargs.setdefault('disabled', True)
          super().__init__(**kwargs)
  ```

### 2.3 Nested Scrolling Arbitration (Horizontal in Vertical)
- **Problem**: Standard Kivy `ScrollView` absorbs `on_scroll_move` along both axes, even when `do_scroll_y: False`. This locks vertical parent scrolling whenever the user touches a horizontal row of chips or cards.
- **Solution**: Use `DirectionalHorizontalScrollMixin` (`DirectionalHorizontalScrollView`, `DirectionalHorizontalRecycleView`):
  - In `on_scroll_move`: if $|dy| > 1.1 \times |dx|$ and $|dy| > 8\text{dp}$, return `False` so the parent vertical scrollview can scroll smoothly.
  - In `on_scroll_start`: forward mouse wheel scrolling (`scrollup`, `scrolldown`) to the parent vertical scrollview.

---

## 3. Synced Lyrics Engine & Centered Auto-Scroll Math

### 3.1 Centered Viewport Math Formula
To keep the currently sung line vertically centered in the bottom sheet viewport:

$$\text{target\_y} = y_{\text{line}} - \frac{H_{\text{viewport}} - H_{\text{line}}}{2}$$

$$\text{scroll\_y} = \frac{\text{target\_y}}{H_{\text{content}} - H_{\text{viewport}}}$$

$$\text{clamped\_scroll\_y} = \max(0.0, \min(1.0, \text{scroll\_y}))$$

Where:
- $y_{\text{line}}$ is the Y-coordinate of the active lyric item relative to the content layout bottom.
- $H_{\text{viewport}}$ is the height of the `LyricsScrollView`.
- $H_{\text{content}}$ is the total height of the inner box layout.
- When $H_{\text{content}} \le H_{\text{viewport}}$, `scroll_y` evaluates to `1.0`.

### 3.2 User Drag Detection & 3-Second Resume Debounce
- During user drag gestures (`on_touch_down` with scroll movement), set `user_scrolling = True` and unschedule auto-scroll.
- On `on_touch_up`, schedule a 3.0s timer (`Clock.schedule_once(resume_auto_scroll, 3.0)`).
- If the user scrolls again within 3 seconds, cancel the timer.
- Once 3 seconds elapse with zero user touches, reset `user_scrolling = False` and smoothly re-center to the currently active lyric line.

### 3.3 Track Transition & Loop Reset
- When a new song starts or current song loops, immediately execute:
  1. `scroll_y = 1.0`
  2. `active_line_index = 0`
  3. `user_scrolling = False`
- **Layout Readiness Arbitration**: If line 0 is requested before Kivy has finalized child layouts ($H_{\text{box}} \le H_{\text{viewport}}$ or $y=0$), defer the calculation by 50ms (`Clock.schedule_once(recenter, 0.05)`) so coordinates are evaluated accurately.

### 3.4 Animation Teardown & CyClock Patch
- When closing the lyrics bottomsheet, ALWAYS call `Animation.stop_all(self, 'scroll_y')` to prevent in-flight animations from modifying detached widgets.
- Kivy's CyClock uses `WeakMethod` to inspect scheduled callbacks. Ensure monkey-patched animations implement both `_update` and `_safe_anim_update` with safe fallback:
  ```python
  def _anim_getattr(self, name):
      if name in ('_update', '_safe_anim_update', 'safe_update'):
          return self._update
      raise AttributeError(f"'Animation' object has no attribute '{name}'")
  Animation.__getattr__ = _anim_getattr
  ```

---

## 4. Cross-Platform Unicode Font Fallback

### 4.1 Missing Glyphs & "Tofu" Prevention
- Standard Roboto/Material font packs lack glyph coverage for Hindi, Devanagari, Japanese, Chinese, Arabic, and emojis, rendering square boxes (`[ ]`).
- **Dynamic Resolution Strategy**:
  1. **Windows**: Check `C:\Windows\Fonts\segoeui.ttf`, `Nirmala.ttf`, `arialuni.ttf`.
  2. **Android**: Check `/system/fonts/NotoSansDevanagari-Regular.ttf`, `/system/fonts/Roboto-Regular.ttf`, `/system/fonts/DroidSansFallback.ttf`.
  3. **Linux**: Check `/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc`, `/usr/share/fonts/truetype/noto/`.
- Register the resolved font globally:
  ```python
  LabelBase.register(DEFAULT_FONT, resolved_font_path)
  ```

---

## 5. Zero-Mock & Dynamic YouTube Ingestion

### 5.1 Anti-Mock Invariant
- **Rule**: Production screens must NEVER display hardcoded fake albums (*"Future Echoes"*, *"Midnight Drive"*) or static mock podcast episodes (*"The Sound Architecture"*, *"EP 142"*).
- **Rule**: If an artist or playlist has no local tracks, NEVER fill the screen with random unrelated tracks from the library.
- **Workflow**:
  1. Show legitimate local matching tracks if they exist.
  2. If none or sparse, set status to `"Fetching real tracks from YouTube..."`.
  3. Query YouTube asynchronously via `yt-dlp` (`ytsearch12:{artist} official songs audio` or `ytsearch10:{album} {artist}`).
  4. Cache results in SQLite for subsequent instant loads.
  5. Dynamically populate `EmbeddedRecycleView` and horizontal album cards.

### 5.2 Header Artwork Presentation
- Never place icons, cards, or badges directly on top of the album artwork.
- Header cards must display clean, prominent artwork (`180x180dp`, radius `16dp`, centered).
- Status icons (Verified artist, explicit badges) belong strictly in the metadata text column below the title.

---

## 6. Headless Verification Testing Standards

All test scripts MUST follow these headless execution rules:
1. `os.environ["KIVY_HEADLESS"] = "1"` MUST be set before any Kivy module import.
2. Resolve working directory immediately: `os.chdir(...)`.
3. Splash Screen Handling: Wait until `app._splash_completed` is `True` before asserting screen contents.
4. ScreenManager Transitions: Use `NoTransition()` during automated testing so assertions do not evaluate mid-flight during animated screen slides.
5. Strict Assertions: Tests must be designed to authentically fail if geometry, touch routing, or data models deviate from specifications.

### 6.1 Synthetic Event Simulation & FakeTouch Invariant
When dispatching synthetic touch events (`on_touch_down`, `on_touch_move`, `on_touch_up`) to test gesture arbitration:
- `touch.grab_list` Contract: Kivy's `ScrollView._do_touch_up` iterates through `touch.grab_list` and calls `x = x()`. Therefore, any mock `FakeTouch` MUST store a `weakref.ref(widget)` inside `grab_list`:
  ```python
  import weakref

  class FakeTouch:
      def __init__(self, x, y):
          self.pos = (x, y)
          self.x, self.y = x, y
          self.grab_list = []
          self.grab_current = None
          ...
      def grab(self, widget):
          self.grab_current = widget
          self.grab_list.append(weakref.ref(widget))
      def ungrab(self, widget):
          if self.grab_current == widget:
              self.grab_current = None
  ```
- Event Loop Pumping: Call `pump_events(app, cycles=5)` running `Clock.tick()` to allow Kivy layouts to compute bounding boxes without human frame rendering.

### 6.2 Interactive Widget Action-Binding Audit
- Every interactive button, chip, and floating action button across `.kv` files MUST have a bound event handler (`on_release`, `on_press`) or be explicitly marked `disabled: True`.
- Run `tests/test_interactive_widgets_audit.py` to statically verify all `.kv` files before concluding UI work.

### 6.3 Permanent 10-Suite Master Test Battery
The project maintains a 10-suite test suite in `KivyMusicApp/tests/run_all_tests.py`:
1. `test_lyrics_engine_and_math.py`: LRC timestamp parsing, viewport centering math, user drag debounce.
2. `test_player_queue_and_offline.py`: Queue sync, track transition, duration formatting.
3. `test_interactive_widgets_audit.py`: 100% action binding verification across all `.kv` files.
4. `test_settings_and_persistence.py`: Light theme default, `PassiveTrailingCheckbox`, SQLite roundtrip.
5. `test_artwork_and_ui_geometry.py`: Non-zero bar heights, zero-overlap, hidden overlay `disabled: True`.
6. `test_artist_and_album_dynamic.py`: Dynamic discography, zero mock albums, dynamic card generation.
7. `test_podcasts_and_trending.py`: `TrackModel` serialization, spotlight card bindings.
8. `test_backend_integration.py`: SQLite track caching, playlists, favorites, search history, `AudioEngine`.
9. `test_battery_fixes.py`: Multilingual Unicode textures, duration accuracy, artwork sync.
10. `test_comprehensive_audit.py`: 13-suite end-to-end integration (18 screens zero overlap, back stacks, dialogs, sheets, carousel Option A, button symmetry, directional gestures).
