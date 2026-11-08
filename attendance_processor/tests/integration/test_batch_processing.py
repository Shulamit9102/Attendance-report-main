"""Integration test for batch processing."""

from src.pipeline.batch_processor import BatchProcessor

def mock_process(file_path: str) -> dict:
    return {"path": file_path, "processed": True}

def test_batch_processor_integration() -> None:
    processor = BatchProcessor(max_workers=2)
    files = ["report_a.pdf", "report_b.csv"]
    results = processor.process_batch(files, mock_process)
    assert len(results) == 2
    for res in results:
        assert res["status"] == "success"