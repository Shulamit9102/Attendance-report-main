# Attendance Data Processing System

מערכת מודולרית ואוטומטית לעיבוד, ניתוח, שינוי והפקת דוחות נוכחות מתוך קבצי PDF (כולל מסמכים סרוקים באמצעות OCR), תוך שמירה על מבנה נתונים דטרמיניסטי ופריסת ארכיטקטורה נקייה לפי 5 תחנות עבודה.

---

## 🚀 מבנה הצינור (Pipeline Stages)
1. **OCR / קריאת קובץ**: המרת PDF סרוק לטקסט גולמי.
2. **זיהוי סוג דו"ח**: סיווג אוטומטי ל-`TYPE_A` או `TYPE_B`.
3. **פרסור**: המרת הטקסט לאובייקט מובנה אחיד (`AttendanceReport`).
4. **טרנספורמציה**: עדכון שעות דטרמיניסטי ויצירת אובייקט דו"ח חדש.
5. **גנרוט**: הפקת קובץ פלט מעוצב (`RTL`) ששומר על מבנה המקור.

---

## 📂 מבנה הפרויקט
```text
attendance_processor/
├── main.py
├── README.md
├── requirements.txt
├── attendance1.pdf
├── attendance2.pdf
├── config/
│   └── laws.py
├── docs/
│   └── architecture.md
├── domain/
│   ├── models.py
│   └── time_math.py
├── scripts/
│   ├── run_stage_1.py
│   ├── run_stage_2.py
│   ├── run_stage_3.py
│   ├── run_stage_4.py
│   └── run_stage_5.py
├── src/
│   ├── cli/
│   ├── exceptions/
│   ├── interfaces/
│   ├── pipeline/
│   └── services/
└── tests/
    ├── integration/
    └── unit/