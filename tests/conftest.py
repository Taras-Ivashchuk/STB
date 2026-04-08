import pytest
from app_logger import logger


@pytest.fixture(autouse=True)
def disable_loguru():
    logger.remove()
