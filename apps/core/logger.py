import sys
from loguru import logger
from .constants import LOG_DIR

LOG_FORMAT = "<green>{time:HH:mm:ss}</green> | <level>{level}</level> | " \
             "{name}:{function}:{line} - {message} | extra={extra}"

logger.remove()

LOG_DIR.mkdir(exist_ok=True)

logger.add(LOG_DIR / "logs.log",
           rotation="10 MB",
           retention="10 days",
           compression="zip",
           level="INFO",
           format=LOG_FORMAT)

logger.add(sys.stdout, colorize=True, level="DEBUG", format=LOG_FORMAT)
