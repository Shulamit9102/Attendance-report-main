# scripts/run_stage_2.py
import sys
import os

# הוספת תיקיית השורש לנתיב כדי לאפשר ייבוא תקין
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.file_readers.pdf_file_reader import PdfFileReader
from src.services.classifiers.file_classifier import FileClassifier

def main():
    pdf_path = "attendance1.pdf"  # או קובץ לבחירתך
    if not os.path.exists(pdf_path):
        print(f"הקובץ {pdf_path} אינו נמצא בתיקיית השורש.")
        return

    print(f"--- מריץ שלב 1 (OCR) על הקובץ: {pdf_path} ---")
    # שלב 1: יצירת מופע של הקורא והמרת ה-PDF לטקסט גולמי באמצעות read_file
    reader = PdfFileReader()
    raw_text = reader.read_file(pdf_path)
    print(f"אורך הטקסט הגולמי שהתקבל: {len(raw_text)} תווים.")

    print("\n--- מריץ שלב 2 (Classifier) ---")
    # שלב 2: סיווג הדו"ח מתוך הטקסט הגולמי
    report_type = FileClassifier.classify(raw_text)
    print(f"תוצאת הסיווג בהצלחה: סוג הדו\"ח הוא -> {report_type.value}")

if __name__ == "__main__":
    main()