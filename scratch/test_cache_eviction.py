import os
import tempfile
import time

def enforce_max_cache_size(cache_dir, max_size_mb=1):
    if not os.path.exists(cache_dir): return
    try:
        files = []
        total_size = 0
        for entry in os.scandir(cache_dir):
            if entry.is_file():
                stat = entry.stat()
                files.append((stat.st_mtime, stat.st_size, entry.path))
                total_size += stat.st_size
        max_bytes = int(max_size_mb * 1024 * 1024)
        if total_size <= max_bytes: return
        files.sort(key=lambda x: x[0])
        for _, size, path in files:
            if total_size <= max_bytes: break
            try:
                os.remove(path)
                total_size -= size
            except Exception as e:
                print(f"Error removing {path}: {e}")
    except Exception as e:
        print("General runtime footprint verification check failure:", e)

def test_eviction():
    td = tempfile.mkdtemp()
    
    # Create 3 files of 600 KB each (total 1.8 MB) with different mtimes
    f1 = os.path.join(td, "old.mp3")
    f2 = os.path.join(td, "mid.mp3")
    f3 = os.path.join(td, "new.mp3")
    
    with open(f1, "wb") as f: f.write(b"0" * (600 * 1024))
    os.utime(f1, (time.time() - 300, time.time() - 300))
    
    with open(f2, "wb") as f: f.write(b"0" * (600 * 1024))
    os.utime(f2, (time.time() - 200, time.time() - 200))
    
    with open(f3, "wb") as f: f.write(b"0" * (600 * 1024))
    os.utime(f3, (time.time() - 100, time.time() - 100))
    
    # Enforce limit of 1 MB: oldest file should be evicted first!
    enforce_max_cache_size(td, max_size_mb=1.0)
    
    assert not os.path.exists(f1), "Oldest file should have been evicted!"
    assert not os.path.exists(f2), "Second oldest file should have been evicted to get <= 1MB!"
    assert os.path.exists(f3), "Newest file should still exist!"
    print("Cache eviction test passed successfully!")

if __name__ == "__main__":
    test_eviction()
