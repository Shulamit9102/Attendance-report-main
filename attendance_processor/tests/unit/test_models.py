from dataclasses import FrozenInstanceError

import pytest

from domain.models import AttendanceReport, AttendanceRow, ReportSummary, ReportType


def test_report_models_are_frozen_and_rows_are_a_tuple():
    row = AttendanceRow(date="01/10/2026", day_of_week="חמישי", entry_time="08:00", exit_time="17:00")
    summary = ReportSummary(total_hours_sum="09:00")
    report = AttendanceReport(report_type=ReportType.TYPE_A, rows=[row], summary=summary)

    assert isinstance(report.rows, tuple)
    with pytest.raises(FrozenInstanceError):
        report.rows = ()
    with pytest.raises(FrozenInstanceError):
        summary.total_hours_sum = "10:00"
    with pytest.raises(FrozenInstanceError):
        row.date = "02/10/2026"
