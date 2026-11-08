# config/rules.py

# סוגי הדו"חות הנתמכים במערכת
REPORT_TYPE_A = "TYPE_A"
REPORT_TYPE_B = "TYPE_B"

# --- חוקים וכללים לטרנספורמציה (תחנה 4) ---
# בהתאם لدרישות האינווריאנטים וחישוב השעות:

# ערך ההזזה עבור שעות הכניסה והיציאה (לדוגמה, הזזה בדקות או בשעות)
TIME_SHIFT_MINUTES = 15 

# ספים לשעות נוספות (רלוונטי במיוחד לסוג B שמחלק ל-100%, 125%, 150%)
STANDARD_WORK_DAY_HOURS = 8.0
OVERTIME_THRESHOLD_125 = 8.5
OVERTIME_THRESHOLD_150 = 10.0

# הפסקה סטנדרטית (בדקות) במידת הצורך
DEFAULT_BREAK_MINUTES = 30