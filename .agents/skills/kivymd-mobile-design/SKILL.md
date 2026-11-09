---
name: kivymd-mobile-design
description: Master Material Design 3 and KivyMD patterns for building responsive mobile and desktop Python apps. Use when designing interfaces, styling KivyMD components, or implementing Material Design 3 guidelines in Kivy.
---

# KivyMD Mobile & Desktop Design (Material Design 3)

Master Material Design 3 (Material You) and KivyMD (v2) to build modern, responsive, and tactile cross-platform music and media applications in Python.

## When to Use This Skill

- Designing and laying out user interfaces with Kivy & KivyMD.
- Implementing Material Design 3 components (`MDButton`, `MDFabButton`, `MDCard`, `MDBottomSheet`, `MDListItem`, `MDDialog`).
- Implementing dynamic theming, palette generation, and album-art-based UI tints.
- Designing responsive layouts for mobile screens (e.g. 360x640 baseline) and desktop windows.
- Structuring declarative `.kv` files cleanly and maintaining separation from Python controllers.
- Ensuring touch-friendly mobile UX (minimum 48dp touch targets, bottom navigation, swipe gestures).

---

## 1. Material Design 3 Theming in KivyMD

### Dynamic & Palette-Based Theming
KivyMD v2 provides built-in Material 3 color generation. Theming can be controlled globally via `self.theme_cls`:

```python
from kivymd.app import MDApp

class MusicApp(MDApp):
    def build(self):
        # Set primary palette and style
        self.theme_cls.primary_palette = "Indigo"  # e.g., "Orange", "Indigo", "Teal"
        self.theme_cls.theme_style = "Dark"        # "Light" or "Dark"
        self.theme_cls.dynamic_color = True        # Enables Material 3 dynamic color tokens
        return ...
```

### Dynamic Theme Extraction from Album Art
For music players, extracting palette tones from the current track's album cover produces an immersive, native feel:
- Extract dominant color with `materialyoucolor` or PIL/Pillow.
- Update `theme_cls.primary_palette` or custom canvas background colors smoothly.
- Ensure text contrast: use `theme_cls.onPrimaryColor`, `theme_cls.onSurfaceColor`, or `theme_cls.onSurfaceVariantColor`.

---

## 2. Layout & Spacing System

Always use density-independent pixels (`dp`) and scalable pixels (`sp`) for text:

| Token | Dimension | Use Case |
|---|---|---|
| **Compact Spacing** | `4dp` - `8dp` | Spacing between tight elements (icon and text, chip padding). |
| **Element Spacing** | `12dp` - `16dp` | Margin between cards, list items, and standard controls. |
| **Screen Padding** | `16dp` - `24dp` | Screen edge margins on phones; `24dp` - `32dp` on tablets/desktop. |
| **Touch Target** | **≥ 48dp** | Minimum width & height for any clickable button, icon, or slider handle. |

### Responsive Layout Example (.kv)

```kv
<PlayerControlBar@MDBoxLayout>:
    orientation: "horizontal"
    adaptive_height: True
    padding: dp(16), dp(8)
    spacing: dp(12)
    pos_hint: {"center_x": 0.5}

    MDIconButton:
        icon: "skip-previous"
        style: "standard"
        size_hint: None, None
        size: dp(48), dp(48)
        on_release: app.player_controller.previous_track()

    MDFabButton:
        icon: "play" if not app.player_controller.is_playing else "pause"
        style: "primary"
        size_hint: None, None
        size: dp(56), dp(56)
        on_release: app.player_controller.toggle_play()

    MDIconButton:
        icon: "skip-next"
        style: "standard"
        size_hint: None, None
        size: dp(48), dp(48)
        on_release: app.player_controller.next_track()
```

---

## 3. Core Component Guidelines

### Bottom Sheets (`MDBottomSheet`)
Use bottom sheets for non-disruptive secondary actions (such as queue management, track options, or playlist selector):
```python
from kivymd.uix.bottomsheet import (
    MDBottomSheet,
    MDBottomSheetDragHandle,
    MDBottomSheetDragHandleTitle
)

sheet = MDBottomSheet(
    MDBottomSheetDragHandle(
        MDBottomSheetDragHandleTitle(text="Playing Queue")
    )
)
sheet.open()
```

### Cards & Surfaces (`MDCard`)
Use cards to group related information (album details, trending music cards, mini-player):
- Use `elevation: 1` or `2` for interactive cards.
- Add rounded corners with `radius: [dp(16), dp(16), dp(16), dp(16)]`.
- Never put heavy logic or blocking calls inside card touch events.

---

## 4. Performance & Fluidity

1. **Keep UI Thread Free:** Any heavy network calls (`yt-dlp`), audio decoding (`ffpyplayer`), or file scanning must run in background threads (`threading.Thread`) and push UI updates back via `Clock.schedule_once`.
2. **Reuse List Items:** For large song libraries or playlists, use lazy loading or recycle views (`MDRecycleView` or batched insertion) rather than loading 1,000 widgets into a layout at once.
3. **Texture / Image Caching:** Use `AsyncImage` or preloaded textures with placeholder images (`blank.png` or `default_album.png`) to avoid hitching during scrolling.
