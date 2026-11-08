"""Unit tests for data exporters and exporter factory."""

import pytest
from src.services.factories.exporter_factory import ExporterFactory
from src.exceptions.custom_exceptions import UnsupportedFormatError

def test_exporter_factory_valid() -> None:
    csv_exp = ExporterFactory.create_exporter("csv")
    assert csv_exp is not None

    excel_exp = ExporterFactory.create_exporter("xlsx")
    assert excel_exp is not None

def test_exporter_factory_invalid() -> None:
    with pytest.raises(UnsupportedFormatError):
        ExporterFactory.create_exporter("unsupported_format")