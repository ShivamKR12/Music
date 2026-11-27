"""Reset transient button/ripple feedback when a screen or overlay is dismissed.

KivyMD paints press/ripple state directly into a widget's canvas. If a widget is
hidden while a menu, sheet or new screen opens, that canvas group can survive
the transition and show a stale highlight when the user navigates back.
Clearing the feedback on navigation guarantees a clean slate on every return.
"""

from __future__ import annotations

_RIPPLE_GROUPS = ("circular_ripple_behavior", "rectangular_ripple_behavior")


def clear_press_feedback(widget) -> None:
    """Clear pressed/rippling state on ``widget`` and all its descendants."""
    if widget is None:
        return
    try:
        walk = list(widget.walk())
    except Exception:
        walk = [widget]

    for w in walk:
        try:
            if hasattr(w, "state") and getattr(w, "state", "normal") != "normal":
                w.state = "normal"
        except Exception:
            pass
        try:
            if hasattr(w, "_doing_ripple"):
                w._doing_ripple = False
                w._finishing_ripple = False
                w._fading_out = False
                w._ripple_rad = 0
        except Exception:
            pass
        try:
            color = getattr(w, "ripple_color", None)
            if color is not None and len(color) >= 4:
                w.ripple_color = [color[0], color[1], color[2], 0.0]
        except Exception:
            pass
        for canvas in (getattr(w, "canvas", None),):
            if canvas is None:
                continue
            for group in _RIPPLE_GROUPS:
                for layer in (getattr(canvas, "before", None), getattr(canvas, "after", None)):
                    if layer is None:
                        continue
                    try:
                        layer.remove_group(group)
                    except Exception:
                        pass
