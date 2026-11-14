import os
import sys
import time
import unittest

os.environ["KIVY_HEADLESS"] = "1"
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "KivyMusicApp"))
os.chdir(APP_DIR)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from kivy.clock import Clock
from models.database import init_db, add_track, get_all_tracks, update_track_artwork
from models.track_model import TrackModel, PlaylistModel

# Test the media utils artwork download functions
from utils.media_utils import get_cache_dir

class TestArtworkDownloadEngine(unittest.TestCase):
    def setUp(self):
        init_db()
        self.cache_dir = get_cache_dir()
        self.test_vid = "zxbDTgRivGI"  # Angreji Beat

    def test_01_direct_download(self):
        import urllib.request
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = f"https://i.ytimg.com/vi/{self.test_vid}/hqdefault.jpg"
        target_path = os.path.join(self.cache_dir, f"{self.test_vid}.jpg")
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            content = resp.read()
            self.assertGreater(len(content), 1000)
            with open(target_path, 'wb') as f:
                f.write(content)

        self.assertTrue(os.path.exists(target_path))
        self.assertGreater(os.path.getsize(target_path), 1000)
        print(f"Verified downloaded artwork at {target_path} ({os.path.getsize(target_path)} bytes)")

if __name__ == '__main__':
    unittest.main()
