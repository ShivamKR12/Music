import os
from kivy.clock import Clock
from kivymd.app import MDApp

_pending_theme_event = None

def update_theme_from_image(image_path: str):
    """
    Updates the KivyMD Material You Theme dynamically based on the album art.
    Extracts harmonized tonal palettes (primary, surfaceContainer, onSurface)
    and applies them across all active widgets.
    This is deferred and debounced to avoid stuttering during UI transitions.
    """
    global _pending_theme_event
    if _pending_theme_event is not None:
        Clock.unschedule(_pending_theme_event)

    def _apply_theme(dt):
        global _pending_theme_event
        _pending_theme_event = None
        app = MDApp.get_running_app()
        if not app or not hasattr(app, "theme_cls"):
            return
        if not getattr(app, "extract_artwork_colors", True):
            return
            
        if image_path and os.path.exists(image_path):
            abs_path = os.path.abspath(image_path)
            # Skip re-quantizing and re-applying if the wallpaper image is unchanged
            if getattr(app.theme_cls, "path_to_wallpaper", None) == abs_path:
                return
            app.theme_cls.path_to_wallpaper = abs_path
        else:
            # Safe fallback to default primary palette
            app.theme_cls.primary_palette = "Indigo"
            
    _pending_theme_event = Clock.schedule_once(_apply_theme, 0.15)
