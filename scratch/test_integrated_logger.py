import os
import sys

# Test logger implementation
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
        base_dir = "logs"
        os.makedirs(base_dir, exist_ok=True)
    return base_dir

def setup_app_logger():
    log_dir = get_public_log_dir()
    log_file = os.path.join(log_dir, "kivy_music_app.log")
    
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
    
    app_logger.info("Integrated logger initialized successfully.")
    return app_logger, log_file

def test():
    logger, log_file = setup_app_logger()
    logger.info("Test logging message 12345")
    assert os.path.exists(log_file)
    with open(log_file, "r", encoding="utf-8") as f:
        data = f.read()
        assert "Test logging message 12345" in data
    print("Integrated logger test passed!")

if __name__ == "__main__":
    test()
