# UI Visual, Geometry & Gesture Audit Rules

This rule defines mandatory quality gates for all user interface changes in Kivy and KivyMD across this workspace.

## 1. Zero Overlap & Geometry Integrity
- **Stacked Heights:** Top-level navigation elements (`MDNavigationBar`, `mini_player`, `MDTopAppBar`) must declare explicit heights in density-independent pixels (e.g. `dp(80)` or `dp(72)`). Do not rely on `minimum_height` for bars whose children have `size_hint_y: 1.0`.
- **Vertical Hierarchy:** Verify that the screen manager and docked bottom bars do not overlap in window coordinates:
  $$\text{bottom\_nav.y} + \text{bottom\_nav.height} \le \text{mini\_player.y}$$
  $$\text{mini\_player.y} + \text{mini\_player.height} \le \text{screen\_manager.y}$$
- **Bottom Content Padding:** Scrollable views must have sufficient bottom padding (minimum `32dp`, or `88dp` if an `MDFabButton` is present) so content is never obscured by the mini player or navigation bar.

## 2. Touch Routing & Stealth Interception Prevention
- **Disabled State for Hidden Overlays:** In Kivy, setting `opacity: 0` or `height: 0` on a widget does **not** stop its children from receiving touch events. Any conditionally visible container placed above other content must be explicitly disabled when not in use:
  ```kv
  disabled: False if screen_manager.current in ["home", "search", "library"] else True
  ```
- **Action Completeness:** All interactive components (`MDButton`, `MDIconButton`, `MDFabButton`, `MDListItem`, `MDChip`, `MDSlider`) must have functional event handlers wired to controllers, modal dialogs, or bottom sheets.

## 3. Centering, Sizing & Spacing Symmetry
- **Horizontal Box Centering:** Always use `adaptive_size: True` (which sets both `adaptive_width` and `adaptive_height` to `True`) with `pos_hint: {"center_x": .5}` when centering a row of fixed-size buttons (e.g. player controls). Using `adaptive_height: True` alone leaves `size_hint_x: 1.0`, anchoring buttons to the left edge and introducing severe horizontal asymmetry.
- **Scroll Container Padding:** Horizontal chip bars must have `height: "48dp"`, `bar_width: "2dp"`, and box padding `padding: ["8dp", "8dp", "8dp", "8dp"]` to ensure chips do not collide with scroll indicators.
- **Single-Slide Viewports:** Carousels (`Carousel`) must contain elevated cards with fixed dimensions and centered positioning (`pos_hint: {"center_x": .5, "center_y": .5}`) to prevent adjacent cards from peeking into view.

## 4. Directional Gesture Arbitration (Nested Scrolling)
- Never use standard Kivy `ScrollView` or `RecycleView` for horizontal carousels placed inside a vertical `MDScrollView`. They swallow vertical gestures and block parent scrolling.
- Always use `DirectionalHorizontalScrollView` or `DirectionalHorizontalRecycleView` (inheriting from `DirectionalHorizontalScrollMixin`):
  - In `on_scroll_start`: forward mouse wheel scrolling (`scrollup`, `scrolldown`) to the parent vertical scrollview.
  - In `on_scroll_move`: if $\lvert dy \rvert > 1.1 \times \lvert dx \rvert$ and movement exceeds touch slop ($8\text{dp}$), return `False` to delegate the vertical gesture to the parent scrollview.

## 5. Main-Thread Performance & Dynamic Color Caching
- **Theme Event Debouncing:** Dynamic color extraction from album art (`theme_cls.path_to_wallpaper`) is synchronous. Always debounce updates via `Clock.schedule_once` and cache the active image path to avoid redundant re-quantization.
- **Startup Async Sequencing:** Trigger dynamic data ingestion (`load_data_async`) promptly on startup ($0.05\text{s}$) rather than on a delayed timer to eliminate mid-interaction stutter.

## 6. Verification Checklist Before Concluding Tasks
Every UI change must be evaluated transparently across layout constraints and the 4-tier test framework (`GEMINI.md` §11 & §20):
1. **Viewport Constraint Resilience:** Design around the `360x640dp` reference viewport using constraint-based, scrollable containers that tolerate varied Android aspect ratios, display cutouts, system bars/insets, and accessibility font scaling.
2. **Automated Headless Battery (`KIVY_HEADLESS=1`):** Verify bounding-box geometry, symmetrical margins (`< 1.0dp`), touch routing (clicking targets without hidden overlay interception), directional scrolling delegation, and visual screenshot captures.
3. **Explicit Honesty Scope:** State clearly that headless UI/geometry checks do **not** verify Android GPU frame pacing, font rendering under OEM skins, or real device audio/background behavior — record real device checks separately when tested via `adb` / Perfetto.
