"""Parser Factory implementation."""

from domain.models import ReportType
from src.services.parsers.parser_a import ParserA
from src.services.parsers.parser_b import ParserB


class ParserFactory:
    """מפעל ליצירת אובייקטי פרסור בהתאם לסוג הדו"ח."""

    @staticmethod
    def create_parser(report_type: ReportType):
        """מייצר ומחזיר את הפרסר המתאים לסוג הדו"ח."""
        if report_type == ReportType.TYPE_A:
            return ParserA()
        elif report_type == ReportType.TYPE_B:
            return ParserB()
        else:
            raise ValueError(f'סוג דו"ח לא נתמך: {report_type}')