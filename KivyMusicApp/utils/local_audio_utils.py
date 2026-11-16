import os
import re
import glob
import struct
import hashlib
from utils.media_utils import get_cache_dir

SINGER_KEYWORDS = [
    'singh', 'kaur', 'khan', 'ali', 'sharma', 'verma', 'gill', 'sethi', 'nautiyal',
    'grewal', 'badshah', 'arijit', 'jubin', 'neha', 'kakkar', 'armaan', 'malik',
    'atif', 'aslam', 'sonu', 'nigam', 'shreya', 'ghoshal', 'kumar', 'udit', 'narayan',
    'lata', 'mangeshkar', 'kishore', 'mohit', 'chauhan', 'falak', 'shabir', 'sukh-e',
    'raftaar', 'divine', 'sidhu', 'moose', 'aujla', 'dhillon', 'dosanjh', 'amrinder',
    'sandhu', 'manak', 'randhawa', 'honey singh', 'yo yo', 'mc square', 'paradox',
    'kaka', 'shubh', 'rikhari', 'pritam', 'sachin-j', 'rahman', 'tanishk', 'mithoon',
    'vishal', 'shekhar', 'neeti', 'mohan', 'darshan', 'raval', 'anuv', 'jain', 'prateek',
    'kuhad', 'benjamin', 'rybak', 'post malone', 'sam smith', 'dua lipa', 'sean paul',
    'thefatrat', 'the score', 'masked wolf', 'nathan evans', 'neoni', 'soap&skin',
    'sub urban', 'kehlani', 'desiigner', 'sia', 'nf', 'palak', 'yasser', 'nadeem',
    'imagine dragons', 'j. cole', 'jay sean', 'alan walker', 'marshmello', 'avicii',
    'eminem', 'ed sheeran', 'charlie puth', 'billie eilish', 'khalid', 'jazzy',
    'apache', 'apache indian', 'kulbir', 'jhinjer', 'sukshinder', 'shinda',
    'deep jandu', 'parmish', 'pardhaan', 'rochak', 'kohli', 'gurdas', 'maan', 'babbal',
    'shasha', 'tirupati', 'nikhita', 'gandhi', 'lost sky', 'gabry ponte'
]

KNOWN_ARTISTS_P1 = {
    'sia', 'desiigner', 'nf', 'neoni', 'thefatrat', 'the score', 'masked wolf',
    'nathan evans', 'post malone', 'sam smith', 'sean paul, dua lipa', 'alec benjamin',
    'alexander rybak', 'soap&skin', 'shubh', 'aditya rikhari', 'kaka', 'badshah',
    'mc square', 'paradox', 'jubin nautiyal', 'yo yo honey singh', 'arijit singh',
    'imagine dragons', 'j. cole', 'jay sean', 'alan walker', 'marshmello', 'avicii',
    'kr$na', 'sub urban', 'kehlani', 'gabry ponte', 'lost sky', 'unknown brain',
    'amrinder gill', 'kulbir jhinjer', 'jazzy b', 'against the current', 'eric matyas'
}

PROMO_CHANNELS = [
    'lyrics', 'records', 'official', 'series', 'music', 'verse', 'videos',
    'vibes', 'channel', 'vevo', 'production', 'studios', 't-series', 'sony',
    'tips', 'srgm', 'zeemusic', 'speed records', 'desi songs', 'black pagoda',
    'afternight', 'seventyskye', 'vibe bird', 'rg lyrics', 'lite lyrics',
    'love & lyrics', 'vip lyrics', 'cassettes', 'robotic verse', 'desisongsvideos'
]

# Curated high-confidence mapping for well-known tracks with noisy or missing tags
SPECIAL_SONG_MAP = {
    "ARJAN VAILLY": ("Arjan Vailly", "Bhupinder Babbal, Manan Bhardwaj"),
    "AANKHON MEIN AANSOON": ("Aankhon Mein Aansoon", "Nadeem, Palak, Yasser"),
    "PASOORI": ("Pasoori", "Ali Sethi, Shae Gill"),
    "TUM HI HO": ("Tum Hi Ho", "Arijit Singh"),
    "SWIMMING PUL": ("Angna Me Saiya Swimming Pul", "Bhojpuri Remix"),
    "SUNNY DEOL": ("Sunny Deol Si Body", "Slowed & Reverb"),
    "AAM JAHE MUNDE": ("Aam Jahe Munde", "Parmish Verma feat. Pardhaan"),
    "PEENE KI TAMANNA": ("Peene Ki Tamanna", "Vishal Dadlani, Parichay"),
    "QAAFIRANA": ("Qaafirana", "Arijit Singh, Nikhita Gandhi"),
    "THE HUMMA SONG": ("The Humma Song", "A.R. Rahman, Badshah, Tanishk"),
    "HUMMA SONG": ("The Humma Song", "A.R. Rahman, Badshah, Tanishk"),
    "OK JAANU": ("The Humma Song", "A.R. Rahman, Badshah, Tanishk"),
    "LO MAAN LIYA": ("Lo Maan Liya", "Arijit Singh"),
    "DIL PE ZAKHAM": ("Dil Pe Zakham Khate Hain (Remix)", "Jubin Nautiyal, Rochak Kohli"),
    "HAR FUNN MAULA": ("Har Funn Maula", "Vishal Dadlani, Zara Khan"),
    "KALANK": ("Kalank (Title Track)", "Arijit Singh, Pritam"),
    "TERI MERI KAHAANI": ("Teri Meri Kahaani", "Arijit Singh & Palak Muchhal"),
    "PAL PAL DIL KE PAAS": ("Pal Pal Dil Ke Paas", "Arijit Singh"),
    "ZINDAGI HAI TU": ("Meri Zindagi Hai Tu (Remix)", "Nusrat Fateh Ali Khan"),
    "KALI KALI ZULFON": ("Kali Kali Zulfon Ke Phande (Remix)", "Nusrat Fateh Ali Khan"),
    "ALL BLACK": ("All Black", "Sukh-E feat. Raftaar"),
    "FEARLESS": ("Fearless", "Lost Sky"),
    "LEGENDS NEVER DIE": ("Legends Never Die", "Against The Current"),
    "LOVELY": ("Lovely", "Billie Eilish, Khalid"),
    "ANGREJI BEAT": ("Angreji Beat", "Yo Yo Honey Singh, Gippy Grewal"),
    "FAIRYTALE": ("Fairytale", "Alexander Rybak"),
    "ZAROORI THA": ("Zaroori Tha", "Rahat Fateh Ali Khan"),
    "SAIYAARA": ("Saiyaara", "Mohit Chauhan, Tarannum Mallik"),
    "MAHI AAJA": ("Mahi Aaja (Unplugged)", "Arijit Singh, Manj Musik"),
    "MUSKAANEIN JHOOTI": ("Muskaanein Jhooti Hai", "Suman Sridhar"),
    "PHIR BHI TUMKO": ("Phir Bhi Tumko Chaahunga", "Arijit Singh, Sasha Tirupati"),
    "APNA BANA LE": ("Apna Bana Le", "Arijit Singh, Sachin-Jigar"),
    "AE DIL HAI MUSHKIL": ("Ae Dil Hai Mushkil", "Arijit Singh, Pritam"),
    "DIL LUTIYA": ("Dil Lutiya", "Jazzy B ft. Apache Indian"),
    "PUNJAB SEYAN": ("Punjab Seyan", "Kulbir Jhinjer"),
    "BANERE TE": ("Banere Te", "Amrinder Gill"),
}

def is_channel_or_junk(text: str) -> bool:
    """Checks if metadata text represents a YouTube promo channel, generic placeholder, or junk label."""
    if not text:
        return True
    t_low = text.lower().strip()
    if t_low in ('offline song', 'offline music', 'local audio', 'unknown artist', 'unknown', 'various artists', 'none', 'unknown title'):
        return True
    for p in PROMO_CHANNELS:
        if p in t_low:
            return True
    return False

def clean_tags(text: str) -> str:
    """Cleans up web promotion tags, brackets, and extra whitespace from metadata strings."""
    if not text:
        return ""
    text = text.replace(" _ ", " - ").replace(" __ ", " - ").replace("|", " - ").replace("•", " - ").replace("–", "-").replace("—", "-")
    # Strip brackets containing technical or promotional fluff
    text = re.sub(r'[\(\[\{][^\)\]\}]*(?:lyrics|official|audio|video|full song|hd|remix|slowed|reverb|kbps|monstercat|winner|norway|eurovision|from|soundtrack|hustle)[^\)\]\}]*[\)\]\}]', '', text, flags=re.IGNORECASE)
    # Strip standalone keywords
    text = re.sub(r'(?i)\b(lyrics|official video|official audio|full video song|full song with lyrics|video song|full song|320\s*kbps|64\s*kbps|hd|4k)\b', '', text)
    # Strip common music download site suffixes
    text = re.sub(r'(?i)\s*-\s*(riskyjatt|songspk|djmaza|mp3mad|pagalworld|indiamp3|waploft|pendujatt)\.com.*', '', text)
    text = re.sub(r'(?i)\[\s*(songspk|djmaza|mp3mad|pagalworld|indiamp3)\s*\]', '', text)
    text = text.strip(' "\'_-|#•')
    text = re.sub(r'\s+', ' ', text)
    return text

clean_metadata_string = clean_tags

def parse_audio_name(raw_title: str, raw_artist: str, filename: str) -> tuple[str, str]:
    """
    Intelligently parses audio title and artist from raw tags and filename.
    Resolves promo channels, handles 'Artist - Title' vs 'Title - Artist' orientation,
    and removes noise.
    """
    base_name = os.path.splitext(filename)[0]

    # 0. Check SPECIAL_SONG_MAP against combined text first
    combined_upper = f"{raw_title or ''} {raw_artist or ''} {base_name}".upper()
    for key, (t_spec, a_spec) in SPECIAL_SONG_MAP.items():
        if key in combined_upper:
            return t_spec, a_spec

    # 1. Clean the given metadata
    c_title = clean_tags(raw_title or base_name)
    c_artist = clean_tags(raw_artist or "")

    # Check if artist is empty or a promo channel
    artist_bad = is_channel_or_junk(c_artist)

    # Determine source string to split
    source_to_split = None
    if artist_bad or not raw_title or not raw_artist:
        source_to_split = raw_title if (raw_title and (" - " in raw_title or " _ " in raw_title or "|" in raw_title)) else base_name
    elif " - " in c_title:
        source_to_split = c_title

    if source_to_split:
        norm = clean_tags(source_to_split)
        parts = [p.strip() for p in norm.split(" - ") if p.strip()]
        if len(parts) >= 2:
            p1 = parts[0]
            p2 = parts[1]

            if c_artist and not artist_bad:
                if c_artist.lower() in p1.lower():
                    c_title = p2
                elif c_artist.lower() in p2.lower():
                    c_title = p1
            else:
                p1_low = p1.lower()
                p2_low = p2.lower()
                p1_is_artist = p1_low in KNOWN_ARTISTS_P1 or any(p1_low.startswith(a) for a in KNOWN_ARTISTS_P1)
                p2_is_artist = p2_low in KNOWN_ARTISTS_P1 or any(p2_low.startswith(a) for a in KNOWN_ARTISTS_P1)
                p1_has_singer = any(k in p1_low for k in SINGER_KEYWORDS)
                p2_has_singer = any(k in p2_low for k in SINGER_KEYWORDS)

                if p1_is_artist:
                    c_artist = p1
                    c_title = p2
                elif p2_is_artist:
                    c_title = p1
                    c_artist = p2
                elif p1_has_singer and not p2_has_singer:
                    c_artist = p1
                    c_title = p2
                elif p2_has_singer and not p1_has_singer:
                    c_title = p1
                    c_artist = p2
                elif len(parts) > 2 and any(k in parts[2].lower() for k in SINGER_KEYWORDS):
                    c_title = p1
                    c_artist = parts[2]
                else:
                    c_artist = p1
                    c_title = p2

    # Clean redundant artist from title
    if c_artist and c_artist.lower() in c_title.lower() and len(c_title) > len(c_artist):
        c_title = re.sub(re.escape(c_artist), '', c_title, flags=re.IGNORECASE).strip(' -_–—|')

    c_title = clean_tags(c_title)
    c_artist = clean_tags(c_artist)

    if c_title and c_title.islower():
        c_title = c_title.title()

    if not c_title:
        c_title = clean_tags(base_name) or "Unknown Title"
    if not c_artist or is_channel_or_junk(c_artist):
        c_artist = "Offline Music"

    return c_title, c_artist

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

def parse_audio_duration(abs_path: str) -> int:
    """
    Fast native extraction of exact audio duration in seconds
    for MP3 (Xing header + CBR stream), WAV, and FLAC.
    """
    if not abs_path or not os.path.exists(abs_path):
        return 0
    size = os.path.getsize(abs_path)
    if size < 128:
        return 0

    ext = os.path.splitext(abs_path)[1].lower()

    # 1. WAV duration: data size / byte_rate
    if ext == '.wav':
        try:
            with open(abs_path, 'rb') as f:
                header = f.read(44)
                if header[:4] == b'RIFF' and header[8:12] == b'WAVE':
                    byte_rate = struct.unpack('<I', header[28:32])[0]
                    if byte_rate > 0:
                        return int((size - 44) / byte_rate)
        except Exception:
            pass

    # 2. FLAC duration: sample_rate and total_samples from STREAMINFO
    if ext == '.flac':
        try:
            with open(abs_path, 'rb') as f:
                head = f.read(42)
                if head[:4] == b'fLaC':
                    b = head[18:26]
                    sr = (b[0] << 12) | (b[1] << 4) | (b[2] >> 4)
                    total_samples = ((b[3] & 0x0F) << 32) | (b[4] << 24) | (b[5] << 16) | (b[6] << 8) | b[7]
                    if sr > 0:
                        return int(total_samples / sr)
        except Exception:
            pass

    # 3. MP3: Fast MPEG frame sync + Xing / Info header or CBR frame rate
    if ext in ('.mp3', '.m4a', ''):
        try:
            with open(abs_path, 'rb') as f:
                data = f.read(min(size, 131072))

            pos = 0
            if data[:3] == b'ID3':
                sb = data[6:10]
                tag_size = ((sb[0] & 0x7F) << 21) | ((sb[1] & 0x7F) << 14) | ((sb[2] & 0x7F) << 7) | (sb[3] & 0x7F)
                pos = 10 + tag_size
                if pos >= len(data):
                    with open(abs_path, 'rb') as f:
                        f.seek(pos)
                        data = f.read(65536)
                    pos = 0

            bitrates_v1_l3 = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
            bitrates_v2_l3 = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0]
            sample_rates_v1 = [44100, 48000, 32000, 0]
            sample_rates_v2 = [22050, 24000, 16000, 0]
            sample_rates_v25 = [11025, 12000, 8000, 0]

            for i in range(pos, min(len(data) - 4, pos + 32768)):
                if data[i] == 0xFF and (data[i+1] & 0xE0) == 0xE0:
                    header = struct.unpack('>I', data[i:i+4])[0]
                    version = (header >> 19) & 3
                    layer = (header >> 17) & 3
                    if version == 1 or layer != 1:
                        continue
                    bitrate_idx = (header >> 12) & 0xF
                    sr_idx = (header >> 10) & 3
                    channel_mode = (header >> 6) & 3

                    if bitrate_idx in (0, 15) or sr_idx == 3:
                        continue

                    if version == 3:  # MPEG 1
                        sr = sample_rates_v1[sr_idx]
                        br = bitrates_v1_l3[bitrate_idx] * 1000
                        side_info_len = 32 if channel_mode != 3 else 17
                        samples_per_frame = 1152
                    else:  # MPEG 2 or 2.5
                        sr = sample_rates_v2[sr_idx] if version == 2 else sample_rates_v25[sr_idx]
                        br = bitrates_v2_l3[bitrate_idx] * 1000
                        side_info_len = 17 if channel_mode != 3 else 9
                        samples_per_frame = 576

                    # Check for Xing / Info header
                    xing_pos = i + 4 + side_info_len
                    if xing_pos + 12 <= len(data):
                        tag = data[xing_pos:xing_pos+4]
                        if tag in (b'Xing', b'Info'):
                            flags = struct.unpack('>I', data[xing_pos+4:xing_pos+8])[0]
                            if flags & 1:  # Frames field present
                                total_frames = struct.unpack('>I', data[xing_pos+8:xing_pos+12])[0]
                                dur = (total_frames * samples_per_frame) / sr
                                return int(dur)

                    # CBR estimation from bitrate and audio stream size
                    audio_stream_size = size - i
                    if br > 0:
                        dur = (audio_stream_size * 8) / br
                        return int(dur)
        except Exception:
            pass

    return 0

def extract_local_audio_metadata(file_path: str, cache_dir: str = None) -> dict:
    """
    Extracts rich metadata (Title, Artist, Album, Duration, Artwork)
    from a local audio file using native Python parsing.
    Guarantees clean, non-reversed artist/title and sanitized tags.
    """
    if cache_dir is None:
        cache_dir = get_cache_dir()

    abs_path = os.path.abspath(file_path)
    base_name = os.path.splitext(os.path.basename(abs_path))[0]

    # Canonical ID: prefer 11-char YouTube ID for cached assets, else deterministic loc hash
    if re.match(r'^[a-zA-Z0-9_-]{11}$', base_name):
        safe_id = base_name
    else:
        safe_id = f"loc_{hashlib.md5(abs_path.encode('utf-8')).hexdigest()[:10]}"

    raw_title = ""
    raw_artist = ""
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
                read_amount = min(tag_size, 5 * 1024 * 1024)
                data = f.read(read_amount)
            else:
                data = f.read(min(file_size, 1024 * 1024))
                ver_major = 3

            # Extract embedded image
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
                                raw_title = val
                            elif fid == 'TPE1' and val:
                                raw_artist = val
                            elif fid == 'TALB' and val:
                                album = val
                            elif fid == 'TLEN' and val and val.isdigit():
                                duration = int(val) // 1000
                        except Exception:
                            pass
    except Exception:
        pass

    # 2. Try ID3v1 Tags if title or artist is empty
    if (not raw_artist or not raw_title) and file_size > 128:
        try:
            with open(abs_path, 'rb') as f:
                f.seek(-128, 2)
                tail = f.read(128)
                if tail[:3] == b'TAG':
                    v1_t = tail[3:33].strip(b'\x00 ').decode('latin1', 'ignore').strip()
                    v1_a = tail[33:63].strip(b'\x00 ').decode('latin1', 'ignore').strip()
                    if v1_t and not raw_title:
                        raw_title = v1_t
                    if v1_a and not raw_artist:
                        raw_artist = v1_a
        except Exception:
            pass

    # 3. Check Sidecar .json metadata
    sidecar_candidates = [
        os.path.join(os.path.dirname(abs_path), f"{base_name}.json"),
        os.path.join(os.path.dirname(abs_path), f"{base_name}.info.json"),
    ]
    if cache_dir:
        sidecar_candidates.extend([
            os.path.join(cache_dir, f"{base_name}.json"),
            os.path.join(cache_dir, f"{base_name}.info.json"),
        ])

    for sc in sidecar_candidates:
        if os.path.exists(sc):
            try:
                import json
                with open(sc, "r", encoding="utf-8") as jf:
                    sdata = json.load(jf)
                    if sdata.get("title") and (not raw_title or is_channel_or_junk(raw_title)):
                        raw_title = sdata.get("title")
                    if sdata.get("artist") and (not raw_artist or is_channel_or_junk(raw_artist)):
                        raw_artist = sdata.get("artist")
                    elif sdata.get("uploader") and (not raw_artist or is_channel_or_junk(raw_artist)):
                        raw_artist = sdata.get("uploader")
                    if sdata.get("artwork") and os.path.exists(sdata.get("artwork")) and not artwork:
                        artwork = sdata.get("artwork")
                    if sdata.get("duration") and sdata.get("duration") > 0 and duration <= 0:
                        duration = int(sdata.get("duration"))
                    if sdata.get("id"):
                        safe_id = sdata.get("id")
                break
            except Exception:
                pass

    # 4. Check SQLite database ONLY for cached assets where base_name is a hash/ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', base_name):
        try:
            from models.database import get_connection
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT video_id, title, artist, artwork, duration FROM tracks WHERE video_id = ? OR local_path = ?", (base_name, abs_path))
            row = cur.fetchone()
            if row:
                db_vid, db_title, db_artist, db_art, db_dur = row[0], row[1], row[2], row[3], row[4]
                if db_title and db_title != base_name and not is_channel_or_junk(db_title):
                    if not raw_title or is_channel_or_junk(raw_title) or raw_title == base_name:
                        raw_title = db_title
                if db_artist and not is_channel_or_junk(db_artist):
                    if not raw_artist or is_channel_or_junk(raw_artist):
                        raw_artist = db_artist
                if db_art and not artwork and os.path.exists(db_art):
                    artwork = db_art
                if db_dur and duration <= 0:
                    duration = db_dur
        except Exception:
            pass

    # 5. Smart Parsing for Title and Artist
    final_title, final_artist = parse_audio_name(raw_title, raw_artist, os.path.basename(abs_path))

    # 6. Check matching artwork in cache or directory
    if not artwork or not os.path.exists(artwork) or artwork == "album_art.png":
        for search_d in (os.path.dirname(abs_path), cache_dir) if cache_dir else (os.path.dirname(abs_path),):
            for ext in (".jpg", ".png", ".webp", ".jpeg"):
                art_cand = os.path.join(search_d, f"{safe_id}{ext}")
                if not os.path.exists(art_cand):
                    art_cand = os.path.join(search_d, f"{base_name}{ext}")
                if os.path.exists(art_cand) and os.path.getsize(art_cand) > 500:
                    artwork = art_cand
                    break
            if artwork and os.path.exists(artwork):
                break

    # 7. Folder artwork fallback
    if not artwork or not os.path.exists(artwork) or artwork == "album_art.png":
        folder_art = find_folder_artwork(os.path.dirname(abs_path))
        if folder_art:
            artwork = folder_art
        else:
            artwork = "album_art.png"

    # 8. Accurately parse duration if still unknown
    if duration <= 0:
        duration = parse_audio_duration(abs_path)
    if duration <= 0 and file_size > 0:
        # Fallback only if header parsing fails
        duration = 180

    return {
        "video_id": safe_id,
        "title": final_title,
        "artist": final_artist,
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
                            norm_p = os.path.normcase(abs_p)
                            if norm_p not in seen_paths:
                                seen_paths.add(norm_p)
                                meta = extract_local_audio_metadata(abs_p, cache_dir=cache_dir)
                                tracks.append(meta)
                                if limit and len(tracks) >= limit:
                                    return tracks
        except Exception:
            continue

    return tracks
