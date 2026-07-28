import pytest

from domain.const import MIN_TRADE_AMOUNT
from domain.models import Stock, Ticker, UserPortfolio
from domain.services import TradeCalculator


@pytest.fixture
def calculator() -> TradeCalculator:
    return TradeCalculator()


@pytest.fixture
def stocks_map(stocks: list[Stock]) -> dict[Ticker, Stock]:
    return {stock.ticker: stock for stock in stocks}


class TestTradeCalculator:
    def test_apportions_by_target_weight(
        self, calculator: TradeCalculator, stocks_map: dict[Ticker, Stock]
    ) -> None:
        portfolio = UserPortfolio(user_id=1, target_portfolio={"A": 40, "B": 60})

        orders = calculator.calculate(portfolio=portfolio, stocks=stocks_map, amount=10000)

        assert [order.model_dump() for order in orders] == [
            {"symbol": "A", "amount": 4000, "quantity": 4.0},
            {"symbol": "B", "amount": 6000, "quantity": 38.709},
        ]

    def test_excludes_untradable_symbol(
        self, calculator: TradeCalculator, stocks_map: dict[Ticker, Stock]
    ) -> None:
        portfolio = UserPortfolio(user_id=2, target_portfolio={"E": 100})

        orders = calculator.calculate(portfolio=portfolio, stocks=stocks_map, amount=10000)

        assert orders == []

    def test_reapportions_after_excluding_untradable_symbol(
        self, calculator: TradeCalculator, stocks_map: dict[Ticker, Stock]
    ) -> None:
        portfolio = UserPortfolio(user_id=3, target_portfolio={"A": 31, "B": 40, "E": 29})

        orders = calculator.calculate(portfolio=portfolio, stocks=stocks_map, amount=10000)

        assert [order.model_dump() for order in orders] == [
            {"symbol": "A", "amount": 4366, "quantity": 4.366},
            {"symbol": "B", "amount": 5633, "quantity": 36.341},
        ]

    def test_excludes_below_minimum_order_amount_and_reapportions(
        self, calculator: TradeCalculator, stocks_map: dict[Ticker, Stock]
    ) -> None:
        portfolio = UserPortfolio(user_id=4, target_portfolio={"B": 50, "C": 49, "D": 1})

        orders = calculator.calculate(portfolio=portfolio, stocks=stocks_map, amount=1000)

        assert [order.model_dump() for order in orders] == [
            {"symbol": "B", "amount": 505, "quantity": 3.258},
            {"symbol": "C", "amount": 494, "quantity": 0.222},
        ]

    def test_excludes_order_that_floors_to_zero_quantity(
        self, calculator: TradeCalculator, stocks_map: dict[Ticker, Stock]
    ) -> None:
        portfolio = UserPortfolio(user_id=5, target_portfolio={"A": 98, "X": 2})

        orders = calculator.calculate(portfolio=portfolio, stocks=stocks_map, amount=10000)

        assert [order.model_dump() for order in orders] == [
            {"symbol": "A", "amount": 9800, "quantity": 9.8},
        ]

    def test_raises_for_amount_below_minimum_trade_amount(
        self, calculator: TradeCalculator, stocks_map: dict[Ticker, Stock]
    ) -> None:
        portfolio = UserPortfolio(user_id=1, target_portfolio={"A": 100})

        with pytest.raises(ValueError, match=str(MIN_TRADE_AMOUNT)):
            calculator.calculate(
                portfolio=portfolio,
                stocks=stocks_map,
                amount=MIN_TRADE_AMOUNT - 1,
            )
