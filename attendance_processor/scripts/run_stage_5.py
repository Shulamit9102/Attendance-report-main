"""סקריפט להרצה ובדיקה של שלב 5 - הפקת ה-PDF/HTML."""

import sys
from pathlib import Path

# הוספת תיקיית השורש לנתיב
sys.path.append(str(Path(__file__).resolve().parent.parent))

from domain.models import AttendanceReport, AttendanceRow, ReportType, ReportSummary
from src.services.exporters.pdf_renderer import PdfRenderer
from src.exceptions.custom_exceptions import ExportError


def run_generation_stage():
    print("--- תחילת שלב 5: הפקת דו\"ח (Generator) ---")

    # יצירת נתוני דמה לדו"ח מסוג A
    sample_rows = [
        AttendanceRow(
            date="01/10/2026",
            day_of_week="חמישי",
            entry_time="08:15",
            exit_time="16:15",
            total_hours="08:00",
            notes="תקין"
        ),
        AttendanceRow(
            date="02/10/2026",
            day_of_week="שישי",
            entry_time="08:45",
            exit_time="13:45",
            total_hours="05:00",
            notes="ערב שבת"
        ),
    ]
    
    report = AttendanceReport(
        report_type=ReportType.TYPE_A,
        rows=sample_rows,
        summary=ReportSummary(total_hours_sum="13:00")
    )

    # הפקת הקובץ
    output_path = "output_attendance_report.pdf"
    renderer = PdfRenderer()

    try:
        renderer.render(report, output_path)
        print(f"\n✓ הדו\"ח הופק בהצלחה ונשמר בנתיב: {output_path}")
    except ExportError as e:
        print(f"\n⚠ הערה בהפקת הדו\"ח: {e}")
        # אם weasyprint לא מותקן, הרנדרר שומר אוטומטית כ-HTML לבדיקה
        html_fallback = Path(output_path).with_suffix('.html')
        if html_fallback.exists():
            print(f"✓ נוצר קובץ HTML גיבוי בנתיב: {html_fallback}")


if __name__ == "__main__":
    run_generation_stage()