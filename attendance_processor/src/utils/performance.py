"""Performance monitoring utilities and execution timers."""

import time
import functools
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

class PerformanceTimer:
    """Context manager for measuring execution duration."""

    def __init__(self, operation_name: str) -> None:
        self.operation_name = operation_name
        self.start_time = 0.0
        self.duration = 0.0

    def __enter__(self) -> 'PerformanceTimer':
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.duration = time.perf_counter() - self.start_time
        logger.info(f"Performance Metrics: [{self.operation_name}] completed in {self.duration:.4f} seconds.")

def monitor_performance(operation_name: str) -> Callable:
    """Decorator to measure and log function execution time."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with PerformanceTimer(operation_name):
                return func(*args, **kwargs)
        return wrapper
    return decorator