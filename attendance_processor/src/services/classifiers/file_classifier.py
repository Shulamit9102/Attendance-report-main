"""File Classifier implementation."""

from domain.models import ReportType


class FileClassifier:
    """מזהה את סוג הדו"ח מתוך טקסט ה-OCR הגולמי."""

    @staticmethod
    def classify(raw_text: str) -> ReportType:
        """מזהה האם הדו"ח הוא מסוג A או מסוג B על סמך מילות מפתח ייחודיות."""
        if not raw_text:
            raise ValueError("הטקסט שהתקבל ריק ולא ניתן לסווג אותו.")

        text_lower = raw_text.lower()

        # מילות מפתח שקיימות אך ורק בדו"חות מסוג A
        type_a_indicators = ["מקום.ע", "125%", "150%", "הפסקה"]
        
        # בדיקה האם לפחות אחת ממילות המפתח המובהקות של סוג A קיימת בטקסט
        found_a_indicator = any(indicator in text_lower for indicator in type_a_indicators)

        if found_a_indicator:
            return ReportType.TYPE_A
        
        # אם לא נמצאו סממנים מובהקים של סוג A, זהו קובץ מסוג B
        return ReportType.TYPE_B