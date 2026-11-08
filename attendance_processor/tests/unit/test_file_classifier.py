# tests/unit/test_file_classifier.py
import pytest
from src.services.classifiers.file_classifier import FileClassifier
from domain.models import ReportType

def test_classify_type_a():
    """בדיקה שזיהוי טקסט של סוג A מחזיר TYPE_A."""
    sample_text_a = "דוח נוכחות מקום.ע הפסקה 100% 125% 150% שבת"
    result = FileClassifier.classify(sample_text_a)
    assert result == ReportType.TYPE_A

def test_classify_type_b():
    """בדיקה שזיהוי טקסט של סוג B מחזיר TYPE_B."""
    sample_text_b = "דוח נוכחות חודשי הערות כלליות"
    result = FileClassifier.classify(sample_text_b)
    assert result == ReportType.TYPE_B

def test_classify_empty_text_raises_error():
    """בדיקה שטקסט ריק זורק שגיאה מתאימה."""
    with pytest.raises(ValueError):
        FileClassifier.classify("")