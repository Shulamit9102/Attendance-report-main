"""Custom exceptions for the attendance processing system."""


class AttendanceSystemError(Exception):
    """Base exception for all attendance system errors."""
    pass


class OCRError(AttendanceSystemError):
    """Raised when OCR processing fails (Station 1)."""
    pass


class FileClassificationError(AttendanceSystemError):
    """Raised when file classification fails (Station 2)."""
    pass


class ParsingError(AttendanceSystemError):
    """Raised when parsing raw data fails (Station 3)."""
    pass


class TransformationError(AttendanceSystemError):
    """Raised when transforming data fails (Station 4)."""
    pass


class GenerationError(AttendanceSystemError):
    """Raised when rendering/generating the output file fails (Station 5)."""
    pass
class ExportError(Exception):
    """שגיאה המתרחשת בעת כישלון בייצוא או הפקת קבצים."""
    pass