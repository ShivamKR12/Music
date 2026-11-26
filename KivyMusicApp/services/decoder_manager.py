"""
Audio Decoder Manager.

Normalizes compressed audio files and network streams (MP3, Opus, M4A, AAC, FLAC, OGG, WAV, HTTPS)
into 44.1 kHz stereo float32 PCM chunks for deterministic DSP filtering and crossfade mixing.
"""

import os
import shutil
import struct
import subprocess
import threading
import wave
from typing import Optional

from services.logger import get_logger
from utils.local_audio_utils import parse_audio_duration

logger = get_logger("DecoderManager")

try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    np = None  # type: ignore
    _HAS_NUMPY = False

DEFAULT_SAMPLE_RATE = 44100
DEFAULT_CHANNELS = 2
BYTES_PER_FRAME = DEFAULT_CHANNELS * 4  # float32 stereo = 8 bytes/frame

_NO_WINDOW_FLAGS = 0x08000000 if os.name == "nt" else 0


def probe_duration_seconds(source: str, fallback: float = 0.0) -> float:
    """Determine accurate track duration using binary header parser first, then ffprobe."""
    if source and os.path.exists(source) and os.path.isfile(source):
        parsed = parse_audio_duration(source)
        if parsed and parsed > 0:
            return float(parsed)

    ffprobe = shutil.which("ffprobe")
    if ffprobe and source:
        try:
            proc = subprocess.run(
                [
                    ffprobe, "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    source,
                ],
                capture_output=True,
                text=True,
                timeout=6,
                creationflags=_NO_WINDOW_FLAGS,
            )
            raw = (proc.stdout or "").strip()
            if raw and raw != "N/A":
                val = float(raw)
                if val > 0:
                    return val
        except Exception as exc:
            logger.debug("ffprobe duration lookup failed for %s: %s", source, exc)
    return float(fallback or 0.0)


class BasePCMDecoder:
    """Common interface for sample-accurate float32 stereo PCM stream decoders."""

    sample_rate: int = DEFAULT_SAMPLE_RATE
    channels: int = DEFAULT_CHANNELS

    def __init__(self, source: str, duration: float = 0.0):
        self.source = source
        self.duration = float(duration or 0.0)
        self.position_frames = 0
        self.eof = False
        self.last_error: str = ""
        self.last_returncode: Optional[int] = None

    def read_frames(self, num_frames: int = 4096):
        raise NotImplementedError

    def seek(self, position_seconds: float) -> bool:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError


class FFmpegPCMDecoder(BasePCMDecoder):
    """Decodes any FFmpeg-supported container or HTTP stream directly to f32le stereo PCM."""

    def __init__(self, source: str, ffmpeg_bin: str, start_seconds: float = 0.0, duration: float = 0.0):
        probed_dur = duration if duration > 0 else probe_duration_seconds(source, 0.0)
        super().__init__(source, probed_dur)
        self._ffmpeg = ffmpeg_bin
        self._lock = threading.RLock()
        self._proc: Optional[subprocess.Popen] = None
        self._closed = False
        self._open_at(max(0.0, float(start_seconds)))

    def _open_at(self, seek_sec: float) -> None:
        old_proc = None
        with self._lock:
            old_proc = self._proc
            self._proc = None
        self._terminate_proc_instance(old_proc)

        cmd = [self._ffmpeg, "-hide_banner", "-loglevel", "error"]
        if str(self.source).startswith(("http://", "https://")):
            cmd.extend(["-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "3"])
        if seek_sec > 0.01:
            cmd.extend(["-ss", f"{seek_sec:.3f}"])
        cmd.extend([
            "-i", self.source,
            "-vn", "-sn", "-dn",
            "-f", "f32le",
            "-acodec", "pcm_f32le",
            "-ar", str(self.sample_rate),
            "-ac", str(self.channels),
            "pipe:1",
        ])
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=_NO_WINDOW_FLAGS,
        )
        with self._lock:
            if self._closed:
                self._terminate_proc_instance(proc)
                return
            self._proc = proc
            self.eof = False
            self.position_frames = int(seek_sec * self.sample_rate)

    @staticmethod
    def _terminate_proc_instance(proc: Optional[subprocess.Popen]) -> None:
        if not proc:
            return
        try:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=0.5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=0.5)
        except Exception:
            pass
        for stream in (proc.stdout, proc.stderr):
            try:
                if stream:
                    stream.close()
            except Exception:
                pass

    def read_frames(self, num_frames: int = 4096):
        with self._lock:
            if self._closed or self.eof or not self._proc or not self._proc.stdout:
                return None
            proc = self._proc
            stdout = proc.stdout

        target_bytes = int(num_frames) * BYTES_PER_FRAME
        chunks = []
        remaining = target_bytes
        while remaining > 0:
            try:
                chunk = stdout.read(remaining)
            except (ValueError, OSError):
                # Pipe closed concurrently by seek() or close()
                return None
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)

        raw = b"".join(chunks)
        usable_bytes = len(raw) - (len(raw) % BYTES_PER_FRAME)
        if usable_bytes == 0:
            with self._lock:
                # Only mark EOF if proc was NOT replaced by a concurrent seek
                if self._proc is proc:
                    self.eof = True
            if proc.stderr:
                try:
                    err = proc.stderr.read().decode("utf-8", errors="ignore").strip()
                    if err:
                        import re as _re
                        clean_err = _re.sub(r"(https?://[^\s'\"<>?]+)\?[^\s'\"<>]+", r"\1?<redacted>", err)
                        self.last_error = clean_err
                        src_label = "<stream>" if str(self.source).startswith(("http://", "https://")) else os.path.basename(self.source)
                        logger.warning("FFmpeg stderr (%s): %s", src_label, clean_err)
                except Exception:
                    pass
            try:
                self.last_returncode = proc.poll()
            except Exception:
                pass
            return None

        frames = usable_bytes // BYTES_PER_FRAME
        with self._lock:
            if self._proc is not proc:
                return None
            self.position_frames += frames
            if len(raw) < target_bytes:
                self.eof = True

        if _HAS_NUMPY:
            return np.frombuffer(raw[:usable_bytes], dtype=np.float32).reshape(-1, self.channels).copy()
        count = usable_bytes // 4
        return list(struct.unpack(f"<{count}f", raw[:usable_bytes]))

    def seek(self, position_seconds: float) -> bool:
        with self._lock:
            if self._closed:
                return False
        target = max(0.0, float(position_seconds))
        if self.duration > 0:
            target = min(target, max(0.0, self.duration - 0.05))
        try:
            self._open_at(target)
            return True
        except Exception as exc:
            logger.error("FFmpeg seek error: %s", exc)
            return False

    def close(self) -> None:
        with self._lock:
            self._closed = True
            proc = self._proc
            self._proc = None
        self._terminate_proc_instance(proc)


class WavPCMDecoder(BasePCMDecoder):
    """Pure-Python PCM WAV decoder (8/16/24/32-bit) normalized to stereo 44.1 kHz float32."""

    def __init__(self, source: str, start_seconds: float = 0.0, duration: float = 0.0):
        self._lock = threading.RLock()
        self._wf = wave.open(source, "rb")
        self._src_channels = self._wf.getnchannels()
        self._src_width = self._wf.getsampwidth()
        self._src_rate = self._wf.getframerate()
        self._src_frames = self._wf.getnframes()
        actual_dur = (self._src_frames / float(self._src_rate)) if self._src_rate > 0 else duration
        super().__init__(source, actual_dur)
        if start_seconds > 0:
            self.seek(start_seconds)

    def read_frames(self, num_frames: int = 4096):
        with self._lock:
            if not self._wf or self.eof:
                return None
            src_count = max(1, int(round(num_frames * (self._src_rate / float(self.sample_rate)))))
            raw = self._wf.readframes(src_count)
            if not raw:
                self.eof = True
                return None

            frames_read = len(raw) // (self._src_channels * self._src_width)
            if frames_read == 0:
                self.eof = True
                return None
            if frames_read < src_count:
                self.eof = True

        samples = self._decode_pcm_bytes(raw)
        if self._src_rate != self.sample_rate and _HAS_NUMPY and len(samples) > 1:
            target_len = max(1, int(round(len(samples) * (self.sample_rate / float(self._src_rate)))))
            x_old = np.linspace(0.0, 1.0, len(samples), endpoint=False)
            x_new = np.linspace(0.0, 1.0, target_len, endpoint=False)
            l_res = np.interp(x_new, x_old, samples[:, 0])
            r_res = np.interp(x_new, x_old, samples[:, 1])
            samples = np.column_stack((l_res, r_res)).astype(np.float32)

        with self._lock:
            self.position_frames += len(samples) if _HAS_NUMPY else (len(samples) // self.channels)
        return samples

    def _decode_pcm_bytes(self, raw: bytes):
        if _HAS_NUMPY:
            if self._src_width == 1:
                arr = (np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0
            elif self._src_width == 2:
                arr = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
            elif self._src_width == 4:
                arr = np.frombuffer(raw, dtype="<i4").astype(np.float32) / 2147483648.0
            else:
                # 24-bit signed little-endian expansion
                u8 = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
                i32 = (u8[:, 0].astype(np.int32) | (u8[:, 1].astype(np.int32) << 8) | (u8[:, 2].astype(np.int32) << 16))
                i32 = np.where(i32 & 0x800000, i32 - 0x1000000, i32)
                arr = i32.astype(np.float32) / 8388608.0

            arr = arr.reshape(-1, self._src_channels)
            if self._src_channels == 1:
                arr = np.repeat(arr, 2, axis=1)
            elif self._src_channels > 2:
                arr = arr[:, :2]
            return arr.astype(np.float32, copy=False)

        # Pure-Python 16-bit fallback
        cnt = len(raw) // 2
        vals = [s / 32768.0 for s in struct.unpack(f"<{cnt}h", raw)]
        if self._src_channels == 1:
            stereo = []
            for v in vals:
                stereo.extend((v, v))
            return stereo
        return vals

    def seek(self, position_seconds: float) -> bool:
        with self._lock:
            if not self._wf or self._src_rate <= 0:
                return False
            target = max(0.0, min(float(position_seconds), self.duration or float(position_seconds)))
            src_frame = min(max(0, int(target * self._src_rate)), max(0, self._src_frames - 1))
            try:
                self._wf.setpos(src_frame)
                self.position_frames = int(target * self.sample_rate)
                self.eof = False
                return True
            except Exception as exc:
                logger.error("WAV seek error: %s", exc)
                return False

    def close(self) -> None:
        with self._lock:
            wf = self._wf
            self._wf = None
            if wf:
                try:
                    wf.close()
                except Exception:
                    pass


class DecoderManager:
    """Creates appropriate PCM stream decoders while checking binary and container availability."""

    @staticmethod
    def has_ffmpeg() -> bool:
        return shutil.which("ffmpeg") is not None

    @staticmethod
    def can_decode_pcm(source: str) -> bool:
        if not source:
            return False
        if shutil.which("ffmpeg") is not None:
            return True
        return str(source).lower().endswith(".wav") and os.path.exists(source)

    @classmethod
    def open_stream(cls, source: str, start_seconds: float = 0.0, duration: float = 0.0) -> Optional[BasePCMDecoder]:
        if not source:
            return None
        lower = str(source).lower()
        if lower.endswith(".wav") and os.path.exists(source):
            try:
                return WavPCMDecoder(source, start_seconds=start_seconds, duration=duration)
            except Exception as exc:
                logger.warning("WavPCMDecoder failed for %s: %s", source, exc)

        ffmpeg_bin = shutil.which("ffmpeg")
        if ffmpeg_bin:
            return FFmpegPCMDecoder(source, ffmpeg_bin=ffmpeg_bin, start_seconds=start_seconds, duration=duration)
        return None
