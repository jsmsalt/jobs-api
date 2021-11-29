import sys

from loguru import logger
from os.path import join

logger.remove()

logger.add(
    sink=join("logs", "warnings_errors.log"),
    rotation="100 MB",
    retention="30 days",
    format="{time} - {level} - {message}",
    level="WARNING"
)

logger.add(
    sink=sys.stdout,
    colorize=True,
    format="<green>{time}</green> <level>{level}</level> {message}",
    level="DEBUG"
)
