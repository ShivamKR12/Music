import os
import re
import glob
import hashlib
from utils.media_utils import get_cache_dir

def clean_metadata_string(text: str) -> str:
    """Cleans up web promotion tags, brackets, and extra whitespace from metadata."""
    if not text:
        return ""
    # Strip common music site tags
    cleaned = re.sub(r'(?i)\s*-\s*(riskyjatt|songspk|djmaza|mp3mad|pagalworld|indiamp3|320kbps|waploft|pendujatt)\.com.*', '', text)
    cleaned = re.sub(r'(?i)\[\s*(songspk|djmaza|mp3mad|pagalworld|indiamp3|320kbps)\s*\]', '', cleaned)
    # Strip (Lyrics), (Official Audio), (320 kbps) etc
    cleaned = re.sub(r'[\(\[\{].*?(lyrics|320\s*kbps|official|audio|video|full song|hd|remix|slowed|reverb).*?[\)\]\}]', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def extract_embedded_artwork(data: bytes, safe_id: str, cache_dir: str) -> str:
    """
    Extracts embedded JPEG or PNG cover artwork from raw audio bytes and saves to cache.
    Uses APIC frame detection and PIL validation for rock-solid image integrity.
    Returns the absolute path of the extracted image, or empty string if not found.
    """
    if not data:
        return ""

    out_jpg = os.path.join(cache_dir, f"{safe_id}.jpg")
    out_png = os.path.join(cache_dir, f"{safe_id}.png")

    # If already successfully cached and valid, return path
    if os.path.exists(out_png) and os.path.getsize(out_png) > 1000:
        return out_png
    if os.path.exists(out_jpg) and os.path.getsize(out_jpg) > 1000:
        return out_jpg

    from PIL import Image
    import io

    def _try_save_image(img_bytes: bytes, out_path: str) -> bool:
        try:
            im = Image.open(io.BytesIO(img_bytes))
            im.verify()
            with open(out_path, 'wb') as f:
                f.write(img_bytes)
            return True
        except Exception:
            return False

    # 1. Search starting from ID3 APIC frame (preferred and most accurate)
    apic_idx = data.find(b'APIC')
    search_slices = [data[apic_idx:]] if apic_idx != -1 else []
    search_slices.append(data)

    for chunk in search_slices:
        # Check for PNG in chunk
        png_idx = chunk.find(b'\x89PNG\r\n\x1a\n')
        if png_idx != -1:
            iend_idx = chunk.find(b'IEND', png_idx)
            if iend_idx != -1:
                cand = chunk[png_idx:iend_idx + 8]
                if _try_save_image(cand, out_png):
                    return out_png

        # Check for JPEG in chunk
        jpg_idx = chunk.find(b'\xff\xd8\xff')
        if jpg_idx != -1:
            # Try right-most EOI marker first to ensure complete frame
            end_idx = chunk.rfind(b'\xff\xd9', jpg_idx)
            if end_idx != -1 and (end_idx + 2 - jpg_idx) > 1000:
                cand = chunk[jpg_idx:end_idx + 2]
                if _try_save_image(cand, out_jpg):
                    return out_jpg

            # Fallback to forward search for EOI marker
            fwd_end = chunk.find(b'\xff\xd9', jpg_idx + 1000)
            if fwd_end != -1:
                cand = chunk[jpg_idx:fwd_end + 2]
                if _try_save_image(cand, out_jpg):
                    return out_jpg

    return ""

def find_folder_artwork(folder_path: str) -> str:
    """Finds album cover image in the same directory as the audio file."""
    if not folder_path or not os.path.isdir(folder_path):
        return ""
    candidates = [
        "cover.jpg", "cover.png", "folder.jpg", "folder.png",
        "album.jpg", "album.png", "artwork.jpg", "artwork.png"
    ]
    for c in candidates:
        p = os.path.join(folder_path, c)
        if os.path.exists(p) and os.path.getsize(p) > 1000:
            return p
    for ext in ("*.jpg", "*.png", "*.jpeg"):
        matches = glob.glob(os.path.join(folder_path, ext))
        if matches:
            return matches[0]
    return ""

def extract_local_audio_metadata(file_path: str, cache_dir: str = None) -> dict:
    """
    Extracts rich metadata (Title, Artist, Album, Duration, Artwork)
    from a local audio file using native Python parsing.
    """
    if cache_dir is None:
        cache_dir = get_cache_dir()

    abs_path = os.path.abspath(file_path)
    base_name = os.path.splitext(os.path.basename(abs_path))[0]
    safe_id = f"loc_{hashlib.md5(abs_path.encode('utf-8')).hexdigest()[:10]}"

    title = base_name
    artist = ""
    album = "Offline Music"
    duration = 0
    artwork = ""

    file_size = os.path.getsize(abs_path) if os.path.exists(abs_path) else 0

    # 1. Parse ID3v2 Tags & Embedded Artwork
    try:
        with open(abs_path, 'rb') as f:
            head = f.read(10)
            tag_size = 0
            if head[:3] == b'ID3':
                ver_major = head[3]
                sb = head[6:10]
                tag_size = ((sb[0] & 0x7F) << 21) | ((sb[1] & 0x7F) << 14) | ((sb[2] & 0x7F) << 7) | (sb[3] & 0x7F)
                # Read tag data (capped at 5MB)
                read_amount = min(tag_size, 5 * 1024 * 1024)
                data = f.read(read_amount)
            else:
                data = f.read(min(file_size, 1024 * 1024))
                ver_major = 3

            # Extract image
            artwork = extract_embedded_artwork(data, safe_id, cache_dir)

            # Extract ID3 frames
            if head[:3] == b'ID3' and data:
                pos = 0
                while pos + 10 < len(data):
                    fid = data[pos:pos+4].decode('latin1', 'ignore')
                    if not fid or not fid[0].isalpha() or fid == '\x00\x00\x00\x00':
                        break
                    if ver_major == 4:
                        fb = data[pos+4:pos+8]
                        fsz = ((fb[0] & 0x7F) << 21) | ((fb[1] & 0x7F) << 14) | ((fb[2] & 0x7F) << 7) | (fb[3] & 0x7F)
                    else:
                        fsz = int.from_bytes(data[pos+4:pos+8], 'big')
                    pos += 10
                    if pos + fsz > len(data):
                        break
                    fdata = data[pos:pos+fsz]
                    pos += fsz

                    if fid in ('TIT2', 'TPE1', 'TALB', 'TLEN') and len(fdata) > 1:
                        enc = fdata[0]
                        raw = fdata[1:]
                        try:
                            if enc == 1:
                                val = raw.decode('utf-16').strip('\x00 ')
                            elif enc == 3:
                                val = raw.decode('utf-8').strip('\x00 ')
                            else:
                                val = raw.decode('latin1').strip('\x00 ')
                            if fid == 'TIT2' and val:
                                title = val
                            elif fid == 'TPE1' and val:
                                artist = val
                            elif fid == 'TALB' and val:
                                album = val
                            elif fid == 'TLEN' and val and val.isdigit():
                                duration = int(val) // 1000
                        except Exception:
                            pass
    except Exception:
        pass

    # 2. Try ID3v1 Tags if title or artist is empty
    if (not artist or not title or title == base_name) and file_size > 128:
        try:
            with open(abs_path, 'rb') as f:
                f.seek(-128, 2)
                tail = f.read(128)
                if tail[:3] == b'TAG':
                    v1_t = tail[3:33].strip(b'\x00 ').decode('latin1', 'ignore').strip()
                    v1_a = tail[33:63].strip(b'\x00 ').decode('latin1', 'ignore').strip()
                    if v1_t and title == base_name:
                        title = v1_t
                    if v1_a and not artist:
                        artist = v1_a
        except Exception:
            pass

    # 3. Smart Filename Heuristic if artist is missing
    title = clean_metadata_string(title)
    artist = clean_metadata_string(artist)

    if not artist or artist.lower() in ('unknown', 'local audio', 'various artists'):
        raw = clean_metadata_string(base_name)
        if ' - ' in raw:
            parts = raw.split(' - ', 1)
            artist = parts[0].strip()
            title = parts[1].strip()
        elif ' _ ' in raw:
            parts = raw.split(' _ ', 1)
            title = parts[0].strip()
            artist = parts[1].strip()
        else:
            artist = "Offline Song"

    if not title:
        title = clean_metadata_string(base_name) or "Unknown Title"

    # 4. Folder Artwork Fallback
    if not artwork:
        folder_art = find_folder_artwork(os.path.dirname(abs_path))
        if folder_art:
            artwork = folder_art
        else:
            artwork = "album_art.png"

    # 5. Estimate duration if unknown
    if duration <= 0 and file_size > 0:
        # Standard 128kbps = 16000 bytes/sec
        duration = max(30, int(file_size / 16000))

    return {
        "video_id": safe_id,
        "title": title,
        "artist": artist,
        "album": album,
        "duration": duration,
        "artwork": artwork,
        "local_path": abs_path,
        "url": "",
        "is_downloaded": True
    }

def get_standard_offline_music_dirs() -> list:
    """Returns candidate music directories across Windows, Android, and Linux."""
    dirs = []
    # 1. User Music folder
    u_music = os.path.expanduser("~/Music")
    if os.path.exists(u_music) and os.path.isdir(u_music):
        dirs.append(u_music)

    # 2. App Cache
    app_cache = get_cache_dir()
    if os.path.exists(app_cache) and os.path.isdir(app_cache):
        dirs.append(app_cache)

    # 3. User Downloads folder
    u_down = os.path.expanduser("~/Downloads")
    if os.path.exists(u_down) and os.path.isdir(u_down):
        dirs.append(u_down)

    # 4. Android storage paths
    android_paths = ["/sdcard/Music", "/sdcard/Download", "/storage/emulated/0/Music"]
    for ap in android_paths:
        if os.path.exists(ap) and os.path.isdir(ap):
            dirs.append(ap)

    return dirs

def scan_device_offline_songs(directories: list = None, cache_dir: str = None, limit: int = None) -> list:
    """
    Scans device music directories for local audio files (.mp3, .m4a, .wav, .ogg, .flac).
    Extracts rich metadata & artwork for every track and returns a list of track metadata dicts.
    """
    if directories is None:
        directories = get_standard_offline_music_dirs()
    if cache_dir is None:
        cache_dir = get_cache_dir()

    seen_paths = set()
    audio_extensions = {".mp3", ".m4a", ".wav", ".ogg", ".flac", ".opus", ".aac"}
    tracks = []

    for d in directories:
        if not os.path.exists(d):
            continue
        try:
            with os.scandir(d) as it:
                for entry in it:
                    if entry.is_file():
                        ext = os.path.splitext(entry.name)[1].lower()
                        if ext in audio_extensions:
                            abs_p = os.path.abspath(entry.path)
                            if abs_p not in seen_paths:
                                seen_paths.add(abs_p)
                                meta = extract_local_audio_metadata(abs_p, cache_dir=cache_dir)
                                tracks.append(meta)
                                if limit and len(tracks) >= limit:
                                    return tracks
        except Exception:
            continue

    return tracks
