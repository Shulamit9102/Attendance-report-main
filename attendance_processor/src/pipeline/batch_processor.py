"""Concurrent batch processor for handling multiple attendance files."""

import concurrent.futures
import logging
from typing import List, Dict, Any, Callable
from src.constants.app_constants import MAX_WORKERS
from src.utils.performance import PerformanceTimer

logger = logging.getLogger(__name__)

class BatchProcessor:
    """Processes multiple attendance files concurrently using thread pools."""

    def __init__(self, max_workers: int = MAX_WORKERS) -> None:
        self.max_workers = max_workers

    def process_batch(self, file_paths: List[str], process_func: Callable[[str], Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a list of file paths concurrently and return results."""
        results: List[Dict[str, Any]] = []
        logger.info(f"Starting batch processing of {len(file_paths)} files with max_workers={self.max_workers}.")
        
        with PerformanceTimer("Batch Processing Execution"):
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_file = {executor.submit(process_func, path): path for path in file_paths}
                for future in concurrent.futures.as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        result = future.result()
                        results.append({"file": file_path, "status": "success", "data": result})
                        logger.info(f"Successfully processed file: {file_path}")
                    except Exception as e:
                        logger.error(f"Error processing file {file_path}: {e}")
                        results.append({"file": file_path, "status": "error", "error": str(e)})
        
        return results