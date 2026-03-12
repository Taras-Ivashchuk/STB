from loguru import logger
from core.settings import settings

logger.remove(0)
logger.add(
    sink=settings.LOG_DIR / settings.LOG_FILENAME,
    rotation="20 kb",
    level="DEBUG",
    retention=3,
)
