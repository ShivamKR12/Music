import os
import sys
import logging
from logging.handlers import RotatingFileHandler

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

def test_stream_logger():
    test_logger = logging.getLogger("TestStreamApp")
    test_logger.setLevel(logging.INFO)
    
    # Write to original underlying stdout to avoid recursion
    console_handler = logging.StreamHandler(sys.__stdout__)
    test_logger.addHandler(console_handler)
    
    orig_stdout = sys.stdout
    sys.stdout = StreamToLogger(test_logger, logging.INFO)
    
    try:
        print("Hello from redirected print!")
    finally:
        sys.stdout = orig_stdout
        
    print("Stream logger test passed without recursion!")

if __name__ == "__main__":
    test_stream_logger()
