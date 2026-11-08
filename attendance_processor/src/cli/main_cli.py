"""Command Line Interface for the attendance data processing system."""

import argparse
import sys
from src.pipeline.pipeline_manager import PipelineManager
from src.utils.logger import get_logger
from src.exceptions.custom_exceptions import AttendanceSystemError

logger = get_logger("MainCLI")


def main() -> int:
    """Execute the CLI interface."""
    parser = argparse.ArgumentParser(description="Attendance Data Processing System CLI")
    parser.add_argument("file_path", type=str, help="Path to the attendance report file")
    parser.add_argument(
        "--parser",
        type=str,
        default="PARSER_A",
        help="Parser type to use (PARSER_A or PARSER_B)",
    )

    args = parser.parse_args()
    pipeline = PipelineManager()
    if len(args.files) > 1:
        pipeline.run_batch(args.files)
    else:
        pipeline.run_file(args.files[0])
    return 0

    try:
        logger.info(f"Starting processing for file: {args.file_path} using parser: {args.parser}")
        pipeline = PipelineManager()
        result = pipeline.process_file(args.file_path, parser_type=args.parser)
        logger.info("Processing completed successfully.")
        print(result)
        return 0
    except AttendanceSystemError as e:
        logger.error(f"System Error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        print(f"Unexpected Error: {e}", file=sys.stderr)
        return 1
    parser.add_argument("--format", default="csv", help="Export format (csv, xlsx)")
    parser.add_argument("--output", default="output.csv", help="Output file path")

if __name__ == "__main__":
    sys.exit(main())