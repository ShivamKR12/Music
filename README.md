# Python Music Players & Mobile Streaming Suite

A collection of cross-platform and desktop music player applications developed in Python, featuring modern Material Design mobile players built with Kivy / KivyMD, online streaming via `yt-dlp`, classic desktop Tkinter UI, and Panda3D audio experiments.

## 🎵 Subprojects Overview

### 1. Kivy Mobile Music App (`KivyMusicApp/`)
A mobile-ready music player application built using **Kivy** and **KivyMD (v2)**.
- Features modern Material Design 3 components, bottom sheets, file manager, playlist drawer, and playback controls.
- Configured with `buildozer.spec` for compilation into an Android `.apk`.
- Modular MVC structure (`controllers/`, `models/`, `views/`, `utils/`).
- **Run**:
  ```bash
  cd KivyMusicApp
  python main.py
  ```

### 2. Music Streaming App (`music_app/`)
An online and local audio player featuring:
- Integration with `yt-dlp` for streaming audio extraction and caching.
- SQLite-backed audio tracks and playlist management.
- KivyMD UI with theme customizers and documentation scrapers (`get_kivy_api.py`, `get_kivymd_api.py`, `get_ytdlp_api.py`).
- **Run**:
  ```bash
  cd music_app
  python main.py
  ```

### 3. Modular App Architecture (`app/`)
A clean architecture implementation dividing audio management into:
- `download`: Background asynchronous fetching
- `library`: Audio indexing and collection management
- `player`: Playback controller and state
- `ui`: Modular user interface views
- **Run**:
  ```bash
  python -m app.main
  ```

### 4. Tkinter Desktop Player (`TKinter-music-player/`)
A lightweight, classic desktop audio player built using standard Python `tkinter` and `pygame`.
- Play, pause, skip, and track selection.
- Bundled with a PyInstaller `.spec` file for standalone executable builds.
- **Run**:
  ```bash
  cd TKinter-music-player
  python TKinter-music-player.py
  ```

### 5. Panda3D Audio Player (`panda3D-music-player.py`)
An audio playback experiment utilizing the Panda3D game engine's positional/3D audio pipeline.
- **Run**:
  ```bash
  python panda3D-music-player.py
  ```

### 6. Development Templates (`template.py` - `template6.py`)
Iterative UI prototypes and KivyMD layout experiments exploring carousels, responsive layouts, and audio visualizers.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+ installed.
- Optional: `ffmpeg` installed on your system PATH for full audio decoding and conversion.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ShivamKR12/Music.git
   cd Music
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux / macOS:
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### 📱 Android Build (Buildozer)

To compile `KivyMusicApp` into an Android APK (requires Linux or WSL):
```bash
cd KivyMusicApp
buildozer android debug
```

---

## 🛠️ Tech Stack

- **Frameworks**: Kivy, KivyMD (Material Design)
- **Audio & Media**: yt-dlp, FFmpeg, ffpyplayer, Pygame, Panda3D
- **Packaging**: Buildozer (Android), PyInstaller (Windows / Linux)
