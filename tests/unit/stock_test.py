import pytest
from pydantic import ValidationError

from domain.models import Stock


class TestStock:
    def test_creates_valid_stock(self) -> None:
        stock = Stock(ticker="A", price=1000, tradable=True)

        assert stock.ticker == "A"
        assert stock.price == 1000
        assert stock.tradable is True

    def test_rejects_extra_fields(self) -> None:
        with pytest.raises(ValidationError):
            Stock(ticker="A", price=1000, tradable=True, extra="nope")

    def test_rejects_non_positive_price(self) -> None:
        with pytest.raises(ValidationError):
            Stock(ticker="A", price=0, tradable=True)
