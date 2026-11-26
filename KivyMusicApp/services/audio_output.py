"""
PCM Hardware Audio Output Backends.

- SDL2PCMOutput: Opens an SDL2 float32 stereo audio device via Kivy's already-loaded
  SDL2 shared library (zero external DLL conflicts), providing hardware-clock-accurate
  playback telemetry and sub-200ms queue headroom for responsive pausing, seeking, and EQ.
- NullPCMOutput: Deterministic timing sink used when KIVY_HEADLESS=1 or when no audio
  output hardware is available in CI environments.
"""

import ctypes
import ctypes.util
import os
import sys
import threading
import time
from typing import Optional

from services.logger import get_logger

logger = get_logger("AudioOutput")

_SDL_INIT_AUDIO = 0x00000010
_AUDIO_F32LSB = 0x8120
_BYTES_PER_FRAME = 8  # 2 channels * float32


class _SDL_AudioSpec(ctypes.Structure):
    _fields_ = [
        ("freq", ctypes.c_int),
        ("format", ctypes.c_uint16),
        ("channels", ctypes.c_uint8),
        ("silence", ctypes.c_uint8),
        ("samples", ctypes.c_uint16),
        ("padding", ctypes.c_uint16),
        ("size", ctypes.c_uint32),
        ("callback", ctypes.c_void_p),
        ("userdata", ctypes.c_void_p),
    ]


_SDL_LIB_CACHE = None


def _load_sdl2_cdll():
    global _SDL_LIB_CACHE
    if _SDL_LIB_CACHE is not None:
        return _SDL_LIB_CACHE

    candidates = []
    if sys.platform == "win32":
        try:
            import kivy_deps.sdl2 as ksdl
            for bin_dir in getattr(ksdl, "dep_bins", []):
                cand = os.path.join(bin_dir, "SDL2.dll")
                if os.path.exists(cand):
                    candidates.append(cand)
        except Exception:
            pass
    lib_name = ctypes.util.find_library("SDL2")
    if lib_name:
        candidates.append(lib_name)

    for cand in candidates:
        try:
            lib = ctypes.CDLL(cand)
            if hasattr(lib, "SDL_OpenAudioDevice") and hasattr(lib, "SDL_QueueAudio"):
                lib.SDL_InitSubSystem.argtypes = [ctypes.c_uint32]
                lib.SDL_InitSubSystem.restype = ctypes.c_int
                lib.SDL_OpenAudioDevice.argtypes = [
                    ctypes.c_char_p, ctypes.c_int,
                    ctypes.POINTER(_SDL_AudioSpec),
                    ctypes.POINTER(_SDL_AudioSpec),
                    ctypes.c_int,
                ]
                lib.SDL_OpenAudioDevice.restype = ctypes.c_uint32
                lib.SDL_QueueAudio.argtypes = [ctypes.c_uint32, ctypes.c_void_p, ctypes.c_uint32]
                lib.SDL_QueueAudio.restype = ctypes.c_int
                lib.SDL_GetQueuedAudioSize.argtypes = [ctypes.c_uint32]
                lib.SDL_GetQueuedAudioSize.restype = ctypes.c_uint32
                lib.SDL_ClearQueuedAudio.argtypes = [ctypes.c_uint32]
                lib.SDL_PauseAudioDevice.argtypes = [ctypes.c_uint32, ctypes.c_int]
                lib.SDL_CloseAudioDevice.argtypes = [ctypes.c_uint32]
                _SDL_LIB_CACHE = lib
                return lib
        except Exception as exc:
            logger.debug("Candidate SDL2 load failed (%s): %s", cand, exc)
    return None


class BasePCMOutput:
    """Abstract interface for stereo float32 PCM output sinks."""

    def __init__(self, sample_rate: int = 44100, channels: int = 2):
        self.sample_rate = int(sample_rate)
        self.channels = int(channels)
        self._lock = threading.RLock()
        self._frames_queued = 0
        self._paused = False
        self._closed = False

    def write(self, pcm_bytes: bytes, n_frames: int) -> bool:
        raise NotImplementedError

    def queued_seconds(self) -> float:
        raise NotImplementedError

    def played_seconds(self) -> float:
        with self._lock:
            total = self._frames_queued / float(self.sample_rate)
            return max(0.0, total - self.queued_seconds())

    def reset_frame_counter(self, start_frames: int = 0) -> None:
        with self._lock:
            self._frames_queued = int(start_frames)

    def pause(self) -> None:
        self._paused = True

    def resume(self) -> None:
        self._paused = False

    def flush(self) -> None:
        raise NotImplementedError

    def close(self) -> None:
        self._closed = True


class SDL2PCMOutput(BasePCMOutput):
    """Real hardware audio output backed by SDL2 queued PCM playback."""

    def __init__(self, sample_rate: int = 44100, channels: int = 2, buffer_samples: int = 2048):
        super().__init__(sample_rate, channels)
        self._sdl = _load_sdl2_cdll()
        if not self._sdl:
            raise RuntimeError("SDL2 shared library with SDL_QueueAudio unavailable")
        if self._sdl.SDL_InitSubSystem(_SDL_INIT_AUDIO) != 0:
            raise RuntimeError("SDL_InitSubSystem(SDL_INIT_AUDIO) failed")

        want = _SDL_AudioSpec(
            freq=self.sample_rate,
            format=_AUDIO_F32LSB,
            channels=self.channels,
            silence=0,
            samples=buffer_samples,
            padding=0,
            size=0,
            callback=None,
            userdata=None,
        )
        have = _SDL_AudioSpec()
        self._dev_id = self._sdl.SDL_OpenAudioDevice(None, 0, ctypes.byref(want), ctypes.byref(have), 0)
        if self._dev_id == 0:
            raise RuntimeError("SDL_OpenAudioDevice failed to open default playback device")
        self._sdl.SDL_PauseAudioDevice(self._dev_id, 0)
        logger.info("Opened SDL2 PCM output device id=%d (%dHz %dch f32)", self._dev_id, have.freq, have.channels)

    def write(self, pcm_bytes: bytes, n_frames: int) -> bool:
        if self._closed or self._dev_id == 0 or not pcm_bytes:
            return False
        buf = (ctypes.c_ubyte * len(pcm_bytes)).from_buffer_copy(pcm_bytes)
        with self._lock:
            if self._closed or self._dev_id == 0:
                return False
            rc = self._sdl.SDL_QueueAudio(self._dev_id, ctypes.cast(buf, ctypes.c_void_p), len(pcm_bytes))
            if rc == 0:
                self._frames_queued += int(n_frames)
                return True
            return False

    def queued_seconds(self) -> float:
        if self._closed or self._dev_id == 0:
            return 0.0
        qbytes = self._sdl.SDL_GetQueuedAudioSize(self._dev_id)
        return qbytes / float(_BYTES_PER_FRAME * self.sample_rate)

    def pause(self) -> None:
        super().pause()
        if not self._closed and self._dev_id:
            self._sdl.SDL_PauseAudioDevice(self._dev_id, 1)

    def resume(self) -> None:
        super().resume()
        if not self._closed and self._dev_id:
            self._sdl.SDL_PauseAudioDevice(self._dev_id, 0)

    def flush(self) -> None:
        with self._lock:
            if not self._closed and self._dev_id:
                self._sdl.SDL_ClearQueuedAudio(self._dev_id)
            self._frames_queued = 0

    def close(self) -> None:
        with self._lock:
            if not self._closed and self._dev_id:
                try:
                    self._sdl.SDL_ClearQueuedAudio(self._dev_id)
                    self._sdl.SDL_CloseAudioDevice(self._dev_id)
                except Exception:
                    pass
                self._dev_id = 0
            self._closed = True


class NullPCMOutput(BasePCMOutput):
    """Non-blocking clock-paced sink for headless verification and no-audio environments."""

    def __init__(self, sample_rate: int = 44100, channels: int = 2):
        super().__init__(sample_rate, channels)
        self._last_write_time = time.monotonic()
        self._queued_sec = 0.0

    def _drain_elapsed(self) -> None:
        now = time.monotonic()
        if not self._paused:
            dt = max(0.0, now - self._last_write_time)
            self._queued_sec = max(0.0, self._queued_sec - dt)
        self._last_write_time = now

    def write(self, pcm_bytes: bytes, n_frames: int) -> bool:
        with self._lock:
            if self._closed:
                return False
            self._drain_elapsed()
            self._frames_queued += int(n_frames)
            self._queued_sec += float(n_frames) / float(self.sample_rate)
            return True

    def queued_seconds(self) -> float:
        with self._lock:
            self._drain_elapsed()
            return self._queued_sec

    def pause(self) -> None:
        with self._lock:
            self._drain_elapsed()
            super().pause()

    def resume(self) -> None:
        with self._lock:
            self._last_write_time = time.monotonic()
            super().resume()

    def flush(self) -> None:
        with self._lock:
            self._queued_sec = 0.0
            self._frames_queued = 0
            self._last_write_time = time.monotonic()


def create_pcm_output(sample_rate: int = 44100, channels: int = 2) -> BasePCMOutput:
    """Create SDL2 hardware output when interactive audio is available, else NullPCMOutput."""
    if os.environ.get("KIVY_HEADLESS") == "1" or os.environ.get("KIVY_AUDIO") == "dummy":
        return NullPCMOutput(sample_rate, channels)
    try:
        return SDL2PCMOutput(sample_rate, channels)
    except Exception as exc:
        logger.warning("Falling back to NullPCMOutput (%s)", exc)
        return NullPCMOutput(sample_rate, channels)
