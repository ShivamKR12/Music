import os
import sys

# Test media_utils import and functions
sys.path.insert(0, os.path.abspath('KivyMusicApp'))

from utils.media_utils import (
    sanitize_text,
    format_time,
    get_cache_dir,
    get_thumbnail_path,
    extract_video_id,
    fetch_youtube_metadata,
    enforce_max_cache_size
)

def test():
    # 1. Sanitize text
    assert sanitize_text("Hello 🔥 World 🎵") == "Hello World"
    assert sanitize_text(None) == "Unknown"
    
    # 2. Format time
    assert format_time(185) == "3:05"
    assert format_time(0) == "0:00"
    
    # 3. Extract video ID
    assert extract_video_id("https://www.youtube.com/watch?v=TI7RQO2cuh0") == "TI7RQO2cuh0"
    assert extract_video_id("TI7RQO2cuh0") == "TI7RQO2cuh0"
    
    # 4. Cache dir
    cdir = get_cache_dir()
    assert os.path.exists(cdir)
    
    # 5. Thumbnail path for TI7RQO2cuh0 (which exists in cache)
    tpath = get_thumbnail_path("TI7RQO2cuh0")
    assert os.path.exists(tpath)
    assert tpath.endswith(".jpg")
    
    # 6. Enforce max cache size runs without error
    enforce_max_cache_size(max_size_mb=10000)
    
    print("Media utils verification test passed!")

if __name__ == "__main__":
    test()
