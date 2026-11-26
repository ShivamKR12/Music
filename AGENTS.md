# AGENTS.md

Working target: **`KivyMusicApp/`** — a Kivy/KivyMD 2.0 mobile music app (YouTube/Spotify/JioSaavn streaming + local library). The repo root holds other independent subprojects (`music_app/`, `app/`, `TKinter-music-player/`, root `template*.py` experiments) that are **out of scope** unless explicitly asked. No CI, linter, formatter, or pytest config exists; verification is the headless suite below.

## History & context (outside the repo)
- `C:\Users\Shivam\.gemini\antigravity\brain\3fa220f8-2d51-4ed4-9907-ad9bbebdaeb5\` — prior-session work history: `plan.md` (milestone-by-milestone changelog, Milestones 1–4.9 completed, Milestone 5 "export to music_app" never done), ~24 dated per-topic reports, and hundreds of `verified_*.png` visual captures. Check here before re-deriving why something is the way it is.
- **Desktop mode was implemented and then reverted** (commit `refactor(ui): revert to mobile-only UI/UX mode`). The app is intentionally mobile-only (360x640); old desktop-era reports/screenshots and any stray desktop references are superseded.
- **SimpMusic (`D:\SimpMusic`) is the design baseline** — recent work targets SimpMusic M3 Expressive UI parity. Services currently *implemented* at varying maturity levels include `autoeq_service.py` (EQ profiles table; PCM DSP filter path not yet wired on Android or `ffpyplayer`), `discord_rpc_service.py` (desktop IPC only), `audio_engine.py` (single-player volume fade-out on end + metadata pre-fetch, not yet dual-player PCM crossfade), `sponsorblock_service.py`, and `listen_together_service.py` (LAN TCP socket prototype). Comparison doc: `kivy_music_app_vs_simpmusic_comparison.md` in the history dir.

## Mandatory reading & permanent engineering discipline
- `GEMINI.md` (repo root) — binding rules for this app: read vendored API docs before touching Kivy/KivyMD/yt-dlp code, MVC/repository separation, never block the Kivy UI thread, UI/threading/data invariants (§6–§19), and **Production Engineering & Verification Standards (§20–§25)**:
  - Always distinguish **Designed** vs **Implemented** vs **Verified** in code, docs, and status reports.
  - Report verification strictly across the **4 test tiers** (**Unit**, **Integration/Headless**, **Device**, **Performance Telemetry**); never treat `KIVY_HEADLESS=1` mocked passes as proof of real audio decoding, DSP, or Android background lifecycle.
  - Follow the **8-Priority Execution Order** (Audio/DSP pipeline -> Progressive buffering -> YouTube extraction resilience -> Recommendation math & contracts -> Dedicated SQLite DB Worker -> Android native media lifecycle -> Device & performance telemetry -> Modularizing `main.py`).

## Architecture (`KivyMusicApp/`)
- `main.py` is a ~5.4k-line monolith holding `MusicApp(MDApp)`, startup, navigation, theming, and much screen logic — avoid growing it further; refactor incrementally into coordinators (`GEMINI.md` §3 & §25). It loads `views/main.kv`, which `#:include`s 20 screen `.kv` files from `views/screens/`.
- Screen Python classes live in `views/screens.py` (mostly `pass` stubs with a few properties); shared custom widgets (Directional horizontal scroll, LazyScreenManager, LyricsScrollView, TrackListItem, PassiveTrailingCheckbox, MarqueeLabel, YouTubeLoadingCircle, PlayerTimelineSlider) are in `views/components.py`.
- Playback state/queue: `controllers/player_controller.py`.
- `services/`: `audio_engine.py`, `lyrics_service.py`, `sponsorblock_service.py`, `autoeq_service.py`, `discord_rpc_service.py`, `listen_together_service.py`, `recommendation_engine.py`, `logger.py`; multi-source providers `youtube_provider.py` / `spotify_provider.py` (metadata scraping only, resolved via JioSaavn/YouTube) / `jiosaavn_provider.py` behind `music_provider_router.py` (`music_provider_base.py`).
- `models/database.py`: SQLite currently using a thread-shared connection (`check_same_thread=False`) guarded by `DB_LOCK` (target architecture: dedicated DB worker + WAL + FK enforcement per `GEMINI.md` §14). Desktop DB is `KivyMusicApp/music_app.db`; Android resolves `user_data_dir`. `track_model.py` must keep `from_dict()`/`to_dict()` for thread/DB serialization.
- `utils/`: `theme_utils.py` (dynamic palette from artwork — heavy, debounce per `GEMINI.md` §10), `media_utils.py`, `local_audio_utils.py`.

## Commands
- Run: `cd KivyMusicApp && python main.py` (desktop preview uses 360x640 reference viewport; Android layouts must remain constraint-based/scrollable for varying aspect ratios & insets).
- Tests are standalone scripts, not pytest. Each sets `KIVY_HEADLESS=1` and `sys.path` itself:
  - Single: `cd KivyMusicApp && python tests/test_lyrics_engine_and_math.py` (19 suites configured in `tests/run_all_tests.py`)
  - Full headless battery: `cd KivyMusicApp && python tests/run_all_tests.py` — runs each module in an isolated subprocess; exits nonzero on any failure (verifies logic, DB queries & UI geometry only — supplement with real audio, network & `adb` device checks).
- Install: `pip install -r requirements.txt` (repo root; Python 3.13). `ffmpeg` on PATH for desktop audio handling.
- Android build (Linux/WSL only): `cd KivyMusicApp && buildozer android debug`. `buildozer.spec` configures custom `kivymd` / `materialyoucolor` recipes, API 33 / min API 21, permissions `INTERNET`, `ACCESS_NETWORK_STATE`, `FOREGROUND_SERVICE`, `FOREGROUND_SERVICE_MEDIA_PLAYBACK`, `WAKE_LOCK`, `READ_EXTERNAL_STORAGE`, `WRITE_EXTERNAL_STORAGE`, `READ_MEDIA_AUDIO`, `VIBRATE`. (Note: native Python-for-Android `ForegroundService` / `MediaSession` runtime wiring is not yet implemented.)

## Gotchas
- Code targets the **KivyMD 2.0 API** (`MDButton`/`MDButtonText`, `style="text"`). Ignore the stale `kivymd>=1.1.1` floor in `requirements.txt` — 1.x component names/styles won't match.
- `main.py` has behavior branches on `KIVY_HEADLESS=1`: instant startup warmup, no transition timers, no background network polling. Tests rely on these paths; don't remove them when "simplifying" startup.
- After any change, verify according to the 4-tier discipline in `GEMINI.md` §11 & §20–§25 (`tests/run_all_tests.py` covers headless integration & UI geometry; real audio/DSP, extraction, and Android lifecycle require device/runtime verification). `GEMINI.md` §6–§13 defines core UI/thread invariants (no widget/property changes off the main thread — marshal with `Clock.schedule_once`; hidden overlays must be `disabled`, not just transparent; explicit bar heights, no `minimum_height`).
- `cache/` is the live yt-dlp download cache (`*.mp3`, thumbnails, `*.json`, `.part` files, `.lrc` lyrics) — not app code; the app does real network downloads by design (GEMINI.md §12 forbids mock content).
- No bundled `fonts/` dir despite the candidate list in `main.py` — `resolve_and_register_system_fonts()` falls back to OS fonts (e.g. `segoeui.ttf` on Windows).
- Commits follow Conventional Commits with scopes, e.g. `feat(theming):`, `refactor(ui):`, `test(desktop):`.
