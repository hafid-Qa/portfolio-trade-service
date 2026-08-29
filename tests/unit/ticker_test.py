import pytest
from pydantic import TypeAdapter, ValidationError

from domain.models import Ticker


ticker_adapter = TypeAdapter(Ticker)


class TestTicker:
    def test_strips_surrounding_whitespace(self) -> None:
        assert ticker_adapter.validate_python("  A  ") == "A"

    def test_rejects_empty_string(self) -> None:
        with pytest.raises(ValidationError):
            ticker_adapter.validate_python("")

    def test_rejects_whitespace_only_string(self) -> None:
        with pytest.raises(ValidationError):
            ticker_adapter.validate_python("   ")
