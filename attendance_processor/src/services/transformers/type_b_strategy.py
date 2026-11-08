from dataclasses import replace
from domain.models import AttendanceRow
from domain.time_math import shift_time_str, calculate_hours_difference
from src.services.transformers.base_strategy import BaseTransformationStrategy

class TypeBTransformationStrategy(BaseTransformationStrategy):
    """אסטרטגיית שינוי נתונים עבור דו"ח מסוג B (כולל הפסקה ושעות נוספות)."""

    def transform_row(self, row: AttendanceRow) -> AttendanceRow:
        if not row.entry_time or not row.exit_time:
            return row

        new_entry = shift_time_str(row.entry_time, 10)
        new_exit = shift_time_str(row.exit_time, 10)
        new_break = row.location_or_break  # הפסקה שמורה בשדה זה בסוג B

        # חישוב סך שעות בניכוי הפסקה
        new_total = calculate_hours_difference(new_entry, new_exit, new_break)

        return replace(
            row,
            entry_time=new_entry,
            exit_time=new_exit,
            total_hours=new_total,
            percentage_100=new_total, # לדוגמה, התאמה בסיסית
            percentage_125="00:00",
            percentage_150="00:00"
        )