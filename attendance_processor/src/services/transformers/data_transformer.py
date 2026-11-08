from domain.models import AttendanceReport, ReportType
from src.interfaces.transformer_interface import ITransformer
from src.services.transformers.type_a_strategy import TypeATransformationStrategy
from src.services.transformers.type_b_strategy import TypeBTransformationStrategy

class DataTransformer(ITransformer):
    """שירות המרכז את בחירת האסטרטגיה והפעלתה ללא שימוש בתנאי if כפולים בלוגיקה."""

    def __init__(self):
        self._strategies = {
            ReportType.TYPE_A: TypeATransformationStrategy(),
            ReportType.TYPE_B: TypeBTransformationStrategy(),
        }

    def transform(self, report: AttendanceReport) -> AttendanceReport:
        """בוחר את האסטרטגיה המתאימה לפי סוג הדו"ח ומריץ אותה."""
        strategy = self._strategies.get(report.report_type)
        if not strategy:
            raise ValueError(f"Unsupported report type for transformation: {report.report_type}")
        
        return strategy.transform_report(report)