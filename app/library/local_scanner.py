from pathlib import Path
from .metadata import Song

AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".flac", ".opus", ".m4a"}

def scan_folder(folder: str):
    print("scan_folder called !")
    songs = []
    root = Path(folder)
    print("root is :", root)

    if root.is_file():
        if root.suffix.lower() in AUDIO_EXTS:
            return [Song(
                title=root.stem,
                file_path=str(root),
                source="local"
            )]
        return []

    if root.is_dir():
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in AUDIO_EXTS:
                songs.append(
                    Song(
                        title=path.stem,
                        file_path=str(path),
                        source="local"
                    )
                )

    print("songs in the songs list are :", songs)
    return songs
