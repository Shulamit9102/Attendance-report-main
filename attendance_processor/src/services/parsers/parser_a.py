"""Parser A implementation for primary report layouts with robust header filtering."""

import re
from typing import List, Optional
from domain.models import AttendanceReport, AttendanceRow, ReportSummary, ReportType
from src.services.parsers.base_parser import BaseParser


class ParserA(BaseParser):
    """פרסר ספציפי עבור דו"חות נוכחות מסוג A."""

    @property
    def report_type(self) -> ReportType:
        return ReportType.TYPE_A

    def _is_header_line(self, line: str) -> bool:
        """זיהוי שורות כותרת אמיתיות בסוג A על פי שילוב מספר מילות מפתח."""
        header_indicators = ["שם החברה", "עובד", "תאריך", "כניסה", "יציאה"]
        # דורש לפחות שתי מילות מפתח כדי לוודא שזו שורת כותרת אמיתית
        matches = sum(1 for keyword in header_indicators if keyword in line)
        return matches >= 2

    def _is_summary_line(self, line: str) -> bool:
        return "סה\"כ" in line or "סיכום" in line

    def _parse_row(self, line: str) -> Optional[AttendanceRow]:
        """מחלץ שורת נוכחות בצורה מדויקת באמצעות Regex וסינון תווי OCR."""
        clean_line = re.sub(r'[\u200e\u200f\u202a-\u202e]', '', line)

        times = re.findall(r'\b\d{2}:\d{2}\b', clean_line)
        if not times:
            return None

        date_match = re.search(r'\b\d{2}/\d{2}/\d{4}\b', clean_line)
        date_str = date_match.group(0) if date_match else ""

        days_list = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
        day_str = ""
        for day in days_list:
            if day in clean_line:
                day_str = day
                break

        return AttendanceRow(
            date=date_str,
            day_of_week=day_str,
            entry_time=times[0] if len(times) > 0 else "",
            exit_time=times[1] if len(times) > 1 else "",
            total_hours=times[3] if len(times) > 3 else (times[2] if len(times) > 2 else None),
            notes=clean_line
        )

    def _parse_summary(self, lines: List[str]) -> Optional[ReportSummary]:
        for line in lines:
            if self._is_summary_line(line):
                return ReportSummary(total_hours_sum=line)
        return None