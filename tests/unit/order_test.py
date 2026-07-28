import pytest
from pydantic import ValidationError

from domain.models import Order


class TestOrder:
    def test_creates_valid_order(self) -> None:
        order = Order(symbol="A", amount=4000, quantity=4.0)

        assert order.symbol == "A"
        assert order.amount == 4000
        assert order.quantity == 4.0

    def test_rejects_extra_fields(self) -> None:
        with pytest.raises(ValidationError):
            Order(symbol="A", amount=4000, quantity=4.0, extra="nope")

    def test_rejects_non_positive_amount(self) -> None:
        with pytest.raises(ValidationError):
            Order(symbol="A", amount=0, quantity=4.0)

    def test_rejects_non_positive_quantity(self) -> None:
        with pytest.raises(ValidationError):
            Order(symbol="A", amount=4000, quantity=0)
