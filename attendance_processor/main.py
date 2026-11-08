"""Main entry point for the Attendance Data Processing System."""

import argparse
import sys
from pathlib import Path

from src.services.file_readers.pdf_file_reader import PdfFileReader
from src.services.classifiers.file_classifier import FileClassifier
from src.services.factories.parser_factory import ParserFactory
from src.services.transformers.data_transformer import DataTransformer
from src.services.exporters.pdf_renderer import PdfRenderer


def process_attendance_file(file_path: str, output_path: str) -> None:
    """מעביר קובץ בודד דרך כל 5 התחנות של הצינור ברצף:
    1. OCR / קריאת קובץ
    2. זיהוי סוג דו"ח (A או B)
    3. פרסור לאובייקט AttendanceReport אחיד
    4. טרנספורמציה (יצירת דו"ח חדש ומעודכן מבלי לגעת במקור)
    5. גנרוט (הפקת קובץ פלט מעוצב השומר על מבנה המקור)
    """
    print(f"--- Processing file: {file_path} ---")

    # שלב 1: קריאת קובץ / OCR
    reader = PdfFileReader()
    raw_text = reader.read_file(file_path)
    print("Stage 1 (OCR / Reading) completed successfully.")

    # שלב 2: זיהוי סוג הדו"ח
    report_type = FileClassifier.classify(raw_text)
    print(f"Stage 2 (Classification) completed. Report type: {report_type.value}")

    # שלב 3: פרסור מאובייקט טקסט ל-AttendanceReport
    parser = ParserFactory.create_parser(report_type)
    report = parser.parse(raw_text)
    print("Stage 3 (Parsing) completed. AttendanceReport object created.")

    # שלב 4: טרנספורמציה (יצירת דו"ח חדש ומעודכן דטרמיניסטית)
    transformer = DataTransformer()
    transformed_report = transformer.transform(report)
    print("Stage 4 (Transformation) completed. New isolated report created.")

    # שלב 5: גנרוט (כתיבת קובץ פלט חדש)
    renderer = PdfRenderer()
    renderer.render(transformed_report, output_path)
    print(f"Stage 5 (Generation) completed. File saved to: {output_path}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Attendance Data Processing System - End-to-End Pipeline")
    parser.add_argument("--inputs", nargs="+", default=["attendance1.pdf"], help="Paths to input PDF files")
    parser.add_argument("--output-dir", default="output", help="Output directory for processed reports")

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    for file_path in args.inputs:
        if not Path(file_path).exists():
            print(f"Error: File {file_path} not found.", file=sys.stderr)
            continue

        file_name = Path(file_path).stem
        output_path = output_dir / f"{file_name}_processed.html"

        try:
            process_attendance_file(file_path, str(output_path))
            success_count += 1
        except Exception as e:
            print(f"Error processing file {file_path}: {e}", file=sys.stderr)

    print(f"Process finished. Successfully processed {success_count} out of {len(args.inputs)} files.")


if __name__ == "__main__":
    main()