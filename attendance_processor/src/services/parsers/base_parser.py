from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models import AttendanceReport, AttendanceRow, ReportSummary, ReportType


class BaseParser(ABC):
    """מחלקת בסיס אבסטרקטית המיישמת את תבנית Template Method לפרסור דו"חות."""

    @property
    @abstractmethod
    def report_type(self) -> ReportType:
        """מחזיר את סוג הדו"ח שהפרסר מטפל בו."""
        pass

    def parse(self, raw_text: str) -> AttendanceReport:
        """תהליך הפרסור המשותף לכל סוגי הדו"חות."""
        if not raw_text:
            raise ValueError("הטקסט הגולמי ריק, לא ניתן לבצע פרסור.")

        # ניקוי הטקסט וחלוקה לשורות
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

        summary = self._parse_summary(lines)
        
        rows: List[AttendanceRow] = []
        for line in lines:
            if not self._is_header_line(line) and not self._is_summary_line(line):
                row = self._parse_row(line)
                if row:
                    rows.append(row)

        return AttendanceReport(
            report_type=self.report_type,
            rows=rows,
            summary=summary
        )

    @abstractmethod
    def _parse_row(self, line: str) -> Optional[AttendanceRow]:
        """מחלץ שורת נוכחות מתוך שורת טקסט (ממומש באופן ייחודי לכל סוג)."""
        pass

    @abstractmethod
    def _parse_summary(self, lines: List[str]) -> Optional[ReportSummary]:
        """מחלץ את שורת הסיכום של הדו"ח."""
        pass

    @abstractmethod
    def _is_header_line(self, line: str) -> bool:
        """בודק האם השורה היא שורת כותרת שיש לדלג עליה."""
        pass

    def _is_summary_line(self, line: str) -> bool:
        """בודק האם השורה היא שורת סיכום (ניתן לדרוס במידת הצורך)."""
        return False