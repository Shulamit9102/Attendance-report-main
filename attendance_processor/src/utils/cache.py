"""Thread-safe caching utility for attendance file processing results."""

import time
import threading
from typing import Any, Dict, Optional, Tuple

class AttendanceCache:
    """Thread-safe in-memory cache with TTL support."""

    def __init__(self, ttl_seconds: int = 3600) -> None:
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._lock = threading.Lock()
        self._ttl = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        """Retrieve cached item if it exists and has not expired."""
        with self._lock:
            if key not in self._cache:
                return None
            data, timestamp = self._cache[key]
            if time.time() - timestamp > self._ttl:
                del self._cache[key]
                return None
            return data

    def set(self, key: str, value: Any) -> None:
        """Store item in cache with current timestamp."""
        with self._lock:
            self._cache[key] = (value, time.time())

    def clear(self) -> None:
        """Clear all cached entries."""
        with self._lock:
            self._cache.clear()