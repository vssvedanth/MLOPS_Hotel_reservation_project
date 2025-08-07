# src/logger.py
import logging
import os
from datetime import datetime
import sys  # <--- You need to add this line

# Define the directory for logs
LOGS_DIR = "logs"
# Create the logs directory if it doesn't exist
os.makedirs(LOGS_DIR, exist_ok=True)

# Define the log file name with the current date
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# Configure the basic logging settings
logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO # Set the logging level to INFO
)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance with the specified name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO) # Ensure the logger level is INFO
    # Prevent duplicate handlers if called multiple times in the same run
    if not logger.handlers:
        # Add a console handler for output to the terminal as well
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger