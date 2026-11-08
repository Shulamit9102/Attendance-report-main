"""בדיקות יחידה עבור שלב הטרנספורמציה (שלב 4)."""

import pytest
from domain.models import AttendanceReport, AttendanceRow, ReportType
from domain.time_math import calculate_hours_difference, shift_time_str
from src.services.transformers.data_transformer import DataTransformer


@pytest.fixture
def sample_report_type_a():
    rows = [
        AttendanceRow(
            date="01/10/2026",
            day_of_week="חמישי",
            entry_time="08:00",
            exit_time="17:00",
            total_hours="09:00"
        )
    ]
    return AttendanceReport(report_type=ReportType.TYPE_A, rows=rows)


@pytest.fixture
def sample_report_type_b():
    rows = [
        AttendanceRow(
            date="01/10/2026",
            day_of_week="חמישי",
            entry_time="08:00",
            exit_time="17:00",
            location_or_break="01:00",  # הפסקה בסוג B
            total_hours="08:00"
        )
    ]
    return AttendanceReport(report_type=ReportType.TYPE_B, rows=rows)


def test_transformation_type_a(sample_report_type_a):
    """בדיקה שהטרנספורמציה לסוג A מזיזה זמנים ומחשבת מחדש סך שעות."""
    transformer = DataTransformer()
    result = transformer.transform(sample_report_type_a)

    assert isinstance(result, AttendanceReport)
    assert result.report_type == ReportType.TYPE_A
    assert len(result.rows) == 1

    updated_row = result.rows[0]
    # וידוא ששעת הכניסה והיציאה השתנו אך ההפרש נשמר תקין
    assert updated_row.entry_time != sample_report_type_a.rows[0].entry_time
    assert updated_row.total_hours == "09:00"


def test_transformation_type_b(sample_report_type_b):
    """בדיקה שהטרנספורמציה לסוג B מנכה הפסקה בחישוב השעות."""
    transformer = DataTransformer()
    result = transformer.transform(sample_report_type_b)

    assert result.report_type == ReportType.TYPE_B
    updated_row = result.rows[0]
    
    # בדיקה שהסך כולל ניכוי הפסקה (8 שעות נטו מתוך 9 שעות ברוטו)
    expected_total = calculate_hours_difference(
        updated_row.entry_time, 
        updated_row.exit_time, 
        updated_row.location_or_break
    )
    assert updated_row.total_hours == expected_total


def test_immutability(sample_report_type_a):
    """בדיקה שאובייקט המקור אינו משתנה בעקבות הטרנספורמציה."""
    original_entry = sample_report_type_a.rows[0].entry_time
    transformer = DataTransformer()
    _ = transformer.transform(sample_report_type_a)

    # האובייקט המקורי חייב להישאר זהה לחלוטין
    assert sample_report_type_a.rows[0].entry_time == original_entry


def test_deterministic_output(sample_report_type_a):
    """בדיקה ששתי הרצות על אותו קובץ נותנות פלט זהה."""
    transformer = DataTransformer()
    res1 = transformer.transform(sample_report_type_a)
    res2 = transformer.transform(sample_report_type_a)

    assert res1.rows[0].entry_time == res2.rows[0].entry_time
    assert res1.rows[0].exit_time == res2.rows[0].exit_time