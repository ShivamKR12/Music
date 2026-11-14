import re

def extract_video_id(url):
    """Extract YouTube video ID or return string if already an 11-char ID."""
    if not url:
        return ""
    if len(url) == 11 and not ("/" in url or "=" in url):
        return url
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    cleaned = re.sub(r'[^a-zA-Z0-9_-]', '', url)
    return cleaned[:11] if cleaned else "unknown"

def test_url_extraction():
    test_urls = [
        ("https://www.youtube.com/watch?v=TI7RQO2cuh0", "TI7RQO2cuh0"),
        ("https://youtu.be/TI7RQO2cuh0?si=test", "TI7RQO2cuh0"),
        ("https://music.youtube.com/watch?v=TI7RQO2cuh0&list=RDAM", "TI7RQO2cuh0"),
        ("TI7RQO2cuh0", "TI7RQO2cuh0"),
    ]
    for url, expected in test_urls:
        vid = extract_video_id(url)
        assert vid == expected, f"Failed for {url}: expected {expected}, got {vid}"
    print("URL extraction logic test passed successfully!")

if __name__ == "__main__":
    test_url_extraction()
