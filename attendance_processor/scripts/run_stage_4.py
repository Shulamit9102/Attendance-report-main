"""סקריפט להרצה ובדיקה של שלב 4 - הטרנספורמציה."""

import sys
from pathlib import Path

# הוספת תיקיית השורש לנתיב כדי לאפשר ייבוא מודולים
sys.path.append(str(Path(__file__).resolve().parent.parent))

from domain.models import AttendanceReport, AttendanceRow, ReportType, ReportSummary
from src.services.transformers.data_transformer import DataTransformer


def run_transformation_stage():
    print("--- תחילת שלב 4: טרנספורמציה ---")

    # יצירת אובייקט דו"ח לדוגמה מסוג A (הנכנס משלב 3)
    sample_rows_a = [
        AttendanceRow(
            date="01/10/2026",
            day_of_week="חמישי",
            entry_time="08:00",
            exit_time="16:00",
            total_hours="08:00"
        ),
        AttendanceRow(
            date="02/10/2026",
            day_of_week="שישי",
            entry_time="08:30",
            exit_time="13:30",
            total_hours="05:00"
        ),
    ]
    report_a = AttendanceReport(
        report_type=ReportType.TYPE_A,
        rows=sample_rows_a,
        summary=ReportSummary(total_hours_sum="13:00")
    )

    # הרצת הטרנספורמציה
    transformer = DataTransformer()
    transformed_report_a = transformer.transform(report_a)

    print(f"\n[סוג {transformed_report_a.report_type.value}] תוצאות השינוי:")
    for original, updated in zip(report_a.rows, transformed_report_a.rows):
        print(f"  מקור: כניסה {original.entry_time} -> יציאה {original.exit_time} | סה\"כ: {original.total_hours}")
        print(f"  חדש:  כניסה {updated.entry_time} -> יציאה {updated.exit_time} | סה\"כ: {updated.total_hours}")
        print("-" * 40)

    # בדיקת אי-שינוי אובייקט המקור (Immutability Check)
    assert report_a.rows[0].entry_time == "08:00", "שגיאה: אובייקט המקור השתנה!"
    print("\n✓ בדיקה עברה: אובייקט המקור נשאר ללא שינוי.")


if __name__ == "__main__":
    run_transformation_stage()