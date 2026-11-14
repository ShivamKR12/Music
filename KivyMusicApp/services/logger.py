import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from kivy.utils import platform

def get_public_log_dir():
    if platform == 'android':
        base_dir = "/storage/emulated/0/Download/MusicAppLogs"
    else:
        base_dir = os.path.join(os.path.expanduser("~"), "Documents", "MusicAppLogs")
    try:
        os.makedirs(base_dir, exist_ok=True)
    except Exception:
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        os.makedirs(base_dir, exist_ok=True)
    return base_dir

log_file = os.path.join(get_public_log_dir(), "kivy_music_app.log")

app_logger = logging.getLogger("KivyMusicApp")
app_logger.setLevel(logging.INFO)

if app_logger.hasHandlers():
    app_logger.handlers.clear()

file_handler = RotatingFileHandler(log_file, maxBytes=2*1024*1024, backupCount=3, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
file_handler.setFormatter(formatter)
app_logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.__stdout__)
console_handler.setFormatter(formatter)
app_logger.addHandler(console_handler)

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Catches unhandled exceptions and writes full stack traces to disk before crashing."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    app_logger.critical("UNCAUGHT EXCEPTION CRASH:", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = global_exception_handler

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

def init_logging():
    app_logger.info("--- Application Session Started ---")
    app_logger.info(f"Logging initialized at: {log_file}")
    return app_logger
