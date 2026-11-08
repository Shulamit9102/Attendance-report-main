from abc import ABC, abstractmethod
from domain.models import AttendanceReport

class ITransformer(ABC):
    """ממשק אבסטרקטי לביצוע טרנספורמציה על דו'ח נוכחות."""

    @abstractmethod
    def transform(self, report: AttendanceReport) -> AttendanceReport:
        """מקבל דו'ח נוכחות ומחזיר דו'ח מעודכן (חדש)."""
        pass