"""Cheap render-only micro-interactions (icon pop, snap-back helpers).

These helpers never touch layout properties: they scale the widget's canvas
around its center so labels, icons and ripples pop without re-rendering text
textures or invalidating the parent layout.
"""

from __future__ import annotations

from kivy.animation import Animation
from kivy.graphics import PopMatrix, PushMatrix, Scale


class _PopTransform:
    """Holds the canvas instructions and current scale for one widget."""

    __slots__ = ("scale", "widget")

    def __init__(self, widget):
        self.widget = widget
        with widget.canvas.before:
            PushMatrix()
            self.scale = Scale(1.0, 1.0, 1.0, origin=self._origin())
        with widget.canvas.after:
            PopMatrix()
        widget.bind(pos=self._sync_origin, size=self._sync_origin)

    def _origin(self):
        widget = self.widget
        return (widget.center_x, widget.center_y, 0.0)

    def _sync_origin(self, *_args):
        self.scale.origin = self._origin()


def pop_widget(widget, scale: float = 1.12, in_duration: float = 0.05, out_duration: float = 0.09):
    """Briefly scale a widget up and back (total ~140 ms, zero layout work)."""
    if widget is None:
        return
    try:
        transform = getattr(widget, "_pop_transform", None)
        if transform is None:
            transform = _PopTransform(widget)
            widget._pop_transform = transform

        instruction = transform.scale
        Animation.cancel_all(instruction)
        (Animation(x=scale, y=scale, duration=in_duration, transition="out_quad")
         + Animation(x=1.0, y=1.0, duration=out_duration, transition="out_quad")
         ).start(instruction)
    except Exception:
        # Feedback polish must never break an interaction.
        pass
