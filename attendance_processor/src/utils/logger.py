"""Centralized logging configuration."""

import logging
import sys
from typing import Final

DEFAULT_LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def get_logger(name: str) -> logging.Logger:
    """Get a standardized logger instance.

    Args:
        name: The name of the logger.

    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger