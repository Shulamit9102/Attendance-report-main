"""PDF file reader implementation with OCR support for scanned documents."""

import os
from typing import Any
import pypdf
from pdf2image import convert_from_path
import pytesseract
from src.exceptions.custom_exceptions import OCRError


class PdfFileReader:
    """Concrete implementation for PDF files with OCR support."""
    
    # הגדרת הנתיב המדויק שבו מותקן Tesseract במחשב
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def read_file(self, file_path: str) -> Any:
        """Read text content from PDF, using OCR if the document is scanned/image-based."""
        if not os.path.exists(file_path):
            raise OCRError(f"The specified file was not found: {file_path}")

        try:
            reader = pypdf.PdfReader(file_path)
            text_content = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
            
            if not text_content.strip():
                images = convert_from_path(file_path, poppler_path=r'C:\poppler-26.09.0\Library\bin')
                for image in images:
                    ocr_text = pytesseract.image_to_string(image, lang='heb+eng')
                    text_content += ocr_text + "\n"

            if not text_content.strip():
                raise OCRError(f"The PDF file is empty or OCR failed: {file_path}")

            return text_content
            
        except Exception as e:
            if isinstance(e, OCRError):
                raise e
            raise OCRError(f"An error occurred while reading the file: {e}") from e