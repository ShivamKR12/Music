from kivy.clock import Clock
from kivymd.app import MDApp
import os

def update_theme_from_image(image_path: str):
    """
    Updates the KivyMD Theme dynamically based on the album art.
    This is deferred to avoid stuttering during screen transitions.
    """
    def _apply_theme(dt):
        app = MDApp.get_running_app()
        if os.path.exists(image_path):
            app.theme_cls.path_to_wallpaper = image_path
            
    # Defer the heavy theme generation by 300ms (after screen transition)
    Clock.schedule_once(_apply_theme, 0.3)

