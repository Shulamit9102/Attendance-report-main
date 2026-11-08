from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


class ReportType(Enum):
    TYPE_A = "TYPE_A"
    TYPE_B = "TYPE_B"


@dataclass(frozen=True)
class AttendanceRow:
    """שורה בודדת בדו"ח הנוכחות. מוגדרת כ-frozen כדי למנוע שינוי של המקור."""
    date: str
    day_of_week: str
    entry_time: str
    exit_time: str
    # שדות ייחודיים או משותפים בהתאם לסוג הדו"ח
    location_or_break: Optional[str] = None  # מקום.ע בסוג A / הפסקה בסוג B
    total_hours: Optional[str] = None
    # שדות נוספים לסוג A או B במידת הצורך
    percentage_100: Optional[str] = None
    percentage_125: Optional[str] = None
    percentage_150: Optional[str] = None
    notes: Optional[str] = None  # הערות סוג B


@dataclass(frozen=True)
class ReportSummary:
    """שורת סיכום של הדו"ח (קיימת בעיקר בסוג A)."""
    total_hours_sum: Optional[str] = None


@dataclass(frozen=True)
class AttendanceReport:
    """האובייקט המרכזי (החוזה) שמכיל את כל נתוני הדו"ח שעברו פרסור."""
    report_type: ReportType
    rows: Tuple[AttendanceRow, ...]
    summary: Optional[ReportSummary] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "rows", tuple(self.rows))