"""Resilience and error-handling utilities for robust file processing."""

import logging
import functools
from typing import Callable, Any, Dict

logger = logging.getLogger(__name__)

def robust_execution(default_return: Any = None) -> Callable:
    """Decorator to catch unexpected runtime exceptions and ensure pipeline resilience."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Resilience caught exception in {func.__name__}: {e}", exc_info=True)
                return {"status": "error", "error": str(e), "data": default_return}
        return wrapper
    return decorator