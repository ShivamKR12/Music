"""
Hardened YouTube Extraction Pipeline (Priority 3 Subsystem).

Pipeline architecture:
  Extractor -> Client Selection -> PO-Token Provider Hook -> Format Validation ->
  Signed Stream URL (+ Expiry) -> Playback Engine / BufferManager (with refresh).

Security & Reliability guarantees:
- Explicit error taxonomy (`ExtractionErrorCode` & `YouTubeExtractionError`) instead of
  blanket silent swallows.
- Never silently discards yt-dlp warnings/errors: routes them cleanly through
  `YtdlpLogBridge` while redacting signed query params, PO tokens, and cookies.
- Cancellation-aware exponential backoff retries and ordered client-tier fallback.
- Pluggable PO-Token provider hook (Python callable or HTTP server endpoint hook)
  plus native yt-dlp PoTokenProvider bridge when registered.
- Never hardcodes `missing_pot` as a magic bypass; keeps it strictly as a documented
  last-resort tier while validating audio codecs, container URLs, and expiry times.
"""

from __future__ import annotations

import os
import random
import re
import threading
import time
import urllib.parse
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from services.logger import get_logger
from services.telemetry_service import get_telemetry

logger = get_logger("YouTubeExtractor")


# =============================================================================
# Secret / Signed URL Redaction & Non-Silent Logging Bridge
# =============================================================================
_URL_QUERY_RE = re.compile(r"(https?://[^\s'\"<>?]+)\?[^\s'\"<>]+")
_SECRET_KV_RE = re.compile(
    r"(?i)(po_token|potoken|token|sig|lsig|signature|s|api_key|key|cookie|authorization)=([^&\s'\",;]+)"
)
_B64_POT_RE = re.compile(r"(?i)((?:web|mweb|android|ios|tv)[^\s+]*\.(?:gvs|player|subs)\+)([^\s'\",;]+)")


def redact_sensitive_text(text: Any) -> str:
    """Scrub signed query strings, PO tokens, signatures, and auth headers from text/logs."""
    if text is None:
        return ""
    s = str(text)
    s = _URL_QUERY_RE.sub(r"\1?<redacted>", s)
    s = _B64_POT_RE.sub(r"\1<redacted>", s)
    s = _SECRET_KV_RE.sub(r"\1=<redacted>", s)
    return s


class YtdlpLogBridge:
    """
    Replaces silent loggers across the codebase.
    Routes yt-dlp warnings/errors to unified logging with secret/URL redaction and
    captures messages so extractors can classify hidden extraction failures accurately.
    """

    def __init__(self, target_logger=None):
        self._logger = target_logger or logger
        self._lock = threading.Lock()
        self.warnings: List[str] = []
        self.errors: List[str] = []

    def debug(self, msg: Any) -> None:
        # Forward critical PO-token/extractor debug hints at TRACE/DEBUG level without leaking secrets
        s = str(msg or "")
        if "po_token" in s.lower() or "bot" in s.lower() or "nsig" in s.lower():
            self._logger.debug("YTDLP: %s", redact_sensitive_text(s))

    def warning(self, msg: Any) -> None:
        clean = redact_sensitive_text(msg)
        with self._lock:
            self.warnings.append(clean)
        self._logger.warning("YTDLP: %s", clean)

    def error(self, msg: Any) -> None:
        clean = redact_sensitive_text(msg)
        with self._lock:
            self.errors.append(clean)
        self._logger.error("YTDLP: %s", clean)

    def snapshot_messages(self) -> List[str]:
        with self._lock:
            return list(self.errors) + list(self.warnings)


# Backward-compatible export name; never silent anymore.
SilentLogger = YtdlpLogBridge


# =============================================================================
# Explicit Extraction Error Taxonomy
# =============================================================================
class ExtractionErrorCode:
    PO_TOKEN_REQUIRED = "PO_TOKEN_REQUIRED"
    AGE_RESTRICTED = "AGE_RESTRICTED"
    GEO_BLOCKED = "GEO_BLOCKED"
    UNAVAILABLE = "UNAVAILABLE"
    STREAM_EXPIRED = "STREAM_EXPIRED"
    RATE_LIMITED = "RATE_LIMITED"
    NETWORK_TRANSIENT = "NETWORK_TRANSIENT"
    NO_VALID_FORMAT = "NO_VALID_FORMAT"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"


NON_RETRYABLE_CODES = {
    ExtractionErrorCode.AGE_RESTRICTED,
    ExtractionErrorCode.GEO_BLOCKED,
    ExtractionErrorCode.UNAVAILABLE,
    ExtractionErrorCode.CANCELLED,
}


class YouTubeExtractionError(RuntimeError):
    """Structured exception carrying machine error code, safe message, and retry hint."""

    def __init__(
        self,
        code: str,
        user_message: str,
        raw_message: str = "",
        retryable: bool = False,
    ):
        self.code = code
        self.user_message = redact_sensitive_text(user_message)
        self.raw_message = redact_sensitive_text(raw_message)
        self.retryable = bool(retryable)
        super().__init__(self.user_message)


def classify_extraction_error(raw_message: str) -> Tuple[str, str, bool]:
    """
    Classify raw yt-dlp / HTTP error messages into (error_code, user_message, is_retryable).
    """
    msg = (raw_message or "").strip()
    low = msg.lower()

    if "po token" in low or "po_token" in low or "confirm you’re not a bot" in low or "confirm you're not a bot" in low or "botguard" in low:
        return (
            ExtractionErrorCode.PO_TOKEN_REQUIRED,
            "YouTube requested bot verification / PO Token; try again or configure a PO-Token provider",
            True,  # retryable via client tier fallback
        )
    if "sign in to confirm your age" in low or "age-restricted" in low or "age gate" in low:
        return (
            ExtractionErrorCode.AGE_RESTRICTED,
            "Track is age-restricted on YouTube",
            False,
        )
    if "not made this video available in your country" in low or "geo-restricted" in low or "blocked it in your country" in low:
        return (
            ExtractionErrorCode.GEO_BLOCKED,
            "Track is region-restricted in your location",
            False,
        )
    if (
        "video unavailable" in low
        or "video is unavailable" in low
        or "private video" in low
        or "this video has been removed" in low
        or "account associated with this video has been terminated" in low
        or "copyright" in low
    ):
        return (
            ExtractionErrorCode.UNAVAILABLE,
            "Track is private or unavailable on YouTube",
            False,
        )
    if "403" in low or "410" in low or "forbidden" in low or "expired" in low or "signature extraction failed" in low or "nsig" in low:
        return (
            ExtractionErrorCode.STREAM_EXPIRED,
            "Audio stream authorization expired or was rejected; refreshing stream",
            True,
        )
    if "429" in low or "too many requests" in low:
        return (
            ExtractionErrorCode.RATE_LIMITED,
            "YouTube rate-limited requests briefly; retrying",
            True,
        )
    if any(k in low for k in ("timed out", "timeout", "connection", "ssl", "eof", "incompleteread", "name resolution", "temporarily unavailable", "reset by peer")):
        return (
            ExtractionErrorCode.NETWORK_TRANSIENT,
            "Network error while contacting YouTube",
            True,
        )
    if "requested format is not available" in low or "no video formats" in low or "no playable" in low:
        return (
            ExtractionErrorCode.NO_VALID_FORMAT,
            "No playable audio stream format returned for this track",
            True,
        )
    return (
        ExtractionErrorCode.UNKNOWN,
        redact_sensitive_text(msg) or "Failed to extract YouTube audio stream",
        True,
    )


# =============================================================================
# URL Expiry Parsing & Audio Format Validation
# =============================================================================
def parse_stream_expiry(url: str) -> float:
    """
    Parse GoogleVideo / signed CDN stream expiration timestamp (`expire=<epoch>`).
    Returns Unix epoch float, or 0.0 if the URL has no explicit expiry parameter.
    """
    if not url or not isinstance(url, str):
        return 0.0
    try:
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        exp_vals = qs.get("expire") or qs.get("exp") or []
        if exp_vals:
            val = float(exp_vals[0])
            if val > 1_000_000_000:
                return val
        # Googlevideo manifest/range path segments: /expire/1735689600/
        m = re.search(r"/expire/(\d{9,12})(?:/|$)", parsed.path)
        if m:
            return float(m.group(1))
    except Exception:
        pass
    return 0.0


def is_stream_url_expired(url: str, expires_at: float = 0.0, leeway_sec: float = 60.0) -> bool:
    """
    Return True when a signed stream URL is missing, empty, or within `leeway_sec` of expiry.
    Non-expiring URLs (e.g., local test HTTP servers without `expire=`) return False.
    """
    if not url or not str(url).startswith(("http://", "https://")):
        return False
    exp = float(expires_at or 0.0)
    if exp <= 0.0:
        exp = parse_stream_expiry(url)
    if exp <= 0.0:
        return False
    return time.time() >= (exp - max(0.0, float(leeway_sec)))


def _is_android_runtime() -> bool:
    try:
        from kivy.utils import platform
        return platform == "android"
    except Exception:
        return False


def _score_audio_format(fmt: dict, prefer_mp4a: bool = False) -> Tuple[int, float, int]:
    """Score candidate yt-dlp format dicts: direct audio codecs preferred over manifest-only."""
    ext = (fmt.get("ext") or "").lower()
    acodec = (fmt.get("acodec") or "").lower()
    vcodec = (fmt.get("vcodec") or "").lower()
    protocol = (fmt.get("protocol") or "").lower()

    audio_only_bonus = 2 if vcodec in ("none", "", None) else 0
    if prefer_mp4a:
        # Android SoundAndroidPlayer natively supports mp4/m4a/aac/mp3/ogg/wav/flac, not webm
        is_android_mp4 = "mp4a" in acodec or ext in ("m4a", "mp4", "aac")
        codec_rank = 3 if is_android_mp4 else (2 if ext in ("mp3", "ogg", "flac", "wav") else 0)
    else:
        codec_rank = 3 if "opus" in acodec or ext == "webm" else (2 if "mp4a" in acodec or ext in ("m4a", "aac") else 1)
    direct_proto_bonus = 2 if protocol in ("https", "http", "") else 0
    abr = float(fmt.get("abr") or fmt.get("tbr") or 0.0)
    return (audio_only_bonus + direct_proto_bonus, codec_rank, int(abr))


def validate_and_select_audio_format(info: Optional[dict], prefer_mp4a: bool = False) -> Optional[dict]:
    """
    Validate extracted yt-dlp info_dict and pick a playable, non-DRM audio stream URL.
    Returns normalized stream descriptor dict or None when no valid audio stream exists.
    """
    if not info or not isinstance(info, dict):
        return None
    if info.get("has_drm"):
        return None

    candidates: List[dict] = []
    if info.get("url") and str(info["url"]).startswith(("http://", "https://")):
        # Top-level selected format
        if (info.get("acodec") or "mp4a").lower() != "none":
            candidates.append(info)
    for key in ("requested_formats", "formats"):
        for f in (info.get(key) or []):
            if not isinstance(f, dict):
                continue
            if f.get("has_drm"):
                continue
            u = f.get("url") or ""
            if not u.startswith(("http://", "https://")):
                continue
            if (f.get("acodec") or "").lower() == "none":
                continue
            candidates.append(f)

    if not candidates:
        return None

    best = max(candidates, key=lambda f: _score_audio_format(f, prefer_mp4a=prefer_mp4a))
    stream_url = best.get("url") or ""
    if not stream_url.startswith(("http://", "https://")):
        return None

    expires_at = parse_stream_expiry(stream_url)
    ext = (best.get("ext") or info.get("ext") or "m4a").lower()
    abr = int(best.get("abr") or info.get("abr") or 128)
    headers = dict(best.get("http_headers") or info.get("http_headers") or {})
    return {
        "url": stream_url,
        "ext": ext,
        "abr": max(32, abr),
        "title": info.get("title") or "Unknown",
        "artist": info.get("uploader") or info.get("channel") or info.get("artist") or "",
        "duration": int(info.get("duration") or 0),
        "thumbnail": info.get("thumbnail") or "",
        "expires_at": expires_at,
        "protocol": best.get("protocol") or "https",
        "acodec": best.get("acodec") or "",
        "http_headers": headers,
        "raw_info": info,
    }


# =============================================================================
# PO-Token Provider Hook Architecture
# =============================================================================
PoTokenCallable = Callable[[str, str, str], Optional[str]]


class PoTokenProviderManager:
    """
    Manages pluggable PO-Token providers:
    1. Registered in-process callback (`fn(video_id, client, context) -> str | None`).
    2. External local HTTP PO-Token service (e.g., BgUtils `KYM_POT_SERVER_URL` / setting `yt_pot_server_url`).
    3. Configured session token string (`KYM_YT_PO_TOKEN` / setting `yt_po_token`).
    Also wires an optional native `yt-dlp` PoTokenProvider when callbacks are supplied.
    """

    def __init__(self):
        self._lock = threading.RLock()
        self._callback: Optional[PoTokenCallable] = None
        self._server_url: str = os.environ.get("KYM_POT_SERVER_URL", "").strip()
        self._static_tokens: List[str] = []
        self._ytdlp_bridge_registered = False
        env_tok = os.environ.get("KYM_YT_PO_TOKEN", "").strip()
        if env_tok:
            self._static_tokens.append(env_tok)

    def register_callback(self, fn: Optional[PoTokenCallable]) -> None:
        with self._lock:
            self._callback = fn
        if fn is not None:
            self._ensure_ytdlp_provider_registered()

    def set_server_url(self, server_url: str) -> None:
        with self._lock:
            self._server_url = (server_url or "").strip().rstrip("/")
        if self._server_url:
            self._ensure_ytdlp_provider_registered()

    def set_static_token(self, token_spec: str) -> None:
        with self._lock:
            clean = (token_spec or "").strip()
            self._static_tokens = [clean] if clean else []

    def clear(self) -> None:
        with self._lock:
            self._callback = None
            self._server_url = os.environ.get("KYM_POT_SERVER_URL", "").strip()
            env_tok = os.environ.get("KYM_YT_PO_TOKEN", "").strip()
            self._static_tokens = [env_tok] if env_tok else []

    def _read_settings_tokens(self) -> Tuple[str, str]:
        """Safely inspect optional user-configured settings without blocking hard on DB failures."""
        try:
            from models.database import get_setting
            tok = (get_setting("yt_po_token", "") or "").strip()
            srv = (get_setting("yt_pot_server_url", "") or "").strip().rstrip("/")
            return tok, srv
        except Exception:
            return "", ""

    def resolve_po_tokens(
        self,
        video_id: str,
        clients: Iterable[str],
        context: str = "gvs",
    ) -> List[str]:
        """
        Resolve formatted `client.context+TOKEN` entries for yt-dlp `extractor_args`.
        Returns empty list cleanly if no provider/token is configured.
        """
        with self._lock:
            cb = self._callback
            srv_url = self._server_url
            static = list(self._static_tokens)

        db_tok, db_srv = self._read_settings_tokens()
        if db_tok and db_tok not in static:
            static.append(db_tok)
        if not srv_url and db_srv:
            srv_url = db_srv

        out: List[str] = []
        client_list = [str(c).strip() for c in clients if c]

        # 1. Static / configured tokens (`web.gvs+<b64>` or bare token applied to active clients)
        for spec in static:
            if "+" in spec:
                out.append(spec)
            elif client_list:
                out.append(f"{client_list[0]}.{context}+{spec}")

        # 2. In-process Python callback hook
        if cb:
            for client in client_list:
                try:
                    res = cb(video_id, client, context)
                    if res and isinstance(res, str):
                        formatted = res if "+" in res else f"{client}.{context}+{res.strip()}"
                        if formatted not in out:
                            out.append(formatted)
                except Exception as exc:
                    logger.warning("PO-Token callback error (%s): %s", client, redact_sensitive_text(exc))

        # 3. External local BgUtils-compatible HTTP PO-Token endpoint hook
        if srv_url:
            import requests
            for client in client_list[:2]:
                try:
                    resp = requests.post(
                        f"{srv_url}/get_pot",
                        json={"video_id": video_id, "client": client, "context": context},
                        timeout=3.0,
                    )
                    if resp.status_code == 200:
                        data = resp.json() if resp.content else {}
                        tok = (data.get("poToken") or data.get("po_token") or "").strip()
                        if tok:
                            formatted = f"{client}.{context}+{tok}"
                            if formatted not in out:
                                out.append(formatted)
                except Exception as exc:
                    logger.debug("PO-Token HTTP hook skipped (%s): %s", client, redact_sensitive_text(exc))

        return out

    def _ensure_ytdlp_provider_registered(self) -> None:
        """Optionally register a lightweight bridge with yt-dlp's built-in POT framework."""
        with self._lock:
            if self._ytdlp_bridge_registered:
                return
            self._ytdlp_bridge_registered = True

        manager = self
        try:
            from yt_dlp.extractor.youtube.pot.provider import (
                PoTokenProvider,
                PoTokenRequest,
                PoTokenResponse,
                register_preference,
                register_provider,
            )

            @register_provider
            class KivyAppHookPTP(PoTokenProvider):  # type: ignore[misc]
                PROVIDER_VERSION = "1.0.0"
                BUG_REPORT_LOCATION = "KivyMusicApp local hook"
                _SUPPORTED_CLIENTS = ("web", "mweb", "android", "ios", "tv", "web_safari", "android_vr")
                _SUPPORTED_CONTEXTS = ("gvs", "player", "subs")

                def is_available(self) -> bool:
                    with manager._lock:
                        return bool(manager._callback or manager._server_url)

                def _real_request_pot(self, request: PoTokenRequest) -> PoTokenResponse:
                    vid = request.video_id or ""
                    client = request.internal_client_name or "web"
                    ctx = request.context.value if request.context else "gvs"
                    tokens = manager.resolve_po_tokens(vid, [client], context=ctx)
                    for t in tokens:
                        _, sep, val = t.partition("+")
                        if sep and val:
                            return PoTokenResponse(po_token=val)
                    from yt_dlp.extractor.youtube.pot.provider import PoTokenProviderRejectedRequest
                    raise PoTokenProviderRejectedRequest("No PO Token produced by registered app hook")

            @register_preference(KivyAppHookPTP)
            def _hook_pref(provider, request):
                return 100
        except Exception as exc:
            logger.debug("yt-dlp PoTokenProvider bridge unavailable: %s", exc)


# =============================================================================
# Ordered Client Tiers & Hardened Extractor Coordinator
# =============================================================================
@dataclass(frozen=True)
class ClientTier:
    name: str
    clients: Tuple[str, ...]
    allow_missing_pot_fallback: bool = False
    format_selector: str = "bestaudio[acodec=opus]/bestaudio[ext=m4a]/bestaudio/best"


DEFAULT_CLIENT_TIERS: Tuple[ClientTier, ...] = (
    ClientTier(
        name="android_direct",
        clients=("android",),
        allow_missing_pot_fallback=False,
    ),
    ClientTier(
        name="ytdlp_default",
        clients=(),
        allow_missing_pot_fallback=False,
    ),
    ClientTier(
        name="web_clients",
        clients=("mweb", "web_safari", "web"),
        allow_missing_pot_fallback=False,
    ),
    ClientTier(
        name="mobile_embedded",
        clients=("ios", "tv", "android_vr"),
        allow_missing_pot_fallback=False,
    ),
    ClientTier(
        name="missing_pot_fallback",
        clients=("android", "mweb", "web", "ios"),
        allow_missing_pot_fallback=True,
    ),
)


@dataclass
class _CachedStreamEntry:
    data: Dict[str, Any]
    cached_at: float = field(default_factory=time.time)


class YouTubeExtractor:
    """
    Central coordinator implementing:
      Extractor -> Client Selection -> PO-Token Hook -> Format Validation ->
      Signed Stream URL (+ Expiry) -> Retry / Refresh Strategy.
    """

    def __init__(
        self,
        po_token_manager: Optional[PoTokenProviderManager] = None,
        client_tiers: Optional[Tuple[ClientTier, ...]] = None,
        max_retries_per_tier: int = 2,
        base_backoff_sec: float = 0.45,
        max_backoff_sec: float = 3.5,
        ydl_factory: Optional[Callable[[dict], Any]] = None,
    ):
        self.po_token_manager = po_token_manager or PoTokenProviderManager()
        self.client_tiers = client_tiers or DEFAULT_CLIENT_TIERS
        self.max_retries_per_tier = max(1, int(max_retries_per_tier))
        self.base_backoff_sec = float(base_backoff_sec)
        self.max_backoff_sec = float(max_backoff_sec)
        self._ydl_factory = ydl_factory
        self._cache_lock = threading.RLock()
        self._stream_cache: Dict[str, _CachedStreamEntry] = {}

    def register_po_token_provider(self, fn: Optional[PoTokenCallable]) -> None:
        self.po_token_manager.register_callback(fn)

    def invalidate_cached_stream(self, video_id: str) -> None:
        if not video_id:
            return
        with self._cache_lock:
            self._stream_cache.pop(video_id, None)

    def get_cached_stream(self, video_id: str, leeway_sec: float = 90.0) -> Optional[Dict[str, Any]]:
        if not video_id:
            return None
        with self._cache_lock:
            entry = self._stream_cache.get(video_id)
            if not entry:
                return None
            url = entry.data.get("url", "")
            exp = entry.data.get("expires_at", 0.0)
            if is_stream_url_expired(url, expires_at=exp, leeway_sec=leeway_sec):
                self._stream_cache.pop(video_id, None)
                return None
            # Reject overly stale non-expiring entries after 4 hours just in case
            if (time.time() - entry.cached_at) > 4 * 3600:
                self._stream_cache.pop(video_id, None)
                return None
            return dict(entry.data)

    @staticmethod
    def normalize_video_id(url_or_id: str) -> str:
        if not url_or_id:
            return ""
        s = str(url_or_id).strip()
        if len(s) == 11 and "/" not in s and "=" not in s and "?" not in s:
            return s
        if "v=" in s:
            return s.split("v=")[-1].split("&")[0]
        if "youtu.be/" in s:
            return s.split("youtu.be/")[-1].split("?")[0]
        cleaned = re.sub(r"[^a-zA-Z0-9_-]", "", s)
        return cleaned[:11] if cleaned else "unknown"

    def _open_ydl(self, ydl_opts: dict):
        if self._ydl_factory is not None:
            return self._ydl_factory(ydl_opts)
        from yt_dlp import YoutubeDL  # Lazy import preserves fast cold startup
        return YoutubeDL(ydl_opts)

    def build_ydl_opts(
        self,
        video_id: str = "",
        tier: Optional[ClientTier] = None,
        extract_flat: bool = False,
        for_download: bool = False,
        extra_opts: Optional[dict] = None,
        log_bridge: Optional[YtdlpLogBridge] = None,
    ) -> dict:
        """Assemble consistent hardened YoutubeDL options with logging bridge and PO-token hooks."""
        active_tier = tier or self.client_tiers[0]
        bridge = log_bridge or YtdlpLogBridge(logger)
        yt_args: Dict[str, Any] = {}
        if active_tier.clients:
            yt_args["player_client"] = list(active_tier.clients)

        po_tokens = self.po_token_manager.resolve_po_tokens(
            video_id, active_tier.clients or ("web", "android"), context="gvs"
        )
        if po_tokens:
            yt_args["po_token"] = po_tokens
        elif active_tier.allow_missing_pot_fallback:
            yt_args["formats"] = ["missing_pot"]

        opts: Dict[str, Any] = {
            "quiet": True,
            "no_warnings": False,
            "noplaylist": True,
            "logger": bridge,
            "socket_timeout": 12,
            "extractor_retries": 1,
            "nocheckcertificate": True,
        }
        if yt_args:
            opts["extractor_args"] = {"youtube": yt_args}
        if extract_flat:
            opts["extract_flat"] = True
            opts["skip_download"] = True
            opts["default_search"] = "ytsearch"
        elif not for_download:
            opts["format"] = active_tier.format_selector
            opts["skip_download"] = True

        if extra_opts:
            opts.update(extra_opts)
        return opts

    def _compute_backoff(self, attempt_index: int) -> float:
        raw = min(self.max_backoff_sec, self.base_backoff_sec * (2 ** max(0, attempt_index - 1)))
        jitter = random.uniform(0.0, 0.25 * raw)
        return raw + jitter

    @staticmethod
    def _wait_backoff(delay: float, cancel_event: Optional[threading.Event]) -> bool:
        """Sleep `delay` seconds unless cancelled. Returns False if cancelled."""
        if delay <= 0:
            return not (cancel_event and cancel_event.is_set())
        if cancel_event is not None:
            return not cancel_event.wait(timeout=delay)
        time.sleep(delay)
        return True

    def extract_stream(
        self,
        watch_url_or_id: str,
        force_refresh: bool = False,
        cancel_event: Optional[threading.Event] = None,
        excluded_tiers: Optional[Iterable[str]] = None,
    ) -> Dict[str, Any]:
        """
        Execute the full YouTube stream extraction pipeline with client tiers, PO-token
        hook injection, format validation, signed URL expiry capture, and backoff retries.
        Raises `YouTubeExtractionError` on failure; never leaks raw URLs/tokens.
        """
        if cancel_event and cancel_event.is_set():
            raise YouTubeExtractionError(ExtractionErrorCode.CANCELLED, "Extraction cancelled")

        is_watch_url = isinstance(watch_url_or_id, str) and (
            "youtube.com/" in watch_url_or_id or "youtu.be/" in watch_url_or_id
        )
        vid = self.normalize_video_id(watch_url_or_id)
        watch_url = watch_url_or_id if is_watch_url else f"https://www.youtube.com/watch?v={vid}"

        if not force_refresh and vid and vid != "unknown":
            cached = self.get_cached_stream(vid, leeway_sec=90.0)
            if cached:
                return cached

        t_op = time.perf_counter()
        last_err = YouTubeExtractionError(
            ExtractionErrorCode.NO_VALID_FORMAT,
            "Could not extract playable audio stream from YouTube",
        )

        excluded = set(excluded_tiers or [])
        active_tiers = [t for t in self.client_tiers if t.name not in excluded] or list(self.client_tiers)
        prefer_mp4a = _is_android_runtime()

        for tier in active_tiers:
            for attempt in range(1, self.max_retries_per_tier + 1):
                if cancel_event and cancel_event.is_set():
                    get_telemetry().record_provider_outcome(
                        "youtube", "extract_stream", False, (time.perf_counter() - t_op) * 1000.0,
                        ExtractionErrorCode.CANCELLED,
                    )
                    raise YouTubeExtractionError(ExtractionErrorCode.CANCELLED, "Extraction cancelled")

                bridge = YtdlpLogBridge(logger)
                opts = self.build_ydl_opts(video_id=vid, tier=tier, extract_flat=False, log_bridge=bridge)

                try:
                    with self._open_ydl(opts) as ydl:
                        info = ydl.extract_info(watch_url, download=False)
                except Exception as exc:
                    err_text = str(exc) or " | ".join(bridge.snapshot_messages())
                    code, user_msg, retryable = classify_extraction_error(err_text)
                    last_err = YouTubeExtractionError(code, user_msg, raw_message=err_text, retryable=retryable)
                    logger.warning(
                        "YouTube extract error [tier=%s attempt=%d/%d code=%s]: %s",
                        tier.name, attempt, self.max_retries_per_tier, code, redact_sensitive_text(err_text),
                    )
                    if code in NON_RETRYABLE_CODES:
                        get_telemetry().record_provider_outcome(
                            "youtube", "extract_stream", False, (time.perf_counter() - t_op) * 1000.0, code,
                        )
                        raise last_err
                    if retryable and attempt < self.max_retries_per_tier:
                        if not self._wait_backoff(self._compute_backoff(attempt), cancel_event):
                            get_telemetry().record_provider_outcome(
                                "youtube", "extract_stream", False, (time.perf_counter() - t_op) * 1000.0,
                                ExtractionErrorCode.CANCELLED,
                            )
                            raise YouTubeExtractionError(ExtractionErrorCode.CANCELLED, "Extraction cancelled")
                        continue
                    break  # Step to next client tier

                validated = validate_and_select_audio_format(info, prefer_mp4a=prefer_mp4a)
                if validated and validated.get("url"):
                    validated["video_id"] = vid
                    validated["client_tier"] = tier.name
                    validated["extractor_warnings"] = bridge.snapshot_messages()
                    if vid and vid != "unknown":
                        with self._cache_lock:
                            self._stream_cache[vid] = _CachedStreamEntry(data=dict(validated))
                    logger.info(
                        "Extracted YouTube audio [vid=%s tier=%s ext=%s abr=%s exp=%s]",
                        vid, tier.name, validated["ext"], validated["abr"],
                        int(validated.get("expires_at") or 0),
                    )
                    get_telemetry().record_provider_outcome(
                        "youtube", "extract_stream", True, (time.perf_counter() - t_op) * 1000.0,
                    )
                    return validated

                # Format validation failed or info was empty -> inspect bridge messages for real reason
                diag = " | ".join(bridge.snapshot_messages()) or "No valid audio format found"
                code, user_msg, retryable = classify_extraction_error(diag)
                if code == ExtractionErrorCode.UNKNOWN:
                    code = ExtractionErrorCode.NO_VALID_FORMAT
                    user_msg = "No playable audio format returned by YouTube"
                last_err = YouTubeExtractionError(code, user_msg, raw_message=diag, retryable=retryable)
                logger.warning(
                    "YouTube format validation failed [tier=%s attempt=%d/%d code=%s]: %s",
                    tier.name, attempt, self.max_retries_per_tier, code, diag,
                )
                if code in NON_RETRYABLE_CODES:
                    get_telemetry().record_provider_outcome(
                        "youtube", "extract_stream", False, (time.perf_counter() - t_op) * 1000.0, code,
                    )
                    raise last_err
                if retryable and attempt < self.max_retries_per_tier:
                    if not self._wait_backoff(self._compute_backoff(attempt), cancel_event):
                        get_telemetry().record_provider_outcome(
                            "youtube", "extract_stream", False, (time.perf_counter() - t_op) * 1000.0,
                            ExtractionErrorCode.CANCELLED,
                        )
                        raise YouTubeExtractionError(ExtractionErrorCode.CANCELLED, "Extraction cancelled")
                    continue
                break

        get_telemetry().record_provider_outcome(
            "youtube", "extract_stream", False, (time.perf_counter() - t_op) * 1000.0, last_err.code,
        )
        raise last_err

    def extract_metadata(
        self,
        query_or_url: str,
        extract_flat: bool = False,
        cancel_event: Optional[threading.Event] = None,
    ) -> Optional[dict]:
        """
        Resilient search / metadata extraction via yt-dlp with non-silent redacted logging,
        transient backoff retry, and graceful tier selection.
        """
        if not query_or_url:
            return None

        t_op = time.perf_counter()
        vid = self.normalize_video_id(query_or_url) if not str(query_or_url).startswith("ytsearch") else ""
        # Flat search rarely needs PO-token tiers unless transient HTTP/network error happens
        tiers = self.client_tiers[:2] if extract_flat else self.client_tiers
        last_exc: Optional[Exception] = None
        last_code: str = ExtractionErrorCode.UNKNOWN

        for tier in tiers:
            for attempt in range(1, self.max_retries_per_tier + 1):
                if cancel_event and cancel_event.is_set():
                    get_telemetry().record_provider_outcome(
                        "youtube", "extract_metadata", False, (time.perf_counter() - t_op) * 1000.0,
                        ExtractionErrorCode.CANCELLED,
                    )
                    return None
                bridge = YtdlpLogBridge(logger)
                opts = self.build_ydl_opts(
                    video_id=vid,
                    tier=tier,
                    extract_flat=extract_flat,
                    log_bridge=bridge,
                )
                try:
                    with self._open_ydl(opts) as ydl:
                        info = ydl.extract_info(query_or_url, download=False)
                        if info:
                            get_telemetry().record_provider_outcome(
                                "youtube", "extract_metadata", True, (time.perf_counter() - t_op) * 1000.0,
                            )
                            return info
                except Exception as exc:
                    last_exc = exc
                    err_text = str(exc) or " | ".join(bridge.snapshot_messages())
                    code, _, retryable = classify_extraction_error(err_text)
                    last_code = code
                    logger.warning(
                        "YouTube metadata error [tier=%s attempt=%d/%d code=%s]: %s",
                        tier.name, attempt, self.max_retries_per_tier, code, redact_sensitive_text(err_text),
                    )
                    if code in NON_RETRYABLE_CODES:
                        get_telemetry().record_provider_outcome(
                            "youtube", "extract_metadata", False, (time.perf_counter() - t_op) * 1000.0, code,
                        )
                        raise YouTubeExtractionError(code, classify_extraction_error(err_text)[1], raw_message=err_text, retryable=False)
                    if retryable and attempt < self.max_retries_per_tier:
                        if not self._wait_backoff(self._compute_backoff(attempt), cancel_event):
                            get_telemetry().record_provider_outcome(
                                "youtube", "extract_metadata", False, (time.perf_counter() - t_op) * 1000.0,
                                ExtractionErrorCode.CANCELLED,
                            )
                            return None
                        continue
                    break

        get_telemetry().record_provider_outcome(
            "youtube", "extract_metadata", False, (time.perf_counter() - t_op) * 1000.0, last_code,
        )
        if last_exc:
            raise last_exc
        return None


_DEFAULT_EXTRACTOR: Optional[YouTubeExtractor] = None
_DEFAULT_LOCK = threading.Lock()


def get_youtube_extractor() -> YouTubeExtractor:
    """Process-wide singleton YouTubeExtractor."""
    global _DEFAULT_EXTRACTOR
    with _DEFAULT_LOCK:
        if _DEFAULT_EXTRACTOR is None:
            _DEFAULT_EXTRACTOR = YouTubeExtractor()
        return _DEFAULT_EXTRACTOR
