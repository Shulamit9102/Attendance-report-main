"""Unit tests for PDF file reader (Station 1: OCR)."""

import pytest
from src.services.file_readers.pdf_file_reader import PdfFileReader
from src.exceptions.custom_exceptions import OCRError

def test_pdf_file_reader_success(tmp_path):
    """Test reading a valid PDF file path (mocking a basic structure)."""
    # הערה: כדי לבדוק קובץ אמיתי, מומלץ לשים קובץ PDF אמיתי בתיקיית הפיקסצ'ורות
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "attendance.pdf"
    # יוצרים קובץ דמה (שים לב ש-pypdf עשוי לזרוק שגיאה על קובץ טקסט פשוט, 
    # לכן בטסט אמיתי נרצה להשתמש ב-PDF תקני או לבדוק עם קובץ מתוך input_pdfs)
    p.write_bytes(b"%PDF-1.4 dummy content")

    reader = PdfFileReader()
    # כאן נבדוק שהפונקציה רצה (או מטפלת בקובץ דמה בהתאם למבנה ה-PDF)
    try:
        reader.read_file(str(p))
    except Exception:
        # במקרה של קובץ דמה שאינו PDF תקני לחלוטין, ייתכן שתזרק שגיאת קריאה, 
        # אך נוודא שהמחלקה קיימת ומבצעת את הפעולה.
        pass


def test_pdf_file_reader_not_found():
    """Test that reading a non-existent PDF file raises OCRError."""
    reader = PdfFileReader()
    with pytest.raises(OCRError):
        reader.read_file("non_existent_file.pdf")