"""
Real-Time PCM Digital Signal Processing (DSP) Pipeline.

Implements:
- 10-band RBJ Audio EQ Cookbook peaking biquad filters (32Hz - 16kHz, +/-12 dB)
- Vectorized SciPy SOS cascade with pure-NumPy and pure-Python fallbacks
- Stereo feedback delay reverb with preserved ring-buffer state
- Soft-knee headroom limiter to prevent +/-0dBFS clipping during boosts & crossfades
- Sample-accurate dual-deck equal-power crossfade mixer (cos / sin power curves)
"""

import math
import threading
from typing import List, Optional, Tuple

from services.logger import get_logger

logger = get_logger("DSPPipeline")

try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    np = None  # type: ignore
    _HAS_NUMPY = False

# `scipy.signal` costs ~2.5 s to import and single-handedly regressed cold start.
# It is loaded lazily on a background thread after startup; DSP chunks use the
# pure-NumPy biquad fallback until the vectorized backend is ready.
_scipy_sig = None  # type: ignore
_SCIPY_LOCK = threading.Lock()
_SCIPY_THREAD: Optional[threading.Thread] = None
_SCIPY_IMPORT_FAILED = False


def _load_scipy_signal() -> None:
    global _scipy_sig, _SCIPY_IMPORT_FAILED
    try:
        import scipy.signal as _sig  # noqa: PLC0415 - intentional lazy import
        _scipy_sig = _sig
    except Exception:
        _scipy_sig = None
        _SCIPY_IMPORT_FAILED = True


def ensure_scipy_loaded_async() -> None:
    """Start (or reuse) a daemon thread that imports `scipy.signal`.

    Never blocks the caller. Once loaded, subsequent `DSPPipeline.process()`
    calls automatically switch to the vectorized `sosfilt` path.
    """
    global _SCIPY_THREAD
    if _scipy_sig is not None or _SCIPY_IMPORT_FAILED:
        return
    with _SCIPY_LOCK:
        if _scipy_sig is not None or _SCIPY_IMPORT_FAILED:
            return
        if _SCIPY_THREAD is not None and _SCIPY_THREAD.is_alive():
            return
        _SCIPY_THREAD = threading.Thread(
            target=_load_scipy_signal, name="scipy-signal-warmup", daemon=True
        )
        _SCIPY_THREAD.start()


def ensure_scipy_loaded(timeout: float = 10.0) -> bool:
    """Blocking variant for DSP benchmarks/tests that require `sosfilt`.

    Normal app startup never calls this; the asynchronous warm-up keeps the
    UI thread and cold start free of the ~2.5 s SciPy import cost.
    """
    ensure_scipy_loaded_async()
    thread = _SCIPY_THREAD
    if thread is not None and thread.is_alive():
        thread.join(timeout)
    return _scipy_sig is not None

ISO_EQ_FREQUENCIES: Tuple[float, ...] = (
    32.0, 64.0, 125.0, 250.0, 500.0,
    1000.0, 2000.0, 4000.0, 8000.0, 16000.0,
)


def design_peaking_biquad(
    freq_hz: float,
    gain_db: float,
    sample_rate: int = 44100,
    q: float = 1.41,
) -> Tuple[float, float, float, float, float, float]:
    """
    Compute normalized second-order section [b0, b1, b2, 1.0, a1, a2] using
    the RBJ Audio EQ Cookbook peaking filter equations.
    """
    gain = max(-12.0, min(12.0, float(gain_db)))
    if abs(gain) < 0.05 or freq_hz <= 0 or freq_hz >= (sample_rate * 0.49):
        return (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)

    a_lin = 10.0 ** (gain / 40.0)
    w0 = 2.0 * math.pi * (float(freq_hz) / float(sample_rate))
    alpha = math.sin(w0) / (2.0 * max(0.1, float(q)))
    cos_w0 = math.cos(w0)

    b0 = 1.0 + alpha * a_lin
    b1 = -2.0 * cos_w0
    b2 = 1.0 - alpha * a_lin
    a0 = 1.0 + alpha / a_lin
    a1 = -2.0 * cos_w0
    a2 = 1.0 - alpha / a_lin

    inv_a0 = 1.0 / a0
    return (
        b0 * inv_a0,
        b1 * inv_a0,
        b2 * inv_a0,
        1.0,
        a1 * inv_a0,
        a2 * inv_a0,
    )


def apply_headroom_limiter(pcm, threshold: float = 0.85):
    """
    Soft-knee asymptotic headroom limiter for float32 stereo PCM frames.
    Leaves linear audio untouched below |threshold| while smoothly saturating
    peaks above |threshold| strictly inside (-1.0, 1.0) without wrap-around.
    """
    headroom = 1.0 - threshold
    if _HAS_NUMPY and isinstance(pcm, np.ndarray):
        abs_x = np.abs(pcm)
        over = abs_x > threshold
        if not np.any(over):
            return pcm
        out = pcm.copy()
        excess = (abs_x[over] - threshold) / headroom
        limited = threshold + headroom * np.tanh(excess)
        out[over] = np.sign(pcm[over]) * limited
        return np.clip(out, -0.9999, 0.9999).astype(np.float32, copy=False)

    # Pure-Python list/tuple fallback
    out_list = []
    for sample in pcm:
        a = abs(sample)
        if a <= threshold:
            out_list.append(sample)
        else:
            excess = (a - threshold) / headroom
            val = threshold + headroom * math.tanh(excess)
            val = min(0.9999, val)
            out_list.append(val if sample >= 0 else -val)
    return out_list


def mix_crossfade(pcm_a, pcm_b, p_start: float, p_end: float):
    """
    Mix two equal-length float32 stereo PCM chunks using equal-power cosine/sine
    curves over progress [p_start, p_end] in [0, 1], then apply headroom limiting
    to guard against +3 dB correlated-signal peaking.
    """
    p0 = max(0.0, min(1.0, float(p_start)))
    p1 = max(0.0, min(1.0, float(p_end)))

    if _HAS_NUMPY and isinstance(pcm_a, np.ndarray) and isinstance(pcm_b, np.ndarray):
        n_frames = min(len(pcm_a), len(pcm_b))
        if n_frames == 0:
            return np.zeros((0, 2), dtype=np.float32)
        p = np.linspace(p0, p1, n_frames, dtype=np.float32)[:, None]
        g_out = np.cos(0.5 * np.pi * p).astype(np.float32)
        g_in = np.sin(0.5 * np.pi * p).astype(np.float32)
        mixed = pcm_a[:n_frames] * g_out + pcm_b[:n_frames] * g_in
        return apply_headroom_limiter(mixed)

    # Pure-Python fallback
    n = min(len(pcm_a), len(pcm_b))
    if n == 0:
        return []
    mixed_list = []
    for i in range(n):
        frac = p0 if n == 1 else p0 + (p1 - p0) * (i / (n - 1))
        g_out = math.cos(0.5 * math.pi * frac)
        g_in = math.sin(0.5 * math.pi * frac)
        mixed_list.append(pcm_a[i] * g_out + pcm_b[i] * g_in)
    return apply_headroom_limiter(mixed_list)


class DSPPipeline:
    """
    Stateful real-time stereo PCM DSP processor:
    10-band biquad EQ -> stereo feedback reverb -> master volume -> soft-clip limiter.
    """

    def __init__(self, sample_rate: int = 44100, channels: int = 2):
        self.sample_rate = int(sample_rate)
        self.channels = int(channels)
        self._lock = threading.RLock()
        self._bands_db: List[float] = [0.0] * len(ISO_EQ_FREQUENCIES)
        self._reverb_enabled: bool = False
        self._bypass_eq: bool = True

        self._sos = None
        self._zi = None
        # Pure-NumPy Direct-Form-II transposed state for fallback when SciPy unavailable
        self._py_z1 = [[0.0, 0.0] for _ in ISO_EQ_FREQUENCIES]
        self._py_z2 = [[0.0, 0.0] for _ in ISO_EQ_FREQUENCIES]

        # Asymmetric stereo delay lines for spatial reverb (~30ms L, ~40ms R)
        self._rev_delay_l = max(128, int(0.030 * self.sample_rate))
        self._rev_delay_r = max(128, int(0.040 * self.sample_rate))
        self._rev_buf_l = None
        self._rev_buf_r = None
        self._alloc_reverb_buffers_locked()
        self._rev_pos_l = 0
        self._rev_pos_r = 0

        self._rebuild_filters_locked()

    def _alloc_reverb_buffers_locked(self) -> None:
        if _HAS_NUMPY:
            self._rev_buf_l = np.zeros(self._rev_delay_l, dtype=np.float64)
            self._rev_buf_r = np.zeros(self._rev_delay_r, dtype=np.float64)
        else:
            self._rev_buf_l = [0.0] * self._rev_delay_l
            self._rev_buf_r = [0.0] * self._rev_delay_r

    def set_eq_bands(self, bands_db: List[float], reverb: bool = False) -> None:
        """Update 10-band EQ gains (dB) and reverb toggle seamlessly across chunk boundaries."""
        normalized = [max(-12.0, min(12.0, float(b))) for b in (bands_db or [])[:len(ISO_EQ_FREQUENCIES)]]
        while len(normalized) < len(ISO_EQ_FREQUENCIES):
            normalized.append(0.0)

        with self._lock:
            self._reverb_enabled = bool(reverb)
            self._bypass_eq = all(abs(g) < 0.05 for g in normalized)
            if normalized != self._bands_db:
                self._bands_db = normalized
                self._rebuild_filters_locked()

    def get_eq_bands(self) -> List[float]:
        with self._lock:
            return list(self._bands_db)

    def reset_state(self) -> None:
        """Clear filter delay states and reverb ring buffers (call on seek or track switch)."""
        with self._lock:
            if _HAS_NUMPY and self._sos is not None:
                self._zi = np.zeros((len(ISO_EQ_FREQUENCIES), self.channels, 2), dtype=np.float64)
            self._py_z1 = [[0.0] * self.channels for _ in ISO_EQ_FREQUENCIES]
            self._py_z2 = [[0.0] * self.channels for _ in ISO_EQ_FREQUENCIES]
            self._alloc_reverb_buffers_locked()
            self._rev_pos_l = 0
            self._rev_pos_r = 0

    def _rebuild_filters_locked(self) -> None:
        coeffs = [
            design_peaking_biquad(freq, gain, self.sample_rate, q=1.41)
            for freq, gain in zip(ISO_EQ_FREQUENCIES, self._bands_db)
        ]
        if _HAS_NUMPY:
            self._sos = np.asarray(coeffs, dtype=np.float64)
            if self._zi is None or self._zi.shape != (len(ISO_EQ_FREQUENCIES), self.channels, 2):
                self._zi = np.zeros((len(ISO_EQ_FREQUENCIES), self.channels, 2), dtype=np.float64)
        else:
            self._sos = coeffs

    def process(self, pcm, volume: float = 1.0):
        """
        Process float32 stereo PCM frames shape (N, 2) through EQ, reverb,
        master volume scaling, and soft-clip headroom protection.
        """
        vol = max(0.0, min(1.0, float(volume)))
        if _HAS_NUMPY and isinstance(pcm, np.ndarray):
            if len(pcm) == 0:
                return pcm
            if vol <= 0.0001:
                return np.zeros_like(pcm, dtype=np.float32)

            with self._lock:
                x = pcm.astype(np.float64, copy=False)
                if not self._bypass_eq:
                    sig = _scipy_sig
                    if sig is None:
                        ensure_scipy_loaded_async()
                    if sig is not None:
                        # scipy.signal.sosfilt expects zi shaped (n_sections, 2, n_channels)
                        zi_scipy = np.transpose(self._zi, (0, 2, 1))
                        y, zi_out = sig.sosfilt(self._sos, x, axis=0, zi=zi_scipy)
                        self._zi = np.transpose(zi_out, (0, 2, 1))
                    else:
                        y = self._biquad_numpy_fallback(x)
                else:
                    y = x

                if self._reverb_enabled:
                    y = self._apply_reverb_numpy(y)

            scaled = (y * vol).astype(np.float32)
            return apply_headroom_limiter(scaled)

        # Pure-Python interleaved fallback
        if not pcm:
            return pcm
        if vol <= 0.0001:
            return [0.0] * len(pcm)
        with self._lock:
            out = self._biquad_python_fallback(pcm) if not self._bypass_eq else list(pcm)
        scaled_list = [s * vol for s in out]
        return apply_headroom_limiter(scaled_list)

    def _biquad_numpy_fallback(self, x):
        """Pure-NumPy Direct-Form-II Transposed cascade when SciPy is absent."""
        y = x.copy()
        for idx, (b0, b1, b2, _a0, a1, a2) in enumerate(self._sos):
            if abs(self._bands_db[idx]) < 0.05:
                continue
            z1_l, z1_r = self._py_z1[idx]
            z2_l, z2_r = self._py_z2[idx]
            col_l = y[:, 0]
            col_r = y[:, 1]
            for i in range(len(col_l)):
                xl = col_l[i]
                yl = b0 * xl + z1_l
                z1_l = b1 * xl - a1 * yl + z2_l
                z2_l = b2 * xl - a2 * yl
                col_l[i] = yl

                xr = col_r[i]
                yr = b0 * xr + z1_r
                z1_r = b1 * xr - a1 * yr + z2_r
                z2_r = b2 * xr - a2 * yr
                col_r[i] = yr
            self._py_z1[idx] = [z1_l, z1_r]
            self._py_z2[idx] = [z2_l, z2_r]
        return y

    def _biquad_python_fallback(self, interleaved_samples: List[float]) -> List[float]:
        out = list(interleaved_samples)
        for idx, (b0, b1, b2, _a0, a1, a2) in enumerate(self._sos):
            if abs(self._bands_db[idx]) < 0.05:
                continue
            for ch in range(self.channels):
                z1 = self._py_z1[idx][ch]
                z2 = self._py_z2[idx][ch]
                for i in range(ch, len(out), self.channels):
                    s = out[i]
                    y = b0 * s + z1
                    z1 = b1 * s - a1 * y + z2
                    z2 = b2 * s - a2 * y
                    out[i] = y
                self._py_z1[idx][ch] = z1
                self._py_z2[idx][ch] = z2
        return out

    @staticmethod
    def _comb_channel_numpy(col, buf, pos: int, delay: int, fb: float, wet: float) -> int:
        n = len(col)
        idx = 0
        while idx < n:
            m = min(n - idx, delay - pos)
            delayed = buf[pos : pos + m].copy()
            seg = col[idx : idx + m]
            buf[pos : pos + m] = seg + delayed * fb
            seg += delayed * wet
            pos += m
            if pos >= delay:
                pos = 0
            idx += m
        return pos

    def _apply_reverb_numpy(self, y):
        """Vectorized stereo comb reflection for spatial ambience without Python per-sample loops."""
        out = y.copy()
        fb = 0.30
        wet = 0.18
        self._rev_pos_l = self._comb_channel_numpy(
            out[:, 0], self._rev_buf_l, self._rev_pos_l, self._rev_delay_l, fb, wet
        )
        self._rev_pos_r = self._comb_channel_numpy(
            out[:, 1], self._rev_buf_r, self._rev_pos_r, self._rev_delay_r, fb, wet
        )
        return out
