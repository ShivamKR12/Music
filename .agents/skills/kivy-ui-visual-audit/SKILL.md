---
name: kivy-ui-visual-audit
description: Comprehensive audit procedures, debugging runbooks, and automated test patterns for Kivy and KivyMD UI layouts. Use whenever modifying or reviewing UI layouts, fixing visual glitches, eliminating widget overlaps, resolving touch-stealing or unresponsive clicks, fixing nested scrolling conflicts, centering controls, or verifying Material Design 3 compliance.
---

# Kivy & KivyMD UI Visual Audit & Debugging Runbook

A production-grade guide to detecting, diagnosing, and resolving visual defects, layout geometry bugs, touch interception issues, and nested scrolling conflicts in Kivy and KivyMD (Material Design 3) applications.

---

## The 8 Critical Pitfalls of Kivy/KivyMD UIs

### 1. The Zero-Height / Overlapping Top-Level Bars Trap
* **The Symptom:** Navigation bars (`MDNavigationBar`), mini players, and screen content render directly on top of each other at the bottom of the window ($y = 0$).
* **The Root Cause:** In KivyMD 2.0, `MDNavigationBar.minimum_height` computes to `0` when child `MDNavigationItem` widgets have `size_hint_y: 1.0` (relative size rather than fixed pixels). Binding `height: self.minimum_height` collapses the bar to `0px`, causing it to overlap other widgets placed at the bottom.
* **The Fix:** Always specify explicit density-independent pixel heights on persistent bars:
  ```kv
  MDNavigationBar:
      id: bottom_nav
      size_hint_y: None
      height: dp(80)
  ```
* **Verification Invariant:**
  $$\text{bottom\_nav.y} + \text{bottom\_nav.height} \le \text{mini\_player.y}$$
  $$\text{mini\_player.y} + \text{mini\_player.height} \le \text{screen\_manager.y}$$

---

### 2. Touch-Stealing by Invisible Overlays
* **The Symptom:** Buttons near the bottom of a screen (e.g. "UP NEXT" queue pill on the Player screen) are completely unresponsive to clicks or touches.
* **The Root Cause:** In Kivy, setting `opacity: 0` or `height: 0` on a parent layout **does NOT stop its children from receiving touch events**. If `mini_player` is placed after `screen_manager` in the root layout, its children remain active at $(8, 8 \dots 352, 72)$, intercepting touches before they can reach the underlying screen.
* **The Fix:** Always set `disabled: True` on conditionally visible containers:
  ```kv
  MDBoxLayout:
      id: mini_player
      size_hint_y: None
      height: dp(72) if screen_manager.current in ["home", "search", "library"] else dp(0)
      opacity: 1 if screen_manager.current in ["home", "search", "library"] else 0
      disabled: False if screen_manager.current in ["home", "search", "library"] else True
  ```

---

### 3. Box Layout Centering Asymmetry (`adaptive_height` vs `adaptive_size`)
* **The Symptom:** Horizontal action buttons (e.g., Shuffle, Prev, Play, Next, Repeat) appear noticeably shifted to the left, leaving significantly more empty space on the right of the repeat button than to the left of shuffle.
* **The Root Cause:** `adaptive_height: True` sets `size_hint_y: None`, but **leaves `size_hint_x: 1.0` active**. In a horizontal `MDBoxLayout`, fixed-size child buttons pack starting at $x=0$. The container expands to 100% of the screen width, shoving all leftover margins to the far right.
* **The Fix:** Use `adaptive_size: True` (which sets both `adaptive_width: True` and `adaptive_height: True`) together with `pos_hint: {"center_x": .5}`:
  ```kv
  MDBoxLayout:
      adaptive_size: True
      spacing: "16dp"
      pos_hint: {"center_x": .5}
      # Buttons pack tightly and the entire container centers symmetrically
  ```
* **Verification Invariant:**
  $$\lvert (W - \text{repeat.right}) - \text{shuffle.x} \rvert < 1.0\text{dp}$$

---

### 4. Nested Directional Scroll Conflict (Horizontal Carousels inside Vertical ScrollViews)
* **The Symptom:** Swiping vertically with a finger or dragging a cursor over horizontal chip bars, Quick Picks, or carousel rows does not scroll the parent page. Over 75% of screens like Home feel frozen or unresponsive.
* **The Root Cause:** In Kivy, `ScrollView` and `RecycleView` return `True` from `on_scroll_move` unconditionally whenever a touch falls within their bounding box—even when `do_scroll_y: False` and the gesture is purely vertical. The parent vertical `ScrollView` sees `True` and aborts vertical scrolling.
* **The Fix:** Implement `DirectionalHorizontalScrollMixin` with directional gesture arbitration:
  ```python
  class DirectionalHorizontalScrollMixin:
      def __init__(self, **kwargs):
          kwargs.setdefault('do_scroll_x', True)
          kwargs.setdefault('do_scroll_y', False)
          super().__init__(**kwargs)

      def on_scroll_start(self, touch, check_children=True):
          if getattr(touch, 'button', None) in ('scrollup', 'scrolldown'):
              return False  # Forward vertical mouse wheel to parent vertical scrollview
          touch.ud[f'{id(self)}_start_pos'] = (touch.x, touch.y)
          touch.ud[f'{id(self)}_locked'] = None
          super().on_scroll_start(touch, check_children=check_children)
          return False  # Allow parent vertical scrollview to initialize its effect_y

      def on_scroll_move(self, touch):
          start_pos = touch.ud.get(f'{id(self)}_start_pos')
          locked = touch.ud.get(f'{id(self)}_locked')

          if start_pos and locked is None:
              dx = abs(touch.x - start_pos[0])
              dy = abs(touch.y - start_pos[1])
              slop = dp(8)
              if dx > slop or dy > slop:
                  if dy > dx * 1.1:
                      touch.ud[f'{id(self)}_locked'] = 'v'
                  else:
                      touch.ud[f'{id(self)}_locked'] = 'h'

          if touch.ud.get(f'{id(self)}_locked') == 'v':
              return False  # Yield to parent vertical scrollview

          return super().on_scroll_move(touch)
  ```

---

### 5. Carousel Adjacent Slide Peeking & Coordinate Clipping
* **The Symptom:** In the Now Playing screen, the album art of the next track on the right clips into the current track's view by 10-20dp.
* **The Root Cause:** `MDCarousel` in `uncontained` mode peeks adjacent slides into the viewport by default.
* **The Fix:** Use native Kivy `Carousel` acting as an Android `HorizontalPager`. Place individual slides inside centered, elevated `MDCard`s with fixed dimensions (`size: dp(280), dp(280)` and `pos_hint: {"center_x": .5, "center_y": .5}`):
  ```kv
  Carousel:
      id: album_carousel
      size_hint: 1, 1
      pos_hint: {"center_x": .5}
  ```

---

### 6. Scrollbar Collision & Edge Padding
* **The Symptom:** Filter chips or list items touch the bottom scroll indicator or the edges of the window.
* **The Root Cause:** Scrollable containers without explicit height, bar width, or inner box padding.
* **The Fix:**
  - Standard chip bar container:
    ```kv
    DirectionalHorizontalScrollView:
        size_hint_y: None
        height: "48dp"
        bar_width: "2dp"
        MDBoxLayout:
            adaptive_size: True
            height: "48dp"
            padding: ["8dp", "8dp", "8dp", "8dp"]
            spacing: "8dp"
    ```
  - Screen bottom padding: Add `padding: ["16dp", "16dp", "16dp", "32dp"]` (or `"88dp"` when a Floating Action Button is present).

---

### 7. Main-Thread Stutter from Dynamic Theming
* **The Symptom:** App hitches or freezes during track changes or screen transitions.
* **The Root Cause:** Recomputing Material You dynamic colors (`theme_cls.path_to_wallpaper`) triggers synchronous PIL image quantization, extracting palettes and recalculating 50+ widget properties. Redundant calls or un-cached paths freeze the main thread.
* **The Fix:** Debounce dynamic theme updates and check image path caching:
  ```python
  _pending_theme_event = None

  def update_theme_from_image(image_path: str):
      global _pending_theme_event
      if _pending_theme_event is not None:
          Clock.unschedule(_pending_theme_event)

      def _apply_theme(dt):
          global _pending_theme_event
          _pending_theme_event = None
          app = MDApp.get_running_app()
          if not app or not hasattr(app, "theme_cls"):
              return
          if image_path and os.path.exists(image_path):
              abs_path = os.path.abspath(image_path)
              if getattr(app.theme_cls, "path_to_wallpaper", None) == abs_path:
                  return  # Skip redundant re-quantization
              app.theme_cls.path_to_wallpaper = abs_path

      _pending_theme_event = Clock.schedule_once(_apply_theme, 0.15)
  ```

---

### 8. Unwired Interactive Widgets
* **The Symptom:** Clicking settings items, equalizer profiles, or top app bar actions produces no feedback or error.
* **The Fix:** Every interactive control must have an `on_release` or `on_touch_down` bound to an app method, modal dialog, or bottom sheet. Maintain true LIFO history navigation in `app.go_back()`:
  - If a dialog or bottom sheet is open, dismiss it first.
  - Otherwise, pop from `self.screen_history` and switch screens.

---

## Automated Headless Verification Template

Use this template to create regression test scripts:

```python
import os, sys
os.environ['KIVY_HEADLESS'] = '1'

from kivy.core.window import Window
from kivy.clock import Clock
from main import MusicApp

Window.size = (360, 640)
app = MusicApp()
root = app.build()
app.root = root
Window.add_widget(root)

for _ in range(10): Clock.tick()

# 1. Geometry overlap check
def check_overlap(w1, w2):
    p1 = w1.to_window(*w1.pos)
    p2 = w2.to_window(*w2.pos)
    overlap = not (p1[0] + w1.width <= p2[0] or p2[0] + w2.width <= p1[0] or
                   p1[1] + w1.height <= p2[1] or p2[1] + w2.height <= p1[1])
    return overlap

# 2. Touch simulation check
class MockTouch:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.dx, self.dy = 0, 0
        self.pos = (x, y)
        self.button = 'left'
        self.profile = ['pos', 'button']
        self.ud = {}
        self.time_start = 0
        self.time_update = 0.05
        self.push = lambda: None
        self.pop = lambda: None
        self.apply_transform_2d = lambda p: p
    def grab(self, w): pass
    def ungrab(self, w): pass
    def move(self, dx, dy):
        self.dx, self.dy = dx, dy
        self.x += dx; self.y += dy
        self.pos = (self.x, self.y)
        self.time_update += 0.016
```

---

## Verification Runbook Checklist

Before concluding any task involving UI changes:
- [ ] **Geometry Check:** Verify explicit heights on stacked bottom bars and test sibling non-overlap.
- [ ] **Touch Interception Check:** Verify `disabled: True` is set on conditionally hidden overlays.
- [ ] **Symmetry Check:** Assert $\lvert \text{Right Margin} - \text{Left Margin} \rvert < 1.0\text{dp}$ on centered action rows (`adaptive_size: True`).
- [ ] **Nested Scroll Check:** Verify that vertical drags and mouse wheel scrolling on horizontal carousels smoothly scroll the parent vertical scrollview.
- [ ] **Interactive Wiring Check:** Verify every button, chip, and menu item triggers an actionable method, sheet, or dialog.
- [ ] **Performance Check:** Confirm dynamic theming is debounced and cached, and async loading executes on early startup ($0.05\text{s}$).
- [ ] **Automated Headless Test Battery:** Execute `scratch/test_comprehensive_audit.py` and ensure 100% PASS rate.
