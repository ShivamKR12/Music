"""
Audio Engine & Playback Coordinator.

Coordinates multi-backend playback cleanly without UI-thread blocking:
- Desktop PCM Pipeline: DecoderManager -> DSPPipeline (10-band RBJ EQ, Reverb,
  Dual-Deck Equal-Power Crossfade, Soft-Clip Limiter) -> SDL2PCMOutput / NullPCMOutput.
- Android Native Path: Kivy SoundLoader (SoundAndroidPlayer) + AndroidAudioEffectBridge
  (pyjnius android.media.audiofx.Equalizer / PresetReverb).
- Progressive Streaming & Caching: Delegated to BufferManager (download bytes,
  playable seconds, buffer safety ahead of playhead, atomic .part -> final promotion).
"""

import json
import os
import re
import shutil
import socket
import threading
import time
import urllib.request
from typing import Any, Callable, Dict, Optional

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.utils import platform

from services.android_audio_fx import AndroidAudioEffectBridge
from services.audio_output import BasePCMOutput, create_pcm_output
from services.buffer_manager import BufferManager, BufferMetrics, BufferState, is_valid_audio_header
from services.decoder_manager import BasePCMDecoder, DecoderManager, probe_duration_seconds
from services.dsp_pipeline import DSPPipeline, ensure_scipy_loaded_async, mix_crossfade
from services.logger import get_logger
from services.sponsorblock_service import SponsorBlockService
from services.telemetry_service import get_telemetry
from services.youtube_extractor import (
    YouTubeExtractionError,
    YtdlpLogBridge,
    SilentLogger,
    get_youtube_extractor,
    is_stream_url_expired,
    redact_sensitive_text,
)

logger = get_logger("AudioEngine")

# Backward-compatible aliases routed to unified redacting extractor bridge
_redact_url = redact_sensitive_text
YtdlpEngineLogger = YtdlpLogBridge

# Register native Android audio provider ahead of SDL2 when running on Android
if platform == "android":
    try:
        from kivy.core.audio.audio_android import SoundAndroidPlayer
        SoundLoader.register(SoundAndroidPlayer)
        SoundLoader._classes = [SoundAndroidPlayer] + [
            cls for cls in SoundLoader._classes if cls is not SoundAndroidPlayer
        ]
        logger.info("Prioritized native SoundAndroidPlayer ahead of SDL2 for Android")
    except Exception as _e:
        logger.error("Failed to register SoundAndroidPlayer: %s", _e)


def get_cache_dir() -> str:
    from kivy.app import App
    app = App.get_running_app()
    if platform == "android" and app:
        path = os.path.join(app.user_data_dir, "cache")
    else:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache")
    os.makedirs(path, exist_ok=True)
    return path


def extract_video_id(url: str) -> str:
    """Extract 11-char YouTube video ID or normalized track identifier."""
    if not url:
        return ""
    if len(url) == 11 and not ("/" in url or "=" in url):
        return url
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    cleaned = re.sub(r"[^a-zA-Z0-9_-]", "", url)
    return cleaned[:11] if cleaned else "unknown"


class _PCMDeckHandle:
    """
    Lightweight Sound-compatible facade wrapping an active PCM decoder + AudioOutput.
    Preserves `engine.player` contract across controllers and headless verification tests.
    """

    def __init__(self, engine: "AudioEngine", decoder: BasePCMDecoder, info: dict, source: str):
        self._engine = engine
        self.decoder = decoder
        self.info = dict(info or {})
        self.source = source
        self.state = "play"
        self._state = "playing"
        self.length = float(decoder.duration or self.info.get("duration") or 0.0)

    @property
    def volume(self) -> float:
        return self._engine.volume

    @volume.setter
    def volume(self, value: float) -> None:
        self._engine.volume = max(0.0, min(1.0, float(value)))

    def play(self) -> None:
        self._engine.unpause()

    def stop(self) -> None:
        self.state = "stop"
        self._state = "paused"

    def unload(self) -> None:
        try:
            self.decoder.close()
        except Exception:
            pass

    def seek(self, position: float) -> None:
        self._engine.seek(position)

    def get_pos(self) -> float:
        return float(self._engine.elapsed)


class AudioEngine:
    """
    Non-blocking multimedia playback engine coordinating:
    - DecoderManager (FFmpeg & native WAV -> unified 44.1 kHz f32le stereo PCM)
    - DSPPipeline (10-band RBJ biquad EQ, spatial reverb, cos/sin crossfade, soft limiter)
    - AudioOutput (SDL2 hardware ring queue / NullPCMOutput in headless runs)
    - Android fallback (SoundAndroidPlayer + AudioEffect bridge)
    - BufferManager (stateful HTTP/cache downloader & playable safety telemetry)
    """

    CHUNK_FRAMES = 4096
    TARGET_HW_BUFFER_SEC = 0.22

    def __init__(self):
        self.player = None
        self.elapsed = 0.0
        self.duration = 0.0
        self.last_tick = None
        self.paused = False
        self.loading = False
        self.current_info: Optional[dict] = None
        self.current_path: Optional[str] = None
        self.repeat_one = False
        self._has_started_playing = False
        self.volume = 1.0
        self.muted = False
        self._is_ducked = False
        self._duck_factor = 1.0
        self.eq_bands = [0.0] * 10
        self.eq_reverb = False
        self.crossfade_duration = 0.0
        self._is_crossfading = False
        self._crossfade_prepare_sent = False
        self._crossfade_start_time = 0.0
        self.sponsorblock_enabled = True
        self.sponsorblock_service = SponsorBlockService()

        # Subsystems
        self.dsp = DSPPipeline(sample_rate=44100, channels=2)
        # Warm the optional vectorized DSP backend after the UI is interactive so
        # `scipy.signal` never delays startup or the first audio chunk.
        if os.environ.get("KIVY_HEADLESS") != "1" and platform in ("win", "linux", "macosx"):
            try:
                Clock.schedule_once(lambda dt: ensure_scipy_loaded_async(), 2.0)
            except Exception:
                pass
        self.buffer_manager = BufferManager(min_buffer_seconds=3.5)
        self._android_fx = AndroidAudioEffectBridge()
        self._pcm_output: Optional[BasePCMOutput] = None
        self._pcm_deck_a: Optional[_PCMDeckHandle] = None
        self._pcm_deck_b: Optional[_PCMDeckHandle] = None
        self._pcm_base_time = 0.0
        self._using_pcm_pipeline = False
        self._telemetry = get_telemetry()
        self._active_play_token: Optional[float] = None
        self._buffer_stream_seq: int = 1

        # Decoupled UI Callbacks
        self.on_time_update: Optional[Callable[[float, float], None]] = None
        self.on_track_end: Optional[Callable[[], None]] = None
        self.on_artwork_loaded: Optional[Callable[[str], None]] = None
        self.on_loading: Optional[Callable[[bool], None]] = None
        self.on_download_progress: Optional[Callable[[str], None]] = None
        self.on_buffer_update: Optional[Callable[[float], None]] = None
        self.on_buffer_metrics: Optional[Callable[[BufferMetrics], None]] = None
        self.buffer_progress = 0.0
        self.on_error: Optional[Callable[[str], None]] = None
        self.on_track_loaded: Optional[Callable[[str, dict], None]] = None
        self.on_sponsorblock_skipped: Optional[Callable[[float, float], None]] = None
        self.on_crossfade_trigger: Optional[Callable[[], None]] = None
        self.on_crossfade_track_advanced: Optional[Callable[[dict], None]] = None

        self.lock = threading.RLock()
        self.cancel_event = threading.Event()
        self._render_stop_event = threading.Event()
        self._render_thread: Optional[threading.Thread] = None

        self.buffer_manager.on_metrics_update = self._handle_buffer_metrics

    def _handle_buffer_metrics(self, metrics: BufferMetrics) -> None:
        self.buffer_progress = metrics.download_progress
        if metrics.state == BufferState.PROBING:
            self._buffer_stream_seq += 1
        self._telemetry.record_buffer_metrics(
            stream_key=(id(self.buffer_manager) ^ self._buffer_stream_seq),
            stall_count=metrics.stall_count,
            total_stall_seconds=metrics.total_stall_seconds,
            buffer_safety_seconds=metrics.buffer_safety_seconds,
            network_bps=metrics.network_bps,
            bytes_downloaded=metrics.bytes_downloaded,
            supports_range=metrics.supports_range,
        )
        if self.on_buffer_update:
            bp = metrics.download_progress
            Clock.schedule_once(lambda dt, val=bp: self.on_buffer_update(val), 0)
        if self.on_buffer_metrics:
            Clock.schedule_once(lambda dt, m=metrics: self.on_buffer_metrics(m), 0)

    def _cache_path_from_id(self, video_id: str) -> str:
        """Locate any existing cached audio file for a given video ID."""
        base = os.path.join(get_cache_dir(), video_id)
        for ext in (".mp3", ".m4a", ".webm", ".opus", ".ogg", ".flac", ".wav", ".mp4", ".mkv"):
            path = base + ext
            if os.path.exists(path) and os.path.isfile(path) and os.path.getsize(path) >= 1024:
                return path
        return ""

    # =========================================================================
    # Public Control Entrypoints (All UI-Thread Safe)
    # =========================================================================
    def resolve_and_play_track(self, track_dict: dict) -> bool:
        """
        Asynchronous track entrypoint: resolves MusicProviderRouter stream URL off the
        UI thread, checks local cache first, and initiates playback without freezing UI.
        """
        if not track_dict:
            return False

        self._active_play_token = self._telemetry.begin_play_request(
            track_dict.get("title") or track_dict.get("video_id") or track_dict.get("id") or ""
        )

        local_path = track_dict.get("local_path") or ""
        meta = {
            "id": track_dict.get("video_id", "") or track_dict.get("id", ""),
            "title": track_dict.get("title", "Unknown"),
            "artist": track_dict.get("artist", "Unknown Artist"),
            "duration": int(track_dict.get("duration") or 0),
            "artwork": track_dict.get("artwork") or track_dict.get("album_art") or "",
            "source": track_dict.get("source", "youtube"),
        }
        if local_path and os.path.exists(local_path) and os.path.isfile(local_path):
            return self.start_play(local_path, meta, _preserve_token=True)

        # Spawn async worker for cache lookup + stream resolution + playback
        with self.lock:
            self.cancel_event.set()
            self.cleanup_player()
            self.loading = True
            self.cancel_event = threading.Event()
            current_cancel = self.cancel_event

        Clock.schedule_once(lambda dt: self._set_loading(True), 0)

        def _worker():
            try:
                vid = meta["id"]
                cached = self._cache_path_from_id(vid) if vid else ""
                if cached and not current_cancel.is_set():
                    self._download_and_play(cached, current_cancel, meta)
                    return

                target_src = track_dict.get("stream_url") or ""
                if target_src and is_stream_url_expired(target_src):
                    logger.info("Cached stream_url expired for %s; re-resolving fresh URL", meta["id"])
                    target_src = ""
                if not target_src:
                    try:
                        from services.music_provider_router import MusicProviderRouter
                        resolved = MusicProviderRouter().resolve_stream(track_dict)
                        target_src = (resolved or {}).get("url") or track_dict.get("url", "")
                        if resolved and resolved.get("matched_video_id") and not meta["id"]:
                            meta["id"] = resolved["matched_video_id"]
                    except Exception as exc:
                        logger.warning("Stream resolution fallback for %s: %s", meta["id"], redact_sensitive_text(exc))
                        target_src = track_dict.get("url", "")

                if not target_src and meta["id"]:
                    target_src = f"https://www.youtube.com/watch?v={meta['id']}"

                if current_cancel.is_set():
                    return
                if not target_src:
                    raise RuntimeError("No playable URL or local path found for track")

                self._download_and_play(target_src, current_cancel, meta)
            except Exception as exc:
                if not current_cancel.is_set():
                    safe_msg = redact_sensitive_text(exc)
                    logger.error("resolve_and_play_track error: %s", safe_msg)
                    if self.on_error:
                        Clock.schedule_once(lambda dt, m=safe_msg: self.on_error(m), 0)
                Clock.schedule_once(lambda dt: self._set_loading(False), 0)

        threading.Thread(target=_worker, daemon=True, name="ResolvePlayWorker").start()
        return True

    def start_play(self, url_or_path: str, track_info: Optional[dict] = None, _preserve_token: bool = False) -> bool:
        """Initiate playback for a local file or remote YouTube/HTTP track."""
        if not url_or_path:
            return False

        if not _preserve_token:
            label = (track_info or {}).get("title") or os.path.basename(str(url_or_path))
            self._active_play_token = self._telemetry.begin_play_request(label)

        # 1. Existing local audio file -> open immediately
        if os.path.exists(url_or_path) and os.path.isfile(url_or_path):
            if not is_valid_audio_header(url_or_path):
                logger.warning("Rejected invalid/corrupt audio file: %s", url_or_path)
                if self.on_error:
                    bn = os.path.basename(url_or_path)
                    Clock.schedule_once(lambda dt: self.on_error(f"Cannot play empty or corrupt file: {bn}"), 0)
                return False
            info = dict(track_info or {"title": os.path.basename(url_or_path), "duration": 0})
            self.cleanup_player()
            self._set_main_thread_info(info, url_or_path)
            self._play_file(url_or_path, info, is_completed_local=True)
            return True

        # 2. Cached local asset check
        video_id = (track_info.get("id") if track_info else "") or extract_video_id(url_or_path)
        if video_id and self.sponsorblock_enabled:
            self.sponsorblock_service.fetch_segments_async(video_id)
        cache_dir = get_cache_dir()
        cached_audio = self._cache_path_from_id(video_id) if video_id else ""
        if cached_audio and os.path.exists(cached_audio) and is_valid_audio_header(cached_audio):
            meta_path = os.path.join(cache_dir, f"{video_id}.json")
            cached_meta = self._load_cached_metadata(meta_path) or {}
            if track_info:
                cached_meta.update(track_info)
            self.cleanup_player()
            self._set_main_thread_info(cached_meta, cached_audio)
            thumb_path = os.path.join(cache_dir, f"{video_id}.jpg")
            art = cached_meta.get("artwork")
            if (not art or not os.path.exists(art)) and os.path.exists(thumb_path):
                art = thumb_path
                cached_meta["artwork"] = art
            if art and os.path.exists(art) and self.on_artwork_loaded:
                Clock.schedule_once(lambda dt, a=art: self.on_artwork_loaded(a), 0)
            self._play_file(cached_audio, cached_meta, is_completed_local=True)
            return True

        # 3. Online stream / YouTube download & progressive streaming
        with self.lock:
            self.cancel_event.set()
            self.cleanup_player()
            self.loading = True
            self.cancel_event = threading.Event()
            current_cancel = self.cancel_event

        threading.Thread(
            target=self._download_and_play,
            args=(url_or_path, current_cancel, track_info),
            daemon=True,
            name="StreamDownloadWorker",
        ).start()
        return True

    def stage_next_deck(self, track_dict: dict) -> None:
        """
        Pre-resolve and stage the upcoming track into Deck B asynchronously so
        dual-deck equal-power crossfade mixes seamlessly when rem_time <= crossfade_duration.
        """
        if not track_dict or platform == "android" or self.crossfade_duration <= 0:
            return
        with self.lock:
            cancel_token = self.cancel_event

        def _stage():
            try:
                if cancel_token.is_set() or not self._using_pcm_pipeline:
                    return
                src = track_dict.get("local_path") or ""
                vid = track_dict.get("video_id") or track_dict.get("id") or ""
                if not (src and os.path.exists(src)):
                    cached = self._cache_path_from_id(vid) if vid else ""
                    if cached:
                        src = cached
                if not src:
                    from services.music_provider_router import MusicProviderRouter
                    resolved = MusicProviderRouter().resolve_stream(track_dict)
                    src = (resolved or {}).get("url") or track_dict.get("url", "")
                if not src or cancel_token.is_set():
                    return

                # Re-resolve expired or watch URLs for FFmpegPCMDecoder
                if src and is_stream_url_expired(src) and vid:
                    src = f"https://www.youtube.com/watch?v={vid}"
                if ("youtube.com/" in src or "youtu.be/" in src) and not os.path.exists(src):
                    direct = self._extract_youtube_direct_stream(src, cancel_event=cancel_token)
                    if direct and direct.get("url"):
                        src = direct["url"]

                if cancel_token.is_set():
                    return
                dec = DecoderManager.open_stream(src, start_seconds=0.0, duration=float(track_dict.get("duration") or 0))
                if not dec:
                    return
                with self.lock:
                    if cancel_token.is_set() or not self._using_pcm_pipeline:
                        dec.close()
                        return
                    if self._pcm_deck_b:
                        self._pcm_deck_b.unload()
                    self._pcm_deck_b = _PCMDeckHandle(self, dec, track_dict, src)
                    logger.info("Staged crossfade Deck B: %s", track_dict.get("title", "Unknown"))
            except Exception as exc:
                logger.debug("Crossfade Deck B staging skipped: %s", redact_sensitive_text(exc))

        threading.Thread(target=_stage, daemon=True, name="CrossfadeStageWorker").start()

    def cleanup_player(self, cancel_workers: bool = False) -> None:
        """Cleanly halt UI timers, render worker threads, decoders, SDL2 hardware, and SoundLoader."""
        if cancel_workers:
            with self.lock:
                self.cancel_event.set()
        Clock.unschedule(self._update)

        with self.lock:
            self._render_stop_event.set()
            r_thread = self._render_thread
            self._render_thread = None

        if r_thread and r_thread.is_alive() and threading.current_thread() is not r_thread:
            r_thread.join(timeout=0.5)

        with self.lock:
            self._android_fx.release()
            if self._pcm_deck_a:
                self._pcm_deck_a.unload()
                self._pcm_deck_a = None
            if self._pcm_deck_b:
                self._pcm_deck_b.unload()
                self._pcm_deck_b = None
            if self._pcm_output:
                try:
                    self._pcm_output.close()
                except Exception:
                    pass
                self._pcm_output = None

            if self.player and not isinstance(self.player, _PCMDeckHandle):
                try:
                    self.player.stop()
                except Exception:
                    pass
                try:
                    if hasattr(self.player, "unload"):
                        self.player.unload()
                except Exception:
                    pass

            self.player = None
            self._using_pcm_pipeline = False
            self.elapsed = 0.0
            self.duration = 0.0
            self._pcm_base_time = 0.0
            self.last_tick = None
            self.paused = False
            self._has_started_playing = False
            self._is_crossfading = False
            self._crossfade_prepare_sent = False
            self._crossfade_start_time = 0.0
            self.dsp.reset_state()

    def _set_loading(self, state: bool) -> None:
        self.loading = state
        if self.on_loading:
            self.on_loading(state)

    # =========================================================================
    # Stream Extraction, Progressive Streaming & Background Caching
    # =========================================================================
    def _extract_youtube_direct_stream(
        self,
        watch_url: str,
        force_refresh: bool = False,
        cancel_event: Optional[threading.Event] = None,
    ) -> Optional[dict]:
        """Extract validated direct audio stream URL + expiry via hardened YouTubeExtractor."""
        return get_youtube_extractor().extract_stream(
            watch_url,
            force_refresh=force_refresh,
            cancel_event=cancel_event or self.cancel_event,
        )

    def _download_and_play(self, target: str, cancel_event: threading.Event, user_info=None):
        try:
            Clock.schedule_once(lambda dt: self._set_loading(True), 0)
            track_id = (user_info.get("id") or user_info.get("video_id")) if user_info else ""
            if not track_id:
                track_id = extract_video_id(target)
            video_id = track_id

            # 0. Local path passed directly into worker
            if os.path.exists(target) and os.path.isfile(target) and is_valid_audio_header(target):
                if cancel_event.is_set():
                    return
                clean_info = dict(user_info or {"id": video_id, "title": os.path.basename(target), "duration": 0})
                Clock.schedule_once(lambda dt: self._set_main_thread_info(clean_info, target), 0)
                Clock.schedule_once(lambda dt: self._play_file(target, clean_info, is_completed_local=True), 0)
                Clock.schedule_once(lambda dt: self._set_loading(False), 0)
                return

            cache_dir = get_cache_dir()
            meta_path = os.path.join(cache_dir, f"{video_id}.json")
            cached_audio = self._cache_path_from_id(video_id)

            # 1. Local cache hit
            if cached_audio and os.path.exists(cached_audio) and is_valid_audio_header(cached_audio):
                cached_meta = self._load_cached_metadata(meta_path) or {}
                if user_info:
                    cached_meta.update(user_info)
                if cancel_event.is_set():
                    return
                Clock.schedule_once(lambda dt: self._set_main_thread_info(cached_meta, cached_audio), 0)
                if cached_meta.get("artwork") and os.path.exists(cached_meta["artwork"]) and self.on_artwork_loaded:
                    Clock.schedule_once(lambda dt, a=cached_meta["artwork"]: self.on_artwork_loaded(a), 0)
                Clock.schedule_once(lambda dt: self._play_file(cached_audio, cached_meta, is_completed_local=True), 0)
                Clock.schedule_once(lambda dt: self._set_loading(False), 0)
                return

            if cancel_event.is_set():
                return

            # 2. Direct CDN HTTP stream (JioSaavn or already resolved CDN URL)
            is_yt_watch = ("youtube.com/" in target or "youtu.be/" in target)
            is_direct_http = target.startswith(("http://", "https://")) and not is_yt_watch
            if is_direct_http:
                self._stream_direct_http(target, video_id, cancel_event, user_info)
                return

            # 3. YouTube watch URL / bare ID extraction (with expiry + refresh hooks)
            full_url = target if is_yt_watch else f"https://www.youtube.com/watch?v={video_id}"
            extracted = self._extract_youtube_direct_stream(
                full_url, force_refresh=False, cancel_event=cancel_event
            )
            if cancel_event.is_set():
                return
            if not extracted or not extracted.get("url"):
                raise YouTubeExtractionError(
                    "NO_VALID_FORMAT",
                    "Could not extract playable audio format from YouTube",
                )

            clean_info = {
                "id": video_id,
                "title": extracted.get("title") or (user_info.get("title", "Unknown") if user_info else "Unknown"),
                "artist": extracted.get("artist") or (user_info.get("artist", "") if user_info else ""),
                "duration": int(extracted.get("duration") or (user_info.get("duration", 0) if user_info else 0)),
                "artwork": "",
                "watch_url": full_url,
                "expires_at": float(extracted.get("expires_at") or 0.0),
                "source": "youtube",
            }

            thumb_url = extracted.get("thumbnail") or (user_info.get("artwork") if user_info else "")
            thumb_path = os.path.join(cache_dir, f"{video_id}.jpg")
            if thumb_url and thumb_url.startswith("http") and not os.path.exists(thumb_path):
                self._download_thumbnail(thumb_url, thumb_path)
            if os.path.exists(thumb_path):
                clean_info["artwork"] = thumb_path

            if cancel_event.is_set():
                return

            stream_url = extracted["url"]
            stream_headers = dict(extracted.get("http_headers") or {})
            used_tier = str(extracted.get("client_tier") or "")
            failed_tiers = []
            ext = extracted.get("ext", "m4a")
            bitrate_bps = max(32000, int(extracted.get("abr", 128)) * 1000)

            def _refresh_yt_stream() -> Optional[str]:
                nonlocal used_tier
                if cancel_event.is_set():
                    return None
                if used_tier and used_tier not in failed_tiers:
                    failed_tiers.append(used_tier)
                try:
                    fresh = get_youtube_extractor().extract_stream(
                        full_url,
                        force_refresh=True,
                        cancel_event=cancel_event or self.cancel_event,
                        excluded_tiers=failed_tiers,
                    )
                    if fresh and fresh.get("url"):
                        used_tier = str(fresh.get("client_tier") or "")
                        clean_info["expires_at"] = float(fresh.get("expires_at") or 0.0)
                        if fresh.get("http_headers"):
                            stream_headers.clear()
                            stream_headers.update(fresh["http_headers"])
                        return fresh["url"]
                except Exception as ref_err:
                    logger.warning("YouTube stream refresh failed (%s): %s", video_id, redact_sensitive_text(ref_err))
                return None

            Clock.schedule_once(lambda dt: self._set_main_thread_info(clean_info, stream_url), 0)
            if clean_info.get("artwork") and self.on_artwork_loaded:
                Clock.schedule_once(lambda dt, a=clean_info["artwork"]: self.on_artwork_loaded(a), 0)

            # Desktop PCM path: decode directly from signed HTTP stream while BufferManager caches cleanly offline!
            if platform != "android" and DecoderManager.has_ffmpeg():
                Clock.schedule_once(lambda dt: self._play_file(stream_url, clean_info, is_completed_local=False), 0)
                Clock.schedule_once(lambda dt: self._set_loading(False), 0)

                final_ext = ext if ext in ("m4a", "mp3", "webm", "opus", "ogg") else "m4a"
                final_cache_path = os.path.join(cache_dir, f"{video_id}.{final_ext}")

                def _on_dl_done(fpath: str, metrics: BufferMetrics):
                    self._save_cached_metadata(meta_path, clean_info)
                    self._notify_cache_completed(video_id, fpath, clean_info)

                self.buffer_manager.download_http_stream(
                    stream_url=stream_url,
                    final_path=final_cache_path,
                    cancel_event=cancel_event,
                    duration_hint=clean_info["duration"],
                    bitrate_bps=bitrate_bps,
                    http_headers=stream_headers,
                    on_completed=_on_dl_done,
                    on_refresh_stream=_refresh_yt_stream,
                    on_error=lambda msg: logger.warning("Background cache failed (%s): %s", video_id, redact_sensitive_text(msg)),
                )
            else:
                # Android / no-ffmpeg path: download atomically via BufferManager, play cleanly on ready/finish
                final_ext = ext if ext in ("m4a", "mp4", "mp3", "ogg", "wav") else "m4a"
                final_cache_path = os.path.join(cache_dir, f"{video_id}.{final_ext}")
                started = [False]

                def _on_done(fpath: str, metrics: BufferMetrics):
                    self._save_cached_metadata(meta_path, clean_info)
                    self._notify_cache_completed(video_id, fpath, clean_info)
                    if not started[0] and not cancel_event.is_set():
                        started[0] = True
                        Clock.schedule_once(lambda dt: self._play_file(fpath, clean_info, is_completed_local=True), 0)
                        Clock.schedule_once(lambda dt: self._set_loading(False), 0)

                def _on_err(msg: str):
                    if not cancel_event.is_set() and self.on_error:
                        safe_m = redact_sensitive_text(msg)
                        Clock.schedule_once(lambda dt, m=safe_m: self.on_error(m), 0)
                    Clock.schedule_once(lambda dt: self._set_loading(False), 0)

                self.buffer_manager.download_http_stream(
                    stream_url=stream_url,
                    final_path=final_cache_path,
                    cancel_event=cancel_event,
                    duration_hint=clean_info["duration"],
                    bitrate_bps=bitrate_bps,
                    http_headers=stream_headers,
                    on_completed=_on_done,
                    on_error=_on_err,
                    on_refresh_stream=_refresh_yt_stream,
                )

        except InterruptedError:
            pass
        except Exception as exc:
            if not cancel_event.is_set():
                logger.error("AudioEngine stream/playback error: %s", _redact_url(str(exc)))
                if self.on_error:
                    err_str = _redact_url(str(exc))
                    Clock.schedule_once(lambda dt, e=err_str: self.on_error(e), 0)
            Clock.schedule_once(lambda dt: self._set_loading(False), 0)
        finally:
            with self.lock:
                if not cancel_event.is_set():
                    Clock.schedule_once(lambda dt: self._set_loading(False), 0)

    def _stream_direct_http(self, stream_url: str, track_id: str, cancel_event: threading.Event, user_info=None):
        """Play direct HTTP CDN audio stream via PCM decoder + BufferManager background caching."""
        try:
            cache_dir = get_cache_dir()
            ext = ".mp4" if ".mp4" in stream_url else (".m4a" if ".m4a" in stream_url else ".mp3")
            target_path = os.path.join(cache_dir, f"{track_id}{ext}")
            meta_path = os.path.join(cache_dir, f"{track_id}.json")

            clean_info = {
                "id": track_id,
                "title": user_info.get("title", "Unknown Title") if user_info else "Unknown Title",
                "artist": user_info.get("artist", "Direct Artist") if user_info else "Direct Artist",
                "duration": int(user_info.get("duration", 0) if user_info else 0),
                "artwork": user_info.get("artwork", "") if user_info else "",
            }

            if os.path.exists(target_path) and is_valid_audio_header(target_path):
                cached_meta = self._load_cached_metadata(meta_path) or clean_info
                thumb_path = os.path.join(cache_dir, f"{track_id}.jpg")
                if (not cached_meta.get("artwork") or not os.path.exists(str(cached_meta.get("artwork")))) and clean_info["artwork"].startswith("http"):
                    if not os.path.exists(thumb_path):
                        self._download_thumbnail(clean_info["artwork"], thumb_path)
                    if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 0:
                        cached_meta["artwork"] = thumb_path
                if cancel_event.is_set():
                    return
                Clock.schedule_once(lambda dt: self._set_main_thread_info(cached_meta, target_path), 0)
                if cached_meta.get("artwork") and os.path.exists(cached_meta["artwork"]) and self.on_artwork_loaded:
                    Clock.schedule_once(lambda dt, a=cached_meta["artwork"]: self.on_artwork_loaded(a), 0)
                Clock.schedule_once(lambda dt: self._play_file(target_path, cached_meta, is_completed_local=True), 0)
                Clock.schedule_once(lambda dt: self._set_loading(False), 0)
                return

            thumb_url = clean_info.get("artwork")
            thumb_path = os.path.join(cache_dir, f"{track_id}.jpg")
            if thumb_url and thumb_url.startswith("http") and not os.path.exists(thumb_path):
                self._download_thumbnail(thumb_url, thumb_path)
            if os.path.exists(thumb_path):
                clean_info["artwork"] = thumb_path

            if cancel_event.is_set():
                return

            Clock.schedule_once(lambda dt: self._set_main_thread_info(clean_info, target_path), 0)
            if clean_info.get("artwork") and self.on_artwork_loaded:
                Clock.schedule_once(lambda dt, a=clean_info["artwork"]: self.on_artwork_loaded(a), 0)

            def _on_done(fpath: str, metrics: BufferMetrics):
                self._save_cached_metadata(meta_path, clean_info)
                self._notify_cache_completed(track_id, fpath, clean_info)

            if platform != "android" and DecoderManager.has_ffmpeg():
                # Immediate HTTP PCM decode + clean background cache
                Clock.schedule_once(lambda dt: self._play_file(stream_url, clean_info, is_completed_local=False), 0)
                Clock.schedule_once(lambda dt: self._set_loading(False), 0)
                self.buffer_manager.download_http_stream(
                    stream_url=stream_url,
                    final_path=target_path,
                    cancel_event=cancel_event,
                    duration_hint=clean_info["duration"],
                    bitrate_bps=320000,
                    on_completed=_on_done,
                )
            else:
                def _on_done_and_play(fpath: str, metrics: BufferMetrics):
                    _on_done(fpath, metrics)
                    if not cancel_event.is_set():
                        Clock.schedule_once(lambda dt: self._play_file(fpath, clean_info, is_completed_local=True), 0)
                        Clock.schedule_once(lambda dt: self._set_loading(False), 0)

                def _on_err(msg: str):
                    if not cancel_event.is_set() and self.on_error:
                        Clock.schedule_once(lambda dt: self.on_error(msg), 0)
                    Clock.schedule_once(lambda dt: self._set_loading(False), 0)

                self.buffer_manager.download_http_stream(
                    stream_url=stream_url,
                    final_path=target_path,
                    cancel_event=cancel_event,
                    duration_hint=clean_info["duration"],
                    bitrate_bps=320000,
                    on_completed=_on_done_and_play,
                    on_error=_on_err,
                )
        except Exception as exc:
            logger.error("Direct HTTP stream error: %s", _redact_url(str(exc)))
            if self.on_error and not cancel_event.is_set():
                msg = _redact_url(str(exc))
                Clock.schedule_once(lambda dt, m=msg: self.on_error(f"Stream error: {m}"), 0)
        finally:
            Clock.schedule_once(lambda dt: self._set_loading(False), 0)

    def _notify_cache_completed(self, track_id: str, final_path: str, info: dict) -> None:
        """Persist cached path only after full download validation completes."""
        try:
            dur = probe_duration_seconds(final_path, fallback=float(info.get("duration") or 0))
            if dur > 0:
                info["duration"] = int(dur)
            from models.database import update_local_track_path
            update_local_track_path(track_id, final_path, info.get("duration", 0))
        except Exception:
            pass
        if self.on_track_loaded:
            Clock.schedule_once(lambda dt: self.on_track_loaded(final_path, info), 0)

    def _set_main_thread_info(self, info: dict, path: str) -> None:
        self.current_info = info
        self.current_path = path

    # =========================================================================
    # Playback Start: Desktop PCM Pipeline + Android/Fallback SoundLoader
    # =========================================================================
    def _play_file(self, source: str, info: dict, is_completed_local: bool = True) -> None:
        self.cleanup_player()

        is_local = os.path.exists(source) and os.path.isfile(source)
        target_src = os.path.abspath(source) if is_local else source

        if is_local and not is_valid_audio_header(target_src):
            logger.error("File invalid or corrupted: %s", target_src)
            if self.on_error:
                bn = os.path.basename(target_src)
                Clock.schedule_once(lambda dt: self.on_error(f"Corrupt or empty audio file: {bn}"), 0)
            return

        # 1. Preferred Desktop PCM DSP Pipeline
        if platform != "android" and DecoderManager.can_decode_pcm(target_src):
            try:
                dur_hint = float((info or {}).get("duration") or 0.0)
                decoder = DecoderManager.open_stream(target_src, start_seconds=0.0, duration=dur_hint)
                if decoder is not None:
                    self._pcm_output = create_pcm_output(decoder.sample_rate, decoder.channels)
                    self.dsp.set_eq_bands(self.eq_bands, self.eq_reverb)
                    self.dsp.reset_state()

                    self._pcm_deck_a = _PCMDeckHandle(self, decoder, info, target_src)
                    self.player = self._pcm_deck_a
                    self._using_pcm_pipeline = True

                    self.duration = float(decoder.duration or dur_hint or 180.0)
                    if info is not None and self.duration > 0:
                        info["duration"] = int(self.duration)
                    self.elapsed = 0.0
                    self._pcm_base_time = 0.0
                    self.last_tick = None
                    self.paused = False
                    self._has_started_playing = False
                    self._is_crossfading = False
                    self._crossfade_prepare_sent = False
                    self._crossfade_start_time = 0.0

                    self._render_stop_event = threading.Event()
                    self._render_thread = threading.Thread(
                        target=self._pcm_render_loop,
                        args=(self._render_stop_event,),
                        daemon=True,
                        name="AudioPCMRenderWorker",
                    )
                    self._render_thread.start()

                    artwork = info.get("artwork") if info else None
                    if artwork and os.path.exists(artwork) and self.on_artwork_loaded:
                        Clock.schedule_once(lambda dt: self.on_artwork_loaded(artwork), 0)
                    if is_local and is_completed_local and self.on_track_loaded:
                        Clock.schedule_once(lambda dt: self.on_track_loaded(target_src, info), 0)

                    Clock.schedule_interval(self._update, 1.0 / 30.0)
                    return
            except Exception as exc:
                logger.warning("PCM pipeline init fell back to SoundLoader (%s): %s", _redact_url(target_src), exc)
                self.cleanup_player()

        # 2. Android / SoundLoader Fallback
        self._using_pcm_pipeline = False
        self.player = None
        if is_local:
            try:
                self.player = SoundLoader.load(target_src)
            except Exception as load_exc:
                logger.warning("Primary SoundLoader provider failed (%s): %s", os.path.basename(target_src), load_exc)
                ext = target_src.rsplit(".", 1)[-1].lower() if "." in target_src else ""
                for cls in list(SoundLoader._classes[1:]):
                    try:
                        if ext in cls.extensions():
                            self.player = cls(source=target_src)
                            break
                    except Exception:
                        continue
        if self.player:
            self.player.play()
            tok = self._active_play_token
            self._active_play_token = None
            if tok is not None:
                self._telemetry.mark_first_audio(tok, (info or {}).get("title", ""))
            if platform == "android":
                if self._android_fx.attach(self.player):
                    self._android_fx.apply(self.eq_bands, self.eq_reverb)

            file_len = getattr(self.player, "length", 0)
            meta_len = info.get("duration", 0) if info else 0
            self.duration = float(file_len if file_len > 0 else (meta_len if meta_len > 0 else 180))
            if info:
                info["duration"] = int(self.duration)
            self.elapsed = 0.0
            self.last_tick = None
            self.paused = False
            self._has_started_playing = False
            self._is_crossfading = False
            if hasattr(self.player, "volume"):
                self.player.volume = 0.0 if self.muted else self.volume

            artwork = info.get("artwork") if info else None
            if artwork and os.path.exists(artwork) and self.on_artwork_loaded:
                Clock.schedule_once(lambda dt: self.on_artwork_loaded(artwork), 0)
            if is_local and is_completed_local and self.on_track_loaded:
                Clock.schedule_once(lambda dt: self.on_track_loaded(target_src, info), 0)

            Clock.schedule_interval(self._update, 1.0 / 30.0)
        else:
            logger.error("Audio load failed: %s", _redact_url(target_src))
            if self.on_error:
                bn = os.path.basename(target_src) if is_local else "remote stream"
                Clock.schedule_once(lambda dt: self.on_error(f"Failed to load audio: {bn}"), 0)

    # =========================================================================
    # Dedicated PCM Render Worker Loop (DSP + Dual-Deck Crossfade + Output)
    # =========================================================================
    def _pcm_render_loop(self, stop_event: threading.Event) -> None:
        sr = 44100
        chunk_frames = self.CHUNK_FRAMES
        chunk_sec = chunk_frames / float(sr)

        while not stop_event.is_set():
            with self.lock:
                paused = self.paused
                deck_a = self._pcm_deck_a
                deck_b = self._pcm_deck_b
                out = self._pcm_output
                muted = self.muted
                duck_mult = self._duck_factor if self._is_ducked else 1.0
                vol = 0.0 if muted else (self.volume * duck_mult)
                xf_dur = self.crossfade_duration

            if not deck_a or not out or stop_event.is_set():
                break

            if paused:
                time.sleep(0.025)
                continue

            # Maintain tight ~220ms hardware output queue for instant pause/seek/EQ responsiveness
            if out.queued_seconds() >= self.TARGET_HW_BUFFER_SEC:
                time.sleep(0.015)
                continue

            pcm_a = deck_a.decoder.read_frames(chunk_frames)

            # Deck A reached EOF -> promote Deck B seamlessly, recover expired HTTP URL if premature, or trigger track end
            if pcm_a is None or len(pcm_a) == 0:
                if deck_b is not None and not stop_event.is_set():
                    self._promote_crossfade_deck_b(deck_a, deck_b, out)
                    continue
                if self._should_attempt_stream_recovery(deck_a, stop_event):
                    recovered = self._recover_expired_pcm_stream(deck_a, out, stop_event)
                    if recovered:
                        continue
                # Wait until SDL2 finishes draining queued tail frames before signaling EOF
                while not stop_event.is_set() and out.queued_seconds() > 0.02:
                    if self.paused:
                        time.sleep(0.02)
                        continue
                    time.sleep(0.02)
                if not stop_event.is_set():
                    Clock.schedule_once(lambda dt: self._handle_pcm_eof(), 0)
                break

            n_frames = len(pcm_a) if hasattr(pcm_a, "shape") else (len(pcm_a) // 2)
            cur_time = deck_a.decoder.position_frames / float(sr) - (n_frames / float(sr))

            # Dual-Deck Equal-Power Crossfade Mixing
            if (
                xf_dur > 0
                and deck_a.length > (xf_dur + 4.0)
                and deck_b is not None
                and cur_time >= (deck_a.length - xf_dur)
            ):
                xf_start = deck_a.length - xf_dur
                p0 = (cur_time - xf_start) / xf_dur
                p1 = (cur_time + chunk_sec - xf_start) / xf_dur
                pcm_b = deck_b.decoder.read_frames(n_frames)
                if pcm_b is not None and len(pcm_b) > 0:
                    pcm_mixed = mix_crossfade(pcm_a, pcm_b, p0, p1)
                else:
                    # Short tail on Deck B fallback
                    pcm_mixed = pcm_a
            elif (
                xf_dur > 0
                and deck_a.length > (xf_dur + 4.0)
                and deck_b is None
                and cur_time >= (deck_a.length - xf_dur)
            ):
                # Fallback fade-out when Deck B isn't available (e.g., offline single track)
                rem = max(0.0, deck_a.length - cur_time)
                vol = vol * max(0.0, min(1.0, rem / xf_dur))
                pcm_mixed = pcm_a
            else:
                pcm_mixed = pcm_a

            dsp_t0 = time.perf_counter()
            processed = self.dsp.process(pcm_mixed, volume=vol)
            dsp_dt = time.perf_counter() - dsp_t0
            self._telemetry.record_dsp_chunk(dsp_dt, float(n_frames) / float(sr))
            raw_bytes = self._frames_to_bytes(processed)
            if raw_bytes:
                out.write(raw_bytes, n_frames)
                tok = self._active_play_token
                if tok is not None:
                    self._active_play_token = None
                    self._telemetry.mark_first_audio(tok, (deck_a.info or {}).get("title", ""))

    @staticmethod
    def _frames_to_bytes(frames) -> bytes:
        if hasattr(frames, "tobytes"):
            return frames.astype("<f4", copy=False).tobytes()
        import struct
        return struct.pack(f"<{len(frames)}f", *frames)

    def _promote_crossfade_deck_b(self, deck_a: _PCMDeckHandle, deck_b: _PCMDeckHandle, out: BasePCMOutput) -> None:
        """Promote crossfading Deck B to primary Deck A cleanly with zero hardware click."""
        with self.lock:
            b_pos_sec = deck_b.decoder.position_frames / float(deck_b.decoder.sample_rate)
            deck_a.unload()
            self._pcm_deck_a = deck_b
            self._pcm_deck_b = None
            self.player = deck_b
            self.current_info = dict(deck_b.info)
            self.current_path = deck_b.source
            self.duration = float(deck_b.length or deck_b.decoder.duration or 180.0)
            # Align base_time so hardware played_seconds() tracks continuous playhead seamlessly
            self._pcm_base_time = b_pos_sec - out.played_seconds()
            self.elapsed = max(0.0, b_pos_sec - out.queued_seconds())
            self._is_crossfading = False
            self._crossfade_prepare_sent = False
            self._crossfade_start_time = 0.0
            next_info = dict(deck_b.info)

        if self.on_crossfade_track_advanced:
            Clock.schedule_once(lambda dt, ni=next_info: self.on_crossfade_track_advanced(ni), 0)

    def _should_attempt_stream_recovery(self, deck_a: _PCMDeckHandle, stop_event: threading.Event) -> bool:
        """Detect premature termination on an expired or interrupted remote HTTP/YouTube stream."""
        if stop_event.is_set() or not deck_a:
            return False
        src = str(deck_a.source or "")
        if not src.startswith(("http://", "https://")):
            return False
        info = deck_a.info or {}
        if int(info.get("_stream_refresh_attempts") or 0) >= 2:
            return False
        watch_url = info.get("watch_url") or ""
        vid = info.get("id") or ""
        if not watch_url and not vid:
            return False
        last_err = (getattr(deck_a.decoder, "last_error", "") or "").lower()
        rc = getattr(deck_a.decoder, "last_returncode", None)
        pos_sec = float(deck_a.decoder.position_frames) / float(deck_a.decoder.sample_rate or 44100)
        is_http_auth_err = any(tok in last_err for tok in ("403", "410", "forbidden", "expired", "404"))
        is_premature_drop = (deck_a.length > 10.0 and pos_sec < (deck_a.length - 4.0) and rc not in (None, 0))
        return is_http_auth_err or is_premature_drop or is_stream_url_expired(src)

    def _recover_expired_pcm_stream(
        self, deck_a: _PCMDeckHandle, out: BasePCMOutput, stop_event: threading.Event
    ) -> bool:
        """Re-resolve an expired signed stream URL and resume FFmpeg decode seamlessly at playhead."""
        info = dict(deck_a.info or {})
        attempt = int(info.get("_stream_refresh_attempts") or 0) + 1
        info["_stream_refresh_attempts"] = attempt
        deck_a.info["_stream_refresh_attempts"] = attempt

        watch_url = info.get("watch_url") or f"https://www.youtube.com/watch?v={info.get('id', '')}"
        resume_sec = max(0.0, float(deck_a.decoder.position_frames) / float(deck_a.decoder.sample_rate or 44100))
        logger.warning(
            "Mid-stream termination on remote URL (attempt %d at %.1fs); refreshing stream",
            attempt, resume_sec,
        )
        self._telemetry.record_network_retry(stream_refresh=True)
        try:
            fresh = self._extract_youtube_direct_stream(watch_url, force_refresh=True, cancel_event=stop_event)
            if not fresh or not fresh.get("url") or stop_event.is_set():
                return False
            fresh_url = fresh["url"]
            new_dec = DecoderManager.open_stream(fresh_url, start_seconds=resume_sec, duration=deck_a.length)
            if not new_dec:
                return False
            info["expires_at"] = float(fresh.get("expires_at") or 0.0)
            new_deck = _PCMDeckHandle(self, new_dec, info, fresh_url)
            with self.lock:
                if stop_event.is_set() or not self._using_pcm_pipeline:
                    new_deck.unload()
                    return False
                deck_a.unload()
                self._pcm_deck_a = new_deck
                self.player = new_deck
                self.current_path = fresh_url
                self.current_info = info
                self._pcm_base_time = resume_sec - out.played_seconds()
            logger.info("Recovered expired stream at %.1fs cleanly", resume_sec)
            return True
        except Exception as exc:
            logger.warning("Expired stream recovery failed: %s", redact_sensitive_text(exc))
            return False

    def _handle_pcm_eof(self) -> None:
        if not self._using_pcm_pipeline:
            return
        self._end_track()

    # =========================================================================
    # Main-Thread Periodic UI/Timing Synchronization (_update at 30 Hz)
    # =========================================================================
    def _update(self, dt):
        if not self.player:
            return False

        now = time.time()
        if self.last_tick is None:
            self.last_tick = now
            return True

        dt_real = now - self.last_tick
        self.last_tick = now

        if not self.paused:
            if not getattr(self, "_has_started_playing", False):
                self._has_started_playing = True

            if self._using_pcm_pipeline and self._pcm_output and self._pcm_deck_a:
                # Authoritative playhead synced directly to consumed audio frames
                hw_elapsed = self._pcm_base_time + self._pcm_output.played_seconds()
                if hw_elapsed >= 0:
                    self.elapsed = min(hw_elapsed, self.duration) if self.duration > 0 else hw_elapsed
                dec_dur = self._pcm_deck_a.decoder.duration
                if dec_dur > 0 and abs(self.duration - dec_dur) > 1.0:
                    self.duration = dec_dur
                    self._pcm_deck_a.length = dec_dur
                self.buffer_manager.update_playhead(self.elapsed)
            else:
                try:
                    pos = getattr(self.player, "get_pos", lambda: None)()
                except Exception:
                    pos = None
                self.elapsed += dt_real
                try:
                    flen = getattr(self.player, "length", 0)
                except Exception:
                    flen = 0
                if flen > 0 and abs(self.duration - flen) > 1.0:
                    self.duration = flen
                if pos is not None and pos > 0:
                    if pos > self.elapsed and (pos - self.elapsed) < 2.0:
                        self.elapsed = pos

            # SponsorBlock non-music segment skip check
            if self.sponsorblock_enabled and self.current_info:
                vid = self.current_info.get("id") or extract_video_id(self.current_path or "")
                if vid:
                    skip_to = self.sponsorblock_service.get_skip_target(vid, self.elapsed)
                    if skip_to is not None and skip_to > (self.elapsed + 0.5):
                        old_pos = self.elapsed
                        self.seek(skip_to)
                        if self.on_sponsorblock_skipped:
                            self.on_sponsorblock_skipped(old_pos, skip_to)

            # Crossfade pre-staging lead window (crossfade_duration + 3.0s before end)
            if self.crossfade_duration > 0 and self.duration > (self.crossfade_duration + 4.0):
                rem_time = self.duration - self.elapsed
                if rem_time <= (self.crossfade_duration + 3.0) and not self._crossfade_prepare_sent:
                    self._crossfade_prepare_sent = True
                    if self.on_crossfade_trigger:
                        self.on_crossfade_trigger()
                if rem_time <= self.crossfade_duration:
                    self._is_crossfading = True
                    if not self._using_pcm_pipeline and hasattr(self.player, "volume"):
                        base_vol = 0.0 if self.muted else self.volume
                        self.player.volume = max(0.0, min(base_vol, base_vol * (rem_time / self.crossfade_duration)))

        if self.on_time_update:
            self.on_time_update(self.elapsed, self.duration)

        # Fallback non-PCM track end detection
        if not self._using_pcm_pipeline:
            if getattr(self.player, "state", None) == "stop" and not self.paused and self.elapsed > 1.0:
                return self._end_track()
            if self.duration > 0 and self.elapsed >= self.duration:
                return self._end_track()

        return True

    # =========================================================================
    # Playback Transport, Seek, Volume & Real DSP EQ Controls
    # =========================================================================
    def pause(self) -> None:
        if not self.player:
            return
        with self.lock:
            self.paused = True
            if self._using_pcm_pipeline and self._pcm_output and self._pcm_deck_a:
                self._pcm_output.pause()
                self._pcm_deck_a.stop()
                return
        try:
            if hasattr(self.player, "_mediaplayer") and self.player._mediaplayer:
                try:
                    self.player._mediaplayer.pause()
                    self.player.state = "stop"
                except Exception:
                    self.player.stop()
            elif hasattr(self.player, "_ffplayer") and self.player._ffplayer:
                self.player._ffplayer.set_pause(True)
                self.player.state = "stop"
                self.player._state = "paused"
            elif hasattr(self.player, "set_pause"):
                self.player.set_pause(True)
            else:
                self.player.stop()
        except Exception:
            self.player.stop()

    def unpause(self) -> None:
        if not self.player:
            return
        with self.lock:
            self.paused = False
            self.last_tick = time.time()
            if self._using_pcm_pipeline and self._pcm_output and self._pcm_deck_a:
                self._pcm_deck_a.state = "play"
                self._pcm_deck_a._state = "playing"
                self._pcm_output.resume()
                return
        try:
            if hasattr(self.player, "_mediaplayer") and self.player._mediaplayer:
                try:
                    self.player._mediaplayer.start()
                    self.player.state = "play"
                except Exception:
                    self.player.play()
            elif hasattr(self.player, "_ffplayer") and self.player._ffplayer:
                self.player._ffplayer.set_pause(False)
                self.player.state = "play"
                self.player._state = "playing"
            elif hasattr(self.player, "set_pause"):
                self.player.set_pause(False)
            else:
                self.player.play()
                Clock.schedule_once(lambda dt: self._safe_seek(self.elapsed), 0.1)
        except Exception:
            self.player.play()
            Clock.schedule_once(lambda dt: self._safe_seek(self.elapsed), 0.1)

    def seek(self, target_pos: float) -> None:
        if not self.player:
            return
        target = max(0.0, min(float(target_pos), self.duration if self.duration > 0 else float(target_pos)))
        with self.lock:
            self.elapsed = target
            self.last_tick = time.time()
            if self._using_pcm_pipeline and self._pcm_deck_a and self._pcm_output:
                self._pcm_output.flush()
                self._pcm_base_time = target
                self._pcm_deck_a.decoder.seek(target)
                self.dsp.reset_state()
                return
        self._safe_seek(target)

    def set_volume(self, val: float) -> None:
        """Set playback volume level in range [0.0, 1.0]."""
        self.volume = max(0.0, min(1.0, float(val)))
        if not self._using_pcm_pipeline and self.player and hasattr(self.player, "volume"):
            duck_mult = self._duck_factor if self._is_ducked else 1.0
            self.player.volume = 0.0 if self.muted else (self.volume * duck_mult)

    def set_muted(self, muted: bool) -> None:
        """Mute or unmute audio output while preserving configured volume."""
        self.muted = bool(muted)
        if not self._using_pcm_pipeline and self.player and hasattr(self.player, "volume"):
            duck_mult = self._duck_factor if self._is_ducked else 1.0
            self.player.volume = 0.0 if self.muted else (self.volume * duck_mult)

    def set_ducked(self, ducked: bool, duck_factor: float = 0.25) -> None:
        """Temporarily attenuate gain cleanly during OS transient AudioFocus ducking."""
        with self.lock:
            self._is_ducked = bool(ducked)
            self._duck_factor = max(0.05, min(1.0, float(duck_factor))) if self._is_ducked else 1.0
            eff = 0.0 if self.muted else (self.volume * self._duck_factor)
        if not self._using_pcm_pipeline and self.player and hasattr(self.player, "volume"):
            self.player.volume = eff

    def set_equalizer(self, bands: list, reverb: bool = False) -> None:
        """
        Apply 10-band EQ dB gains (-12..+12 dB) & spatial reverb in real time:
        - Desktop PCM pipeline: updates DSPPipeline biquad filter coefficients live.
        - Android MediaPlayer path: updates native Android AudioEffect Equalizer.
        """
        self.eq_bands = list(bands or [0.0] * 10)
        self.eq_reverb = bool(reverb)
        self.dsp.set_eq_bands(self.eq_bands, self.eq_reverb)
        if platform == "android" and self.player:
            self._android_fx.apply(self.eq_bands, self.eq_reverb)

    def _safe_seek(self, pos: float) -> None:
        if hasattr(self.player, "_mediaplayer") and self.player._mediaplayer:
            try:
                self.player._mediaplayer.seekTo(max(0, int(float(pos) * 1000)))
                return
            except Exception:
                pass
        if hasattr(self.player, "seek") and not isinstance(self.player, _PCMDeckHandle):
            try:
                self.player.seek(pos)
            except TypeError:
                try:
                    self.player.seek(pos, relative=False)
                except Exception:
                    pass
            except Exception:
                pass

    def _end_track(self):
        if self.repeat_one and self.player:
            try:
                if self._using_pcm_pipeline:
                    self.seek(0.0)
                    if self.on_time_update:
                        self.on_time_update(0.0, self.duration)
                    # Restart render worker if it exited at EOF
                    if not self._render_thread or not self._render_thread.is_alive():
                        self._render_stop_event = threading.Event()
                        self._render_thread = threading.Thread(
                            target=self._pcm_render_loop,
                            args=(self._render_stop_event,),
                            daemon=True,
                            name="AudioPCMRenderWorker",
                        )
                        self._render_thread.start()
                    return True
                self.elapsed = 0.0
                self.last_tick = time.time()
                self.player.seek(0)
                self.player.play()
                if self.on_time_update:
                    self.on_time_update(0.0, self.duration)
                return True
            except Exception:
                pass

        self.cleanup_player()
        if self.on_track_end:
            self.on_track_end()
        return False

    def _save_cached_metadata(self, meta_path: str, info: dict) -> None:
        try:
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(info, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _load_cached_metadata(self, meta_path: str) -> Optional[dict]:
        if not os.path.exists(meta_path):
            return None
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def _download_thumbnail(self, url: str, path: str) -> None:
        try:
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp, open(path, "wb") as out_f:
                out_f.write(resp.read())
        except Exception:
            pass

    def fade_out(self, duration: float = 0.25, on_complete=None) -> None:
        """Gradually decreases master volume toward 0.0 over duration, then stops."""
        if not self.player:
            if on_complete:
                on_complete()
            return

        current_vol = self.volume
        steps = 10
        interval = max(0.01, duration / steps)
        step_val = current_vol / steps

        def _step(dt):
            nonlocal current_vol
            if not self.player:
                if on_complete:
                    on_complete()
                return False
            current_vol = max(0.0, current_vol - step_val)
            self.set_volume(current_vol)
            if current_vol <= 0.001:
                self.cleanup_player()
                if on_complete:
                    on_complete()
                return False
            return True

        Clock.schedule_interval(_step, interval)
