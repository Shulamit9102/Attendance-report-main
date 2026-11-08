from dataclasses import replace
from domain.models import AttendanceRow
from domain.time_math import shift_time_str, calculate_hours_difference
from src.services.transformers.base_strategy import BaseTransformationStrategy

class TypeATransformationStrategy(BaseTransformationStrategy):
    """אסטרטגיית שינוי נתונים עבור דו"ח מסוג A."""

    def transform_row(self, row: AttendanceRow) -> AttendanceRow:
        if not row.entry_time or not row.exit_time:
            return row

        # הזזת שעת כניסה ויציאה ב-15 דקות לדוגמה
        new_entry = shift_time_str(row.entry_time, 15)
        new_exit = shift_time_str(row.exit_time, 15)
        
        # חישוב מחדש של סך השעות
        new_total = calculate_hours_difference(new_entry, new_exit)

        return replace(
            row,
            entry_time=new_entry,
            exit_time=new_exit,
            total_hours=new_total
        )