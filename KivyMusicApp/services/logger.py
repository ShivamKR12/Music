import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from kivy.utils import platform
from kivy.logger import Logger as kivy_logger

# ==============================================================================
# 1. 5-LEVEL CANONICAL LOG SYSTEM
# ==============================================================================
class LogLevel:
    """
    Canonical 5-Level Logging System for Melodify/KivyMusicApp.
    1. DEBUG    (10) - Detailed diagnostic tracing for debugging
    2. INFO     (20) - Routine operational events and progress indicators
    3. WARNING  (30) - Non-fatal recoverable anomalies or deprecations
    4. ERROR    (40) - Failures preventing completion of an operation
    5. CRITICAL (50) - Severe system failures, crashes, or unhandled exceptions
    """
    DEBUG = logging.DEBUG         # 10
    INFO = logging.INFO           # 20
    WARNING = logging.WARNING     # 30
    ERROR = logging.ERROR         # 40
    CRITICAL = logging.CRITICAL   # 50

    LEVELS = {
        "DEBUG": DEBUG,
        "INFO": INFO,
        "WARNING": WARNING,
        "ERROR": ERROR,
        "CRITICAL": CRITICAL,
    }

    LEVEL_NAMES = {
        DEBUG: "DEBUG",
        INFO: "INFO",
        WARNING: "WARNING",
        ERROR: "ERROR",
        CRITICAL: "CRITICAL",
    }

    @classmethod
    def from_str(cls, name: str, default=INFO) -> int:
        """Parses a string log level (case-insensitive) to its integer constant."""
        if not name:
            return default
        clean = str(name).strip().upper()
        if clean == "WARN":
            clean = "WARNING"
        elif clean == "FATAL":
            clean = "CRITICAL"
        return cls.LEVELS.get(clean, default)

    @classmethod
    def to_str(cls, level: int) -> str:
        """Converts an integer level constant to canonical string."""
        return cls.LEVEL_NAMES.get(int(level), "INFO")

    @classmethod
    def all_names(cls):
        """Returns ordered list of all 5 level names."""
        return ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


# ==============================================================================
# 2. LOG DIRECTORY & ROTATING FILE HANDLER RESOLUTION
# ==============================================================================
def get_public_log_dir() -> str:
    """Resolves a writable persistent log directory across Android and Desktop platforms."""
    candidates = []
    if platform == 'android':
        android_priv = os.environ.get("ANDROID_PRIVATE")
        if android_priv:
            candidates.append(os.path.join(android_priv, "logs"))
        try:
            from jnius import autoclass
            act = autoclass("org.kivy.android.PythonActivity").mActivity
            if act:
                ext_dir = act.getExternalFilesDir(None)
                if ext_dir:
                    candidates.insert(0, os.path.join(str(ext_dir.getAbsolutePath()), "logs"))
        except Exception:
            pass
    else:
        candidates.append(os.path.join(os.path.expanduser("~"), "Documents", "MusicAppLogs"))

    candidates.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs"))

    for base_dir in candidates:
        try:
            os.makedirs(base_dir, exist_ok=True)
            probe_path = os.path.join(base_dir, ".write_probe")
            with open(probe_path, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe_path)
            return base_dir
        except Exception:
            continue

    fallback = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    try:
        os.makedirs(fallback, exist_ok=True)
    except Exception:
        pass
    return fallback

log_file = os.path.join(get_public_log_dir(), "kivy_music_app.log")

_kivy_file_handler = None

def _setup_kivy_file_handler():
    """Attaches a rotating file handler to Kivy's core Logger instance."""
    global _kivy_file_handler
    if _kivy_file_handler is not None:
        return _kivy_file_handler

    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        # Max 2MB per file with 3 rotating backups (max ~8MB total on disk)
        _kivy_file_handler = RotatingFileHandler(
            log_file,
            maxBytes=2 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8'
        )
        formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)-7s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        _kivy_file_handler.setFormatter(formatter)
        _kivy_file_handler.setLevel(logging.DEBUG)

        # Attach to Kivy Logger so all Kivy & App log records are preserved on disk
        kivy_logger.addHandler(_kivy_file_handler)
    except Exception as e:
        print(f"[Logger init fallback error]: {e}")
    return _kivy_file_handler


# ==============================================================================
# 3. SCOPED LOGGER FOR SYSTEMS & SUB-SYSTEMS
# ==============================================================================
class ScopedLogger:
    """
    Subsystem-scoped logger that wires through Kivy's core Logger.
    Formats logs as '{subsystem}: {message}' so Kivy's ColonSplittingLogRecord
    automatically renders them with clean subsystem tags in console and logcat.
    """
    def __init__(self, name: str):
        self.name = str(name).strip()

    def _fmt(self, msg, args):
        if args:
            try:
                msg = str(msg) % args
            except Exception:
                msg = f"{msg} {' '.join(str(a) for a in args)}"
        return f"{self.name}: {msg}"

    # --- 1. DEBUG (Level 10) ---
    def debug(self, msg, *args, **kwargs):
        """Logs detailed diagnostic and internal tracing information."""
        if not kivy_logger.isEnabledFor(logging.DEBUG):
            return
        kivy_logger.debug(self._fmt(msg, args), **kwargs)

    # --- 2. INFO (Level 20) ---
    def info(self, msg, *args, **kwargs):
        """Logs normal lifecycle milestones and confirmation events."""
        if not kivy_logger.isEnabledFor(logging.INFO):
            return
        kivy_logger.info(self._fmt(msg, args), **kwargs)

    # --- 3. WARNING (Level 30) ---
    def warning(self, msg, *args, **kwargs):
        """Logs recoverable non-fatal anomalies, retries, or unexpected state."""
        if not kivy_logger.isEnabledFor(logging.WARNING):
            return
        kivy_logger.warning(self._fmt(msg, args), **kwargs)

    def warn(self, msg, *args, **kwargs):
        """Alias for warning."""
        self.warning(msg, *args, **kwargs)

    # --- 4. ERROR (Level 40) ---
    def error(self, msg, *args, **kwargs):
        """Logs operation failures, caught exceptions, or degraded performance."""
        if not kivy_logger.isEnabledFor(logging.ERROR):
            return
        kivy_logger.error(self._fmt(msg, args), **kwargs)

    # --- 5. CRITICAL (Level 50) ---
    def critical(self, msg, *args, **kwargs):
        """Logs fatal conditions, data corruption risks, or impending crashes."""
        if not kivy_logger.isEnabledFor(logging.CRITICAL):
            return
        kivy_logger.critical(self._fmt(msg, args), **kwargs)

    def fatal(self, msg, *args, **kwargs):
        """Alias for critical."""
        self.critical(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """Logs an ERROR or CRITICAL event accompanied by complete exception traceback."""
        kivy_logger.exception(self._fmt(msg, args), **kwargs)

    def log(self, level, msg, *args, **kwargs):
        """Logs a message at arbitrary numeric log level."""
        kivy_logger.log(level, self._fmt(msg, args), **kwargs)

    def isEnabledFor(self, level) -> bool:
        """Checks whether the given level is enabled on Kivy Logger."""
        return kivy_logger.isEnabledFor(level)

    def is_enabled_for(self, level) -> bool:
        return self.isEnabledFor(level)

    def setLevel(self, level):
        """Sets the system-wide log level."""
        set_log_level(level)

    def set_level(self, level):
        self.setLevel(level)

    def getEffectiveLevel(self) -> int:
        return kivy_logger.getEffectiveLevel()

    @property
    def handlers(self):
        return kivy_logger.handlers

    def hasHandlers(self) -> bool:
        return kivy_logger.hasHandlers()

    def addHandler(self, h):
        kivy_logger.addHandler(h)

    def removeHandler(self, h):
        kivy_logger.removeHandler(h)


_loggers = {}

def get_logger(name: str = "App") -> ScopedLogger:
    """Returns or registers a ScopedLogger for a specific system or sub-system."""
    clean_name = str(name).strip() if name else "App"
    if clean_name not in _loggers:
        _loggers[clean_name] = ScopedLogger(clean_name)
    return _loggers[clean_name]

# Primary default application logger
app_logger = get_logger("MusicApp")


# ==============================================================================
# 4. SYSTEM-WIDE LOG LEVEL CONFIGURATION
# ==============================================================================
def set_log_level(level):
    """
    Sets log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    consistently across Kivy's core Logger, Kivy Config, and file handlers.
    """
    if isinstance(level, str):
        level_int = LogLevel.from_str(level)
        level_str = LogLevel.to_str(level_int).lower()
    else:
        level_int = int(level)
        level_str = LogLevel.to_str(level_int).lower()

    # 1. Kivy core Logger level
    kivy_logger.setLevel(level_int)

    # 2. Kivy configuration entry
    try:
        from kivy.config import Config
        Config.set('kivy', 'log_level', level_str)
    except Exception:
        pass

    # 3. Rotating file handler
    if _kivy_file_handler:
        _kivy_file_handler.setLevel(level_int)

    # 4. Standard Python root logger
    logging.getLogger("KivyMusicApp").setLevel(level_int)
    logging.getLogger().setLevel(level_int)

def get_current_log_level_name() -> str:
    """Returns current effective log level as human-readable string."""
    return LogLevel.to_str(kivy_logger.getEffectiveLevel())


# ==============================================================================
# 5. GLOBAL UNCAUGHT EXCEPTION CRASH HANDLER
# ==============================================================================
def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Catches unhandled exceptions and writes full stack traces to disk before crashing."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    kivy_logger.critical("Crash: UNCAUGHT EXCEPTION", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = global_exception_handler


# ==============================================================================
# 6. STREAM TO LOGGER (STDOUT/STDERR ADAPTER)
# ==============================================================================
class StreamToLogger:
    def __init__(self, logger_instance, log_level=logging.INFO):
        self.logger = logger_instance
        self.log_level = log_level

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            if line.strip():
                self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


# ==============================================================================
# 7. INITIALIZATION LIFECYCLE
# ==============================================================================
def init_logging(initial_level=None):
    """
    Initializes the 5-level logging system:
    - Attaches rotating file handler to Kivy's core Logger
    - Suppresses third-party noise (Pillow, urllib3)
    - Loads persisted log level from SQLite if available, else defaults to INFO
    - Emits session startup banner with system paths and active level
    """
    # 1. Suppress verbose debug logs from third-party libraries
    for lib in ("PIL", "PIL.Image", "PIL.PngImagePlugin", "urllib3"):
        logging.getLogger(lib).setLevel(logging.WARNING)

    # 2. Setup rotating file handler attached to Kivy core Logger
    _setup_kivy_file_handler()

    # 3. Determine active level
    target_level = initial_level
    if not target_level:
        try:
            from models.database import get_setting
            db_level = get_setting("log_level", "INFO")
            target_level = db_level if db_level else "INFO"
        except Exception:
            target_level = "INFO"

    set_log_level(target_level)

    # 4. Session startup banner
    app_logger.info("--- Application Session Started ---")
    app_logger.info(f"Logging initialized at: {log_file}")
    app_logger.info(f"Active 5-level log threshold: {get_current_log_level_name()}")
    return app_logger
