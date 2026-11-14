import os
import tempfile
import time

def get_thumbnail_path(video_id, cache_dir):
    thumb_path = os.path.join(cache_dir, f"{video_id}.jpg")
    if os.path.exists(thumb_path):
        return thumb_path
    web_url = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"
    return web_url

def test_thumbnail_path():
    td = tempfile.mkdtemp()
    
    # 1. Non-existent returns web URL
    url = get_thumbnail_path("abc12345678", td)
    assert url == "https://i.ytimg.com/vi/abc12345678/mqdefault.jpg"
    
    # 2. Existing local returns file path
    local_f = os.path.join(td, "abc12345678.jpg")
    with open(local_f, "wb") as f: f.write(b"fake image data")
    
    res = get_thumbnail_path("abc12345678", td)
    assert res == local_f
    print("Thumbnail logic test passed successfully!")

if __name__ == "__main__":
    test_thumbnail_path()
