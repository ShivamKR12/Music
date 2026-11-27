"""Lightweight cross-platform haptic feedback.

Android uses the platform `Vibrator` (API 26+ `VibrationEffect`); every other
platform is a silent no-op so tests and desktop runs stay deterministic.

All helpers are fire-and-forget and must be called from the Kivy main thread.
"""

from __future__ import annotations

import threading

from kivy.utils import platform

from services.logger import get_logger

logger = get_logger("Haptics")

_vibrator = None
_vibration_effect_cls = None
_sdk_int = 0
_lock = threading.Lock()
_unavailable = False


def _resolve_vibrator():
    """Resolve and cache the Android Vibrator service once."""
    global _vibrator, _vibration_effect_cls, _sdk_int, _unavailable
    if _vibrator is not None or _unavailable:
        return _vibrator
    with _lock:
        if _vibrator is not None or _unavailable:
            return _vibrator
        try:
            from jnius import autoclass

            python_activity = autoclass("org.kivy.android.PythonActivity")
            context = autoclass("android.content.Context")
            build_version = autoclass("android.os.Build$VERSION")
            activity = python_activity.mActivity
            if activity is None:
                _unavailable = True
                return None
            _sdk_int = int(getattr(build_version, "SDK_INT", 0) or 0)
            if _sdk_int >= 26:
                _vibration_effect_cls = autoclass("android.os.VibrationEffect")
            _vibrator = activity.getSystemService(context.VIBRATOR_SERVICE)
        except Exception as exc:  # noqa: BLE001 - optional platform feature
            logger.debug("Android vibrator unavailable: %s", exc)
            _unavailable = True
    return _vibrator


def vibrate(duration_ms: int = 10) -> None:
    """Fire a short one-shot vibration (no-op off Android)."""
    if platform != "android":
        return
    vibrator = _resolve_vibrator()
    if vibrator is None:
        return
    try:
        duration_ms = max(1, int(duration_ms))
        if _sdk_int >= 26 and _vibration_effect_cls is not None:
            effect = _vibration_effect_cls.createOneShot(
                duration_ms, _vibration_effect_cls.DEFAULT_AMPLITUDE
            )
            vibrator.vibrate(effect)
        else:
            vibrator.vibrate(duration_ms)
    except Exception as exc:  # noqa: BLE001 - feedback must never crash UI
        logger.debug("Haptic vibration failed: %s", exc)


def tick() -> None:
    """Crisp selection tick used for transport, rows and toggles."""
    vibrate(8)


def confirm() -> None:
    """Slightly stronger confirmation used for like/queue actions."""
    vibrate(14)


def swipe() -> None:
    """Threshold feedback used while a swipe action commits."""
    vibrate(10)
