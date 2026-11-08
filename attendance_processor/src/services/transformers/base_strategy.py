from abc import ABC, abstractmethod
from domain.models import AttendanceRow, AttendanceReport

class BaseTransformationStrategy(ABC):
    """מחלקת בסיס אבסטרקטית לאסטרטגיות שינוי נתוני הנוכחות."""

    @abstractmethod
    def transform_row(self, row: AttendanceRow) -> AttendanceRow:
        """משנה שורה בודדת ומחזירה שורה חדשה ומעודכנת."""
        pass

    def transform_report(self, report: AttendanceReport) -> AttendanceReport:
        """מריצה את הטרנספורמציה על כל שורות הדו"ח ומחזירה דו"ח חדש."""
        new_rows = [self.transform_row(row) for row in report.rows]
        return AttendanceReport(
            report_type=report.report_type,
            rows=new_rows,
            summary=report.summary
        )