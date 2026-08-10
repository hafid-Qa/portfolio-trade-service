import pytest

from domain.exceptions import PortfolioNotFound, UnknownStocksInPortfolio
from domain.models import TradeResult
from domain.repositories import StockRepository, UserPortfolioRepository
from domain.services import TradeCalculator, TradeService


@pytest.fixture
def calculator() -> TradeCalculator:
    return TradeCalculator()


@pytest.fixture
def service(
    stock_repo: StockRepository,
    portfolio_repo: UserPortfolioRepository,
    calculator: TradeCalculator,
) -> TradeService:
    return TradeService(stock_repo, portfolio_repo, calculator)


class TestTradeService:
    def test_apportions_by_target_weight(
        self,
        stock_repo: StockRepository,
        portfolio_repo: UserPortfolioRepository,
        service: TradeService,
    ) -> None:
        result = service.create_trade(user_id=1, amount=10000)
        assert isinstance(result, TradeResult)

        assert result.amount == 10000
        assert result.target_portfolio == {"A": 40, "B": 60}
        assert [order.model_dump() for order in result.orders] == [
            {"symbol": "A", "amount": 4000, "quantity_units": 4000},
            {"symbol": "B", "amount": 6000, "quantity_units": 38709},
        ]

    def test_reapportions_after_excluding_below_minimum_order_amount(
        self, service: TradeService
    ) -> None:
        result = service.create_trade(user_id=4, amount=1000)

        assert result.target_portfolio == {"B": 50, "C": 49, "D": 1}
        assert [order.model_dump() for order in result.orders] == [
            {"symbol": "B", "amount": 505, "quantity_units": 3258},
            {"symbol": "C", "amount": 494, "quantity_units": 222},
        ]

    def test_raises_for_unknown_user(self, service: TradeService) -> None:
        with pytest.raises(PortfolioNotFound):
            service.create_trade(user_id=999, amount=10000)

    def test_raises_when_portfolio_references_unknown_stock(self, service: TradeService) -> None:
        with pytest.raises(UnknownStocksInPortfolio):
            service.create_trade(user_id=6, amount=10000)
