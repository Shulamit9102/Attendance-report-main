# scripts/run_stage_3.py
import sys
import os

# הוספת תיקיית השורש לנתיב כדי לאפשר ייבוא תקין
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.file_readers.pdf_file_reader import PdfFileReader
from src.services.classifiers.file_classifier import FileClassifier
from src.services.factories.parser_factory import ParserFactory

def main():
    pdf_path = "attendance2.pdf"  # ניתן להחליף גם ל- attendance2.pdf
    if not os.path.exists(pdf_path):
        print(f"הקובץ {pdf_path} אינו נמצא בתיקיית השורש.")
        return

    print(f"--- שלב 1: קריאת OCR לקובץ {pdf_path} ---")
    reader = PdfFileReader()
    raw_text = reader.read_file(pdf_path)
    print(f"אורך הטקסט הגולמי: {len(raw_text)} תווים.")

    print("\n--- שלב 2: זיהוי סוג הדו\"ח (Classifier) ---")
    report_type = FileClassifier.classify(raw_text)
    print(f"סוג הדו\"ח שזוהה: {report_type.value}")

    print("\n--- שלב 3: פרסור הדו\"ח לאובייקטים (Parser & Factory) ---")
    parser = ParserFactory.create_parser(report_type)
    report = parser.parse(raw_text)
    
    print(f"הדו\"ח פוענח בהצלחה!")
    print(f"סוג הדו\"ח במודל: {report.report_type.value}")
    print(הכמות_שורות := f"מספר שורות הנוכחות שזוהו: {len(report.rows)}")
    
    # הצגת 3 שורות ראשונות לדוגמה מתוך הדו"ח
    print("\nדוגמה לשורות שנוצרו:")
    for i, row in enumerate(report.rows[:3], 1):
        print(f"שורה {i}: {row}")

if __name__ == "__main__":
    main()