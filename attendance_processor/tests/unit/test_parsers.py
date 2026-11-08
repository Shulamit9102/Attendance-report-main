# tests/unit/test_parsers.py
import pytest
from domain.models import ReportType
from src.services.parsers.parser_a import ParserA
from src.services.parsers.parser_b import ParserB

def test_parser_a():
    """בדיקת פרסור תקין של דו"ח מסוג A."""
    sample_text = "07/02/2023 שלישי גונן 08:00 16:00 00:30 7.50 7.50 0.00 0.00 0.00"
    parser = ParserA()
    report = parser.parse(sample_text)
    
    assert report.report_type == ReportType.TYPE_A
    assert len(report.rows) == 1
    assert report.rows[0].entry_time == "08:00"
    assert report.rows[0].exit_time == "16:00"

def test_parser_b():
    """בדיקת פרסור תקין של דו"ח מסוג B."""
    sample_text = "01/10/2026 ראשון 08:00 17:00 08:00 טקסט חופשי"
    parser = ParserB()
    report = parser.parse(sample_text)
    
    assert report.report_type == ReportType.TYPE_B
    assert len(report.rows) == 1
    assert report.rows[0].entry_time == "08:00"
    assert report.rows[0].exit_time == "17:00"


@pytest.mark.parametrize(
    ("parser_class", "sample_text"),
    [
        (ParserA, "07/02/2023 שבת"),
        (ParserB, "07/02/2023 שבת"),
    ],
)
def test_saturday_without_hours_is_preserved(parser_class, sample_text):
    report = parser_class().parse(sample_text)

    assert len(report.rows) == 1
    saturday = report.rows[0]
    assert saturday.day_of_week == "שבת"
    assert saturday.entry_time == ""
    assert saturday.exit_time == ""
    assert saturday.total_hours is None


def test_parser_empty_text_raises_error():
    """בדיקה שטקסט ריק זורק שגיאה."""
    parser = ParserA()
    with pytest.raises(ValueError):
        parser.parse("")