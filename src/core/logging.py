import os
import sys
from loguru import logger
from src.core.config import settings

LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/userhub.log")

logger.remove()

log_level = settings.log_level.upper()

logger.add(
    sys.stderr,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    ),
    level=log_level,
)

logger.add(
    LOG_FILE_PATH,
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - " "{message}"
    ),
    level=log_level,
)

logger = logger.bind(service="UserService")

logger.info("Logging setup completed successfully for UserService.")
