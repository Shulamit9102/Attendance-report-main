# Architecture Documentation - Attendance Data Processing System

## 1. System Pipeline & Stages
הפרויקט בנוי כצינור עיבוד (Pipeline) מודולרי המורכב מחמש תחנות עוקבות, כאשר כל תחנה מקבלת נתון מוגדר ומחזירה תוצאה ברורה ללא תלות חיצונית:

1. **OCR / קריאת קובץ (`src/services/file_readers/`)**: 
   - המרת עמודי PDF סרוקים לתמונות וזיהוי טקסט באמצעות `Tesseract OCR` (עברית ואנגלית).
   - פלט: מחרוזת טקסט גולמית (`str`).

2. **זיהוי סוג דו"ח (`src/services/classifiers/`)**:
   - ניתוח הטקסט הגולמי וזיהוי מבנה הדו"ח (`TYPE_A` או `TYPE_B`) על בסיס מילות מפתח מובהקות.
   - פלט: טיפוס מסוג `ReportType`.

3. **פרסור (`src/services/parsers/`, `src/services/factories/`)**:
   - בחירת הפרסר באמצעות `ParserFactory` והפעלת תבנית **Template Method** במחלקת הבסיס `BaseParser`.
   - **החוזה המרכזי**: מעבר לנקודה זו, המערכת עובדת אך ורק עם אובייקט נתונים אחיד.
   - פלט: אובייקט `AttendanceReport`.

4. **טרנספורמציה (`src/services/transformers/`, `domain/`)**:
   - שימוש בתבנית **Strategy** לביצוע שינויים דטרמיניסטיים בשעות וחישוב מחדש של נתוני השעות.
   - שמירה על שלמות המקור באמצעות אובייקטים קפואים (`frozen=True`) ויצירת דו"ח חדש.
   - פלט: אובייקט `AttendanceReport` חדש ומעודכן.

5. **גנרוט פלט (`src/services/exporters/`)**:
   - הפקת קובץ פלט ויזואלי חדש (HTML/PDF) מימין לשמאל (`RTL`) השומר בקפידה על מבנה העמודות והעיצוב של קובץ המקור מבלי לשנות את המקור.

---

## 2. Design Decisions & SOLID Principles
- **Single Responsibility Principle (SRP)**: לכל תחנה ולכל מחלקה יש אחריות בלעדית וממוקדת.
- **Open/Closed Principle (OCP)**: קל להוסיף סוגי דוחות נוספים בעתיד על ידי הוספת מחלקת פרסר ואסטרטגיה ייעודית מבלי לפגוע בקוד הקיים.
- **Immutability & Determinism**: הבטחה שכל הרצה על אותו קובץ תייצר תוצאה מדויקת וזהה לחלוטין.