"""Integration tests for system resilience and final stabilization."""

from src.pipeline.pipeline_manager import PipelineManager

def test_pipeline_resilience_with_malformed_input() -> None:
    pipeline = PipelineManager()
    # Simulating processing of a non-existent or malformed file path
    result = pipeline.run_file("non_existent_malformed_file.xyz")
    
    # System should handle gracefully and return an error status instead of crashing
    assert isinstance(result, dict)
    assert result.get("status") == "error" or "error" in result