"""Parser B implementation for alternative report layouts with robust regex extraction."""

import re
from typing import List, Optional
from domain.models import AttendanceReport, AttendanceRow, ReportSummary, ReportType
from src.services.parsers.base_parser import BaseParser


class ParserB(BaseParser):
    """פרסר ספציפי עבור דו"חות נוכחות מסוג B."""

    @property
    def report_type(self) -> ReportType:
        return ReportType.TYPE_B

    def _is_header_line(self, line: str) -> bool:
        """זיהוי שורות כותרת אמיתיות בסוג B."""
        # כותרת אמיתית תכיל לרוב שילוב של מספר מילות כותרת ולא רק מילה בודדת
        header_indicators = ["שעת כניסה", "שעת יציאה", "יום בשבוע"]
        return any(keyword in line for keyword in header_indicators)

    def _parse_row(self, line: str) -> Optional[AttendanceRow]:
        """מחלץ שורת נוכחות עבור מבנה B באמצעות Regex."""
        clean_line = re.sub(r'[\u200e\u200f\u202a-\u202e]', '', line)

        times = re.findall(r'\b\d{2}:\d{2}\b', clean_line)
        date_match = re.search(r'\b\d{2}/\d{2}/\d{4}\b', clean_line)
        date_str = date_match.group(0) if date_match else ""

        days_list = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
        day_str = ""
        for day in days_list:
            if day in clean_line:
                day_str = day
                break

        if not times and (not date_str or day_str != "שבת"):
            return None

        return AttendanceRow(
            date=date_str,
            day_of_week=day_str,
            entry_time=times[0] if len(times) > 0 else "",
            exit_time=times[1] if len(times) > 1 else "",
            total_hours=times[2] if len(times) > 2 else None,
            notes=clean_line
        )

    def _parse_summary(self, lines: List[str]) -> Optional[ReportSummary]:
        return None