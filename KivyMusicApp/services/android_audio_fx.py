"""
Android Hardware AudioEffect Integration (Equalizer & PresetReverb via pyjnius).

IMPORTANT STATUS NOTE:
- Designed & Implemented for Android API 9+ attaching to Android MediaPlayer audioSessionId.
- Explicitly NOT verified until tested on physical Android hardware via adb (desktop hosts
  route EQ/AutoEq through services.dsp_pipeline.DSPPipeline instead).
"""

from typing import List, Optional
from kivy.utils import platform
from services.logger import get_logger
from services.dsp_pipeline import ISO_EQ_FREQUENCIES

logger = get_logger("AndroidAudioFX")


class AndroidAudioEffectBridge:
    """Attaches native Android Equalizer / PresetReverb to an active Android MediaPlayer."""

    def __init__(self):
        self._eq = None
        self._reverb = None
        self._session_id: Optional[int] = None

    def attach(self, sound_android_player) -> bool:
        """Bind native Android AudioEffect instances to SoundAndroidPlayer._mediaplayer."""
        self.release()
        if platform != "android" or not sound_android_player:
            return False
        mp = getattr(sound_android_player, "_mediaplayer", None)
        if not mp:
            return False
        try:
            from jnius import autoclass
            Equalizer = autoclass("android.media.audiofx.Equalizer")
            session_id = int(mp.getAudioSessionId())
            eq = Equalizer(0, session_id)
            eq.setEnabled(True)
            self._eq = eq
            self._session_id = session_id
            logger.info("Attached Android Equalizer to session %d (%d bands)", session_id, int(eq.getNumberOfBands()))
            return True
        except Exception as exc:
            logger.warning("AndroidAudioEffect attach failed: %s", exc)
            self.release()
            return False

    def apply(self, bands_db: List[float], reverb: bool = False) -> bool:
        """Map 10-band ISO gains (-12..+12 dB) onto native Android hardware EQ bands."""
        if platform != "android" or not self._eq:
            return False
        try:
            num_bands = int(self._eq.getNumberOfBands())
            lvl_range = self._eq.getBandLevelRange()
            min_mb = int(lvl_range[0])
            max_mb = int(lvl_range[1])

            for band_idx in range(num_bands):
                center_hz = float(self._eq.getCenterFreq(band_idx)) / 1000.0
                # Pick nearest ISO band gain
                nearest_i = min(
                    range(len(ISO_EQ_FREQUENCIES)),
                    key=lambda idx: abs(ISO_EQ_FREQUENCIES[idx] - center_hz),
                )
                target_db = float(bands_db[nearest_i]) if nearest_i < len(bands_db) else 0.0
                mb = max(min_mb, min(max_mb, int(target_db * 100.0)))
                self._eq.setBandLevel(band_idx, mb)

            if reverb and self._session_id is not None and not self._reverb:
                try:
                    from jnius import autoclass
                    PresetReverb = autoclass("android.media.audiofx.PresetReverb")
                    rev = PresetReverb(0, self._session_id)
                    rev.setPreset(PresetReverb.PRESET_SMALLROOM)
                    rev.setEnabled(True)
                    self._reverb = rev
                except Exception:
                    pass
            elif self._reverb:
                self._reverb.setEnabled(bool(reverb))
            return True
        except Exception as exc:
            logger.warning("AndroidAudioEffect apply error: %s", exc)
            return False

    def release(self) -> None:
        for obj_name in ("_eq", "_reverb"):
            obj = getattr(self, obj_name, None)
            if obj is not None:
                try:
                    obj.release()
                except Exception:
                    pass
                setattr(self, obj_name, None)
        self._session_id = None
