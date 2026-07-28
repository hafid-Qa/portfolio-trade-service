from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from api.deps import get_portfolio_repo, get_stock_repo
from domain.models import Stock, UserPortfolio
from domain.repositories import StockRepository, UserPortfolioRepository
from main import create_app
from repositories import InMemoryStockRepository, InMemoryUserPortfolioRepository
from settings import get_settings


@pytest.fixture
def stocks() -> list[Stock]:
    return [
        Stock(ticker="A", price=1000, tradable=True),
        Stock(ticker="B", price=155, tradable=True),
        Stock(ticker="C", price=2222, tradable=True),
        Stock(ticker="D", price=467, tradable=True),
        Stock(ticker="E", price=888, tradable=False),
        Stock(ticker="X", price=250_000, tradable=True),
    ]


@pytest.fixture
def portfolios() -> list[UserPortfolio]:
    return [
        UserPortfolio(user_id=1, target_portfolio={"A": 40, "B": 60}),
        UserPortfolio(user_id=2, target_portfolio={"E": 100}),
        UserPortfolio(user_id=3, target_portfolio={"A": 31, "B": 40, "E": 29}),
        UserPortfolio(user_id=4, target_portfolio={"B": 50, "C": 49, "D": 1}),
        # Zero quantity skip
        UserPortfolio(user_id=5, target_portfolio={"A": 98, "X": 2}),
        # Unknown Stock
        UserPortfolio(user_id=6, target_portfolio={"A": 50, "ZZZ": 50}),
    ]


@pytest.fixture
def portfolio_repo(portfolios: list[UserPortfolio]) -> InMemoryUserPortfolioRepository:
    return InMemoryUserPortfolioRepository(portfolios)


@pytest.fixture
def stock_repo(stocks: list[Stock]) -> InMemoryStockRepository:
    return InMemoryStockRepository(stocks)


@pytest.fixture
def client() -> Iterator[TestClient]:
    app = create_app(get_settings())
    with TestClient(app) as c:
        yield c


@pytest.fixture
def client_with(
    stock_repo: StockRepository, portfolio_repo: UserPortfolioRepository
) -> Iterator[TestClient]:
    app = create_app(get_settings())
    app.dependency_overrides[get_stock_repo] = lambda: stock_repo
    app.dependency_overrides[get_portfolio_repo] = lambda: portfolio_repo
    with TestClient(app) as c:
        yield c
