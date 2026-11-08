"""Unit tests for AttendanceCache."""

import time
from src.utils.cache import AttendanceCache

def test_cache_set_and_get() -> None:
    cache = AttendanceCache(ttl_seconds=2)
    cache.set("key1", "val1")
    assert cache.get("key1") == "val1"

def test_cache_expiry() -> None:
    cache = AttendanceCache(ttl_seconds=1)
    cache.set("key2", "val2")
    time.sleep(1.1)
    assert cache.get("key2") is None

def test_cache_clear() -> None:
    cache = AttendanceCache()
    cache.set("key3", "val3")
    cache.clear()
    assert cache.get("key3") is None