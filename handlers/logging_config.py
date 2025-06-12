import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
LOG_FILE = "bot.log"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(LOG_PATH, maxBytes=5*1024*1024, backupCount=3),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("yadisk_bot")