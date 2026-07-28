import pytest
from pydantic import ValidationError

from domain.models import Order, TradeResult


class TestTradeResult:
    def test_creates_valid_trade_result(self) -> None:
        result = TradeResult(
            amount=10000,
            target_portfolio={"A": 40, "B": 60},
            orders=[Order(symbol="A", amount=4000, quantity=4.0)],
        )

        assert result.amount == 10000
        assert result.target_portfolio == {"A": 40, "B": 60}
        assert result.orders == [Order(symbol="A", amount=4000, quantity=4.0)]

    def test_is_frozen(self) -> None:
        result = TradeResult(amount=10000, target_portfolio={"A": 100}, orders=[])

        with pytest.raises(ValidationError):
            result.amount = 5000
