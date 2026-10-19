import os
import sys
import logging
import traceback
from logging.handlers import RotatingFileHandler
from kivy.utils import platform

def get_public_log_dir():
    if platform == 'android':
        # On Android, the standard public external storage path is usually the Download or Documents folder.
        # This allows the user to access it easily via a standard File Manager app.
        base_dir = "/storage/emulated/0/Download/MusicAppLogs"
    else:
        # On Windows/Desktop, use the user's Documents folder
        base_dir = os.path.join(os.path.expanduser("~"), "Documents", "MusicAppLogs")
    
    try:
        os.makedirs(base_dir, exist_ok=True)
    except Exception as e:
        # Fallback to current directory if permissions are heavily restricted
        base_dir = "logs"
        os.makedirs(base_dir, exist_ok=True)
        
    return base_dir

log_file = os.path.join(get_public_log_dir(), "music_app.log")

# Setup the root logger
app_logger = logging.getLogger("MusicApp")
app_logger.setLevel(logging.INFO)

# Clear existing handlers if imported multiple times
if app_logger.hasHandlers():
    app_logger.handlers.clear()

# 1. Use RotatingFileHandler to prevent the file from becoming a "heap of garbage"
# Max 2 MB per file, keep up to 3 backups (music_app.log, music_app.log.1, etc.)
file_handler = RotatingFileHandler(log_file, maxBytes=2*1024*1024, backupCount=3, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
file_handler.setFormatter(formatter)
app_logger.addHandler(file_handler)

# 2. Also log to console (useful for IDE monitoring)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
app_logger.addHandler(console_handler)

# Global Unhandled Exception Hook (Crisis Preparation)
def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Catches unhandled exceptions and writes them to the log file before crashing."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    app_logger.critical("UNCAUGHT EXCEPTION CRASH:", exc_info=(exc_type, exc_value, exc_traceback))

# Register the crash hook
sys.excepthook = global_exception_handler

# Redirect standard print() statements and errors to our logger
class StreamToLogger(object):
    def __init__(self, logger_instance, log_level=logging.INFO):
        self.logger = logger_instance
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            if line.strip():
                self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

sys.stdout = StreamToLogger(app_logger, logging.INFO)
sys.stderr = StreamToLogger(app_logger, logging.ERROR)

app_logger.info("--- Application Session Started ---")
app_logger.info(f"Logging initialized at: {log_file}")
