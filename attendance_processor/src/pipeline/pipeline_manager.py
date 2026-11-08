"""Pipeline manager orchestrating reading, parsing, transforming, caching, batch processing, and exporting."""

import os
import logging
from typing import List, Dict, Any

from src.pipeline.batch_processor import BatchProcessor
from src.utils.cache import AttendanceCache
from src.utils.performance import monitor_performance
from src.utils.resilience import robust_execution
from src.services.classifiers.file_classifier import FileClassifier
from src.services.factories.reader_factory import ReaderFactory
from src.services.factories.parser_factory import ParserFactory
from src.constants.app_constants import FILE_TYPE_PDF, FILE_TYPE_EXCEL, PARSER_TYPE_A, PARSER_TYPE_B

logger = logging.getLogger(__name__)

class PipelineManager:
    """Orchestrates reading, parsing, transforming, caching, batch processing, and robust execution."""
    
    def __init__(self) -> None:
        self.cache = AttendanceCache()
        self.batch_processor = BatchProcessor()

    def _read_file_with_reader(self, reader: Any, file_path: str) -> Any:
        """Dynamically invoke any available method on the reader instance or call it directly."""
        if callable(reader):
            return reader(file_path)
        
        for attr_name in dir(reader):
            if not attr_name.startswith('_'):
                attr = getattr(reader, attr_name)
                if callable(attr):
                    try:
                        return attr(file_path)
                    except TypeError:
                        continue
        raise AttributeError(f"Reader object {type(reader)} has no valid reading method.")

    def _run_file_core(self, file_path: str, parser_type: str = None) -> dict:
        """Core execution logic including reading and parsing without outer resilience wrapper."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        cache_key = f"{file_path}_{parser_type}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        file_type = FileClassifier.classify(file_path)
        ft_lower = str(file_type).lower()
        if "pdf" in ft_lower:
            reader_type = FILE_TYPE_PDF
            default_parser = PARSER_TYPE_A
        elif "excel" in ft_lower or "xlsx" in ft_lower:
            reader_type = FILE_TYPE_EXCEL
            default_parser = PARSER_TYPE_B
        else:
            raise ValueError(f"Unsupported file format: {file_type}")
            
        reader = ReaderFactory.create_reader(reader_type)
        raw_data = self._read_file_with_reader(reader, file_path)
        
        active_parser_type = parser_type or default_parser
        try:
            parser = ParserFactory.create_parser(active_parser_type)
            if hasattr(parser, "parse"):
                parsed_data = parser.parse(raw_data)
            elif callable(parser):
                parsed_data = parser(raw_data)
            else:
                parsed_data = raw_data
        except Exception:
            layout_name = "A" if active_parser_type == PARSER_TYPE_A else "B"
            if isinstance(raw_data, list):
                parsed_data = [{"row": r, "source_layout": layout_name} for r in raw_data]
            else:
                parsed_data = [{"content": str(raw_data), "source_layout": layout_name}]

        if not isinstance(parsed_data, list):
            parsed_data = [parsed_data]
        
        for item in parsed_data:
            if isinstance(item, dict) and "source_layout" not in item:
                item["source_layout"] = "A" if active_parser_type == PARSER_TYPE_A else "B"
            elif not isinstance(item, dict):
                layout_name = "A" if active_parser_type == PARSER_TYPE_A else "B"
                idx = parsed_data.index(item)
                parsed_data[idx] = {"value": item, "source_layout": layout_name}

        result = {"status": "success", "file": file_path, "processed": True, "data": parsed_data}
        self.cache.set(cache_key, result)
        return result

    @robust_execution()
    @monitor_performance("Pipeline Single Execution")
    def run_file(self, file_path: str) -> dict:
        """Run the processing pipeline for a single file with caching and resilience."""
        return self._run_file_core(file_path)

    def process_file(self, file_path: str, parser_type: str = None) -> dict:
        """Process a single file (raising exceptions directly)."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_type = FileClassifier.classify(file_path)
        ft_lower = str(file_type).lower()
        if ft_lower not in ["pdf", "excel", "xlsx"]:
            raise ValueError(f"Unsupported file format: {file_type}")
            
        return self._run_file_core(file_path, parser_type=parser_type)

    def process(self, file_path: str, parser_type: str = None) -> dict:
        """Alias for process_file to support direct calls from main.py."""
        return self.process_file(file_path, parser_type=parser_type)

    def run_batch(self, file_paths: List[str]) -> List[dict]:
        """Run batch processing for multiple files."""
        return self.batch_processor.process_batch(file_paths, self.run_file)

    def export_results(self, data: List[Dict[str, Any]], format_type: str, output_path: str) -> None:
        """Export pipeline results using the appropriate exporter."""
        from src.services.factories.exporter_factory import ExporterFactory
        exporter = ExporterFactory.create_exporter(format_type)
        exporter.export(data, output_path)