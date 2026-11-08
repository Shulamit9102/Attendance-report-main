"""Interface for data parser components."""

from abc import ABC, abstractmethod
from typing import Any


class IParser(ABC):
    """Abstract interface for parsing raw attendance report data."""

    @abstractmethod
    def parse(self, raw_data: Any) -> Any:
        """Parse raw data into structured records."""
        pass