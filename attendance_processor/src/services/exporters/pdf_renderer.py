"""PDF Renderer implementation for attendance reports using layouts and HTML templates."""

import logging
from pathlib import Path
from typing import List, Dict, Any
from domain.models import AttendanceReport
from .layouts import get_layout_for_report_type
from src.exceptions.custom_exceptions import ExportError

logger = logging.getLogger(__name__)

class PdfRenderer:
    """מרנדר אובייקט AttendanceReport לקובץ PDF מעוצב תוך שמירה על מבנה העמודות המקורי וכיווניות RTL."""

    def render(self, report: AttendanceReport, output_path: str) -> None:
        """מפיק קובץ PDF מתוך נתוני הדו"ח."""
        if not report or not report.rows:
            logger.warning("אין נתונים להפקת PDF.")
            return

        try:
            # שליפת מבנה העמודות בהתאם לסוג הדו"ח (A או B)
            columns = get_layout_for_report_type(report.report_type)
            
            # יצירת מבנה ה-HTML המעוצב לדו"ח
            html_content = self._generate_html(report, columns)
            
            # המרה ל-PDF באמצעות WeasyPrint (או שמירה כ-HTML כגיבוי אם הספרייה אינה מותקנת או חסרות ספריות מערכת)
            try:
                from weasyprint import HTML
                HTML(string=html_content).write_pdf(output_path)
                logger.info(f"קובץ ה-PDF נוצר בהצלחה בנתיב: {output_path}")
            except (ImportError, OSError):
                html_path = str(Path(output_path).with_suffix('.html'))
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"הודעה: ספריות המערכת של WeasyPrint אינן זמינות. הדו\"ח נשמר בהצלחה כקובץ HTML בנתיב: {html_path}")
                logger.warning(f"ספריות המערכת של WeasyPrint אינן זמינות. הדו\"ח נשמר כקובץ HTML בנתיב: {html_path}")
                return

        except Exception as e:
            logger.error(f"שגיאה בהפקת ה-PDF: {e}")
            raise ExportError(f"כשל בהפקת PDF: {e}")

    def _generate_html(self, report: AttendanceReport, columns: List[Dict[str, str]]) -> str:
        """מייצר מחרוזת HTML מעוצבת התומכת בעברית ובכיווניות RTL."""
        headers_html = "".join([f"<th>{col['label']}</th>" for col in columns])
        
        rows_html = ""
        for row in report.rows:
            row_cells = []
            for col in columns:
                key = col["key"]
                val = getattr(row, key, "") or ""
                row_cells.append(f"<td>{val}</td>")
            rows_html += f"<tr>{''.join(row_cells)}</tr>\n"

        summary_text = f"סיכום שעות כולל: {report.summary.total_hours_sum}" if report.summary and report.summary.total_hours_sum else ""

        html_template = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>דו"ח נוכחות - סוג {report.report_type.value}</title>
    <style>
        body {{
            font-family: 'David', 'Arial', sans-serif;
            direction: rtl;
            text-align: right;
            margin: 30px;
            color: #2c3e50;
        }}
        h2 {{
            text-align: center;
            margin-bottom: 5px;
        }}
        .report-info {{
            text-align: center;
            font-size: 0.9em;
            color: #7f8c8d;
            margin-bottom: 20px;
        }}
        .summary {{
            margin-bottom: 15px;
            font-weight: bold;
            font-size: 1.1em;
            background-color: #ecf0f1;
            padding: 8px 12px;
            border-radius: 4px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        th, td {{
            border: 1px solid #bdc3c7;
            padding: 8px 12px;
            text-align: center;
            font-size: 0.95em;
        }}
        th {{
            background-color: #34495e;
            color: #ffffff;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
    </style>
</head>
<body>
    <h2>דו"ח נוכחות מרוכז</h2>
    <div class="report-info">סוג דו"ח: {report.report_type.value}</div>
    <div class="summary">{summary_text}</div>
    <table>
        <thead>
            <tr>{headers_html}</tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
</body>
</html>"""
        return html_template