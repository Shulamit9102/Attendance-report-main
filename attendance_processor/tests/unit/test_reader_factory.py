"""Unit tests for ReaderFactory."""

import pytest
from src.services.factories.reader_factory import ReaderFactory
from src.services.file_readers.pdf_file_reader import PdfFileReader
from src.services.file_readers.excel_file_reader import ExcelFileReader
from src.constants.app_constants import FILE_TYPE_PDF, FILE_TYPE_EXCEL


def test_factory_creates_pdf_reader():
    """Test that factory correctly instantiates PdfFileReader."""
    reader = ReaderFactory.create_reader(FILE_TYPE_PDF)
    assert isinstance(reader, PdfFileReader)


def test_factory_creates_excel_reader():
    """Test that factory correctly instantiates ExcelFileReader."""
    reader = ReaderFactory.create_reader(FILE_TYPE_EXCEL)
    assert isinstance(reader, ExcelFileReader)


def test_factory_unsupported_type():
    """Test that factory raises ValueError for unsupported file types."""
    with pytest.raises(ValueError):
        ReaderFactory.create_reader("UNSUPPORTED")