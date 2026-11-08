"""הגדרות עמודות ומבנה ויזואלי עבור סוגי הדו"חות השונים (סוג A וסוג B)."""

from typing import Dict, List, Any
from domain.models import ReportType


# הגדרת מבנה עמודות עבור דו"ח סוג A
TYPE_A_COLUMNS: List[Dict[str, str]] = [
    {"key": "date", "label": "תאריך"},
    {"key": "day_of_week", "label": "יום"},
    {"key": "entry_time", "label": "כניסה"},
    {"key": "exit_time", "label": "יציאה"},
    {"key": "total_hours", "label": "סה\"כ שעות"},
    {"key": "notes", "label": "הערות"},
]

# הגדרת מבנה עמודות עבור דו"ח סוג B (כולל פירוט הפסקות/מיקום ואחוזים)
TYPE_B_COLUMNS: List[Dict[str, str]] = [
    {"key": "date", "label": "תאריך"},
    {"key": "day_of_week", "label": "יום בשבוע"},
    {"key": "entry_time", "label": "כניסה"},
    {"key": "exit_time", "label": "יציאה"},
    {"key": "location_or_break", "label": "הפסקה / מיקום"},
    {"key": "total_hours", "label": "סה\"כ שעות"},
    {"key": "percentage_100", "label": "100%"},
    {"key": "percentage_125", "label": "125%"},
    {"key": "percentage_150", "label": "150%"},
    {"key": "shabat", "label": "שבת/חג"},
    {"key": "notes", "label": "הערות"},
]


def get_layout_for_report_type(report_type: ReportType) -> List[Dict[str, str]]:
    """מחזיר את רשימת העמודות והכותרות המתאימה לפי סוג הדו"ח."""
    if report_type == ReportType.TYPE_A:
        return TYPE_A_COLUMNS
    elif report_type == ReportType.TYPE_B:
        return TYPE_B_COLUMNS
    else:
        raise ValueError(f"סוג דו\"ח לא מוכר: {report_type}")