"""End-to-end integration tests for the attendance processing pipeline."""

import pytest
from src.pipeline.pipeline_manager import PipelineManager
from src.constants.app_constants import PARSER_TYPE_A, PARSER_TYPE_B


def test_end_to_end_pdf_pipeline(tmp_path):
    """Test full processing pipeline with a PDF file and Parser A."""
    d = tmp_path / "reports"
    d.mkdir()
    file_path = d / "attendance.pdf"
    file_path.write_text("sample pdf data")

    pipeline = PipelineManager()
    result = pipeline.process_file(str(file_path), parser_type=PARSER_TYPE_A)

    assert result["status"] == "success"
    assert len(result["data"]) > 0
    assert result["data"][0]["source_layout"] == "A"


def test_end_to_end_excel_pipeline(tmp_path):
    """Test full processing pipeline with an Excel file and Parser B."""
    d = tmp_path / "reports"
    d.mkdir()
    file_path = d / "attendance.xlsx"
    file_path.write_text("sample excel data")

    pipeline = PipelineManager()
    result = pipeline.process_file(str(file_path), parser_type=PARSER_TYPE_B)

    assert result["status"] == "success"
    assert len(result["data"]) > 0
    assert result["data"][0]["source_layout"] == "B"


def test_end_to_end_invalid_file_format(tmp_path):
    """Test pipeline raises ValueError on unsupported file extension."""
    d = tmp_path / "reports"
    d.mkdir()
    file_path = d / "attendance.txt"
    file_path.write_text("sample text data")

    pipeline = PipelineManager()
    with pytest.raises(ValueError):
        pipeline.process_file(str(file_path))