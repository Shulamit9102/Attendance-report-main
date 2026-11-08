# scripts/run_stage_1.py
import os
import sys

# הוספת נתיב הפרויקט כדי שנוכל לייבא מתוך src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.file_readers.pdf_file_reader import PdfFileReader

def main():
    # הגדרת נתיב לקובץ PDF לדוגמה בתיקיית הקלט
    input_pdf_path = "attendance1.pdf"  # או הנתיב שבו נמצא קובץ ה-PDF שלך    
    if not os.path.exists(input_pdf_path):
        print(f"שגיאה: קובץ ה-PDF לא נמצא בנתיב: {input_pdf_path}")
        print("אנא ודאי שקיים קובץ PDF לבדיקה בתיקיית input_pdfs.")
        return

    print(f"==> מתחיל עיבוד OCR לקובץ: {input_pdf_path}")

    try:
        # הפעלת קורא ה-PDF שמבצע את ה-OCR (תחנה 1)
        reader = PdfFileReader()
        raw_text = reader.read_file(input_pdf_path)

        print("\n--- תוצאת טקסט גולמי (OCR) ---")
        # הדפסת תחילת הטקסט להתרשמות ראשונית
        print(raw_text[:1000] if len(raw_text) > 1000 else raw_text)
        print("--------------------------------")
        
        print(f"\nסך הכל חולצו {len(raw_text)} תווים בהצלחה.")
        print("✓ תחנה 1 הושלמה בהצלחה.")

    except Exception as e:
        print(f"✗ שגיאה בתחנת ה-OCR: {e}")

if __name__ == "__main__":
    main()