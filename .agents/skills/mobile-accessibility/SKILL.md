---
name: mobile-accessibility
description: Checklist and best practices for auditing and implementing accessibility in mobile and desktop Python apps (Kivy, KivyMD). Covers touch target sizing, color contrast, keyboard navigation, and descriptive actions.
---

# Mobile & Desktop UI Accessibility Checklist

Auditing and implementing accessibility standards (WCAG 2.1 AA) in Python applications built with Kivy and KivyMD.

## 1. Touch Target Sizes
* **Minimum Standard:** All interactive touch elements (buttons, icons, switches, slider thumbs) must be at least **48x48 dp**.
* **Visual Icon vs Touch Target:** If the visual icon is 24dp, expand the button bounds or touch padding to 48dp so users with motor impairments or on small touchscreens can reliably tap it.
* **In Kivy:**
  ```kv
  MDIconButton:
      icon: "heart-outline"
      size_hint: None, None
      size: dp(48), dp(48)
  ```

---

## 2. Color Contrast (WCAG AA)
* **Body & Secondary Text:** Contrast ratio must be at least **4.5:1** against the background.
* **Large Text (≥ 18sp) & Key Icons:** Contrast ratio must be at least **3.0:1**.
* **Dynamic / Album Theming:** When generating themes dynamically from album covers, ensure the text color automatically flips between dark and light tones depending on luminance (use `theme_cls.onSurfaceColor` or `theme_cls.onPrimaryColor`).

---

## 3. Clear & Actionable Icon Descriptions
* **Actionable Meaning:** Icons used for playback controls must represent the *action* taken, not the shape:
  * Good: `"Play Track"`, `"Pause"`, `"Next Track"`, `"Add to Playlist"`.
  * Bad: `"Triangle"`, `"Two bars"`, `"Plus sign"`.
* **Tooltips & Labels:** For desktop or tablet modes, provide `MDTooltip` or accompanying text labels for unlabeled icons.

---

## 4. Keyboard Navigation & Hardware Controls
* **Android Back Button (Key 27 / Escape):** Always handle the Android hardware back button cleanly. Close bottom sheets, exit fullscreen player, or return to the main library instead of unexpectedly terminating the app.
* **Keyboard Navigation:** Support keyboard shortcuts on desktop builds:
  * `Space`: Play / Pause toggle
  * `Left` / `Right`: Seek backward / forward (5-10s)
  * `Up` / `Down`: Volume adjustment
  * `Tab`: Advance focus between interactive controls
  * `Escape`: Close active dialogs, overlays, or return home

---

## 5. Typography & Readability
* Use scalable pixel units (`sp`) for text so that font scaling preferences on Android / OS settings are respected.
* Avoid truncating song titles without a marquee or subtitle; allow long titles to scroll or wrap cleanly.
