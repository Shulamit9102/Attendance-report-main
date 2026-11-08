"""Interface for file readers adhering to SOLID principles."""

from abc import ABC, abstractmethod
from typing import Any


class IFileReader(ABC):
    """Abstract interface for reading attendance report files."""

    @abstractmethod
    def read_file(self, file_path: str) -> Any:
        """Read data from the specified file path."""
        pass