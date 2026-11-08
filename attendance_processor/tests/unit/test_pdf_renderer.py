"""בדיקות יחידה עבור רנדרר ה-PDF / HTML (שלב 5)."""

import pytest
from pathlib import Path
from domain.models import AttendanceReport, AttendanceRow, ReportType, ReportSummary
from src.services.exporters.pdf_renderer import PdfRenderer


@pytest.fixture
def sample_report():
    rows = [
        AttendanceRow(
            date="01/10/2026",
            day_of_week="חמישי",
            entry_time="08:00",
            exit_time="17:00",
            total_hours="09:00"
        )
    ]
    return AttendanceReport(
        report_type=ReportType.TYPE_A,
        rows=rows,
        summary=ReportSummary(total_hours_sum="09:00")
    )


def test_html_generation_content(sample_report):
    """בדיקה שמחולל ה-HTML מייצר את התגיות והנתונים הנדרשים בהתאם לדו"ח."""
    renderer = PdfRenderer()
    html_content = renderer._generate_html(sample_report, renderer._PdfRenderer__get_columns_safely(sample_report.report_type) if hasattr(renderer, '_PdfRenderer__get_columns_safely') else __import__('src.services.exporters.layouts', fromlist=['get_layout_for_report_type']).get_layout_for_report_type(sample_report.report_type))

    # וידוא שנתוני המפתח קיימים ב-HTML
    assert "01/10/2026" in html_content
    assert "08:00" in html_content
    assert "09:00" in html_content
    assert "dir=\"rtl\"" in html_content  # וידוא תמיכה בכיווניות עברית


def test_renderer_empty_report(tmp_path):
    """בדיקה שהרנדרר מטפל נכון בדו"ח ריק ללא שגיאות קריטיות."""
    empty_report = AttendanceReport(report_type=ReportType.TYPE_A, rows=[])
    renderer = PdfRenderer()
    
    output_file = tmp_path / "empty_report.pdf"
    # לא אמור לזרוק שגיאה חריגה, אלא לסיים בבטחה
    renderer.render(empty_report, str(output_file))