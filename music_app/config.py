import os
from kivy.config import Config
from kivy.utils import platform

if platform in ('win', 'macosx', 'linux'):
    Config.set('graphics', 'width', '375')
    Config.set('graphics', 'height', '667')
    Config.set('graphics', 'resizable', True)
    Config.set('graphics', 'fullscreen', False)

from kivy.core.text import LabelBase, DEFAULT_FONT

try:
    LabelBase.register(name="MaterialIcons", fn_regular="MaterialIcons-Regular.ttf")
    fallbacks = []
    if platform == 'win':
        font_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
        fallbacks = [
            os.path.join(font_dir, 'segoeui.ttf'),
            os.path.join(font_dir, 'seguiemj.ttf'),
            os.path.join(font_dir, 'msgothic.ttc'),
            os.path.join(font_dir, 'arial.ttf')
        ]
    elif platform == 'macosx':
        fallbacks = [
            '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
            '/System/Library/Fonts/Apple Color Emoji.ttc'
        ]
    elif platform == 'linux':
        fallbacks = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
        ]
    for font in fallbacks:
        if os.path.exists(font):
            LabelBase.register(DEFAULT_FONT, fn_regular=font)
            break
except Exception as e:
    print(f"Warning: font failed to load: {e}")

LIGHT_THEME = {
    "bg": (0.98, 0.97, 0.94, 1),
    "surface": (0.95, 0.97, 1.0, 1),
    "surface_alt": (1.0, 0.96, 0.96, 1),
    "text_primary": (0.12, 0.14, 0.18, 1),
    "text_secondary": (0.40, 0.42, 0.48, 1),
    "icon": (0.18, 0.20, 0.26, 1),
    "accent": (0.95, 0.55, 0.25, 1),
    "accent_soft": (1.0, 0.85, 0.70, 1),
}

def enforce_max_cache_size(cache_dir=None, max_size_mb=5000):
    """
    Checks total folder footprint size and flushes historical assets
    if the directory footprint exceeds the maximum constraints.
    """
    if cache_dir is None:
        from utils import get_cache_dir
        cache_dir = get_cache_dir()
        
    if not os.path.exists(cache_dir): return
    
    try:
        files = []
        total_size = 0
        for entry in os.scandir(cache_dir):
            if entry.is_file():
                stat = entry.stat()
                files.append((stat.st_mtime, stat.st_size, entry.path))
                total_size += stat.st_size
        max_bytes = max_size_mb * 1024 * 1024
        if total_size <= max_bytes: return
        files.sort(key=lambda x: x[0])
        print(f"Cache threshold exceeded ({total_size / 1024 / 1024:.2f} MB). Evicting older entries...")
        for _, size, path in files:
            if total_size <= max_bytes: break
            try:
                os.remove(path)
                total_size -= size
                print(f"Evicted item from storage cache: {path}")
            except Exception as e:
                print(f"Eviction exception targeting file path {path}: {e}")
    except Exception as e:
        print("General runtime footprint verification check failure:", e)
