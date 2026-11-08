"""Interface for attendance data exporters."""
from abc import ABC, abstractmethod
from domain.models import AttendanceReport

class AttendanceExporterInterface(ABC):
    """Abstract base class defining the exporter contract for AttendanceReport."""

    @abstractmethod
    def export(self, report: AttendanceReport, output_path: str) -> None:
        """Export an AttendanceReport object to a specific file format."""
        pass
    