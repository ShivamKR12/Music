from yt_dlp import YoutubeDL

class SilentLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): print(f"[YTDLP ERROR]: {msg}")

def test_fetch_metadata():
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'extract_flat': True,
        'socket_timeout': 10,
        'logger': SilentLogger(),
    }
    # Test flat extraction on a quick search
    with YoutubeDL(ydl_opts) as ydl:
        res = ydl.extract_info("ytsearch3:punjabi hits", download=False)
        entries = res.get('entries', [])
        print(f"Fetched {len(entries)} search entries:")
        for e in entries:
            print(f"- {e.get('title')} ({e.get('id')})")
        assert len(entries) > 0, "No entries found!"
    print("Flat search extraction test passed successfully!")

if __name__ == "__main__":
    test_fetch_metadata()
