from collections.abc import Iterable
from typing import Protocol

from domain.models import Stock, Ticker, UserPortfolio


class StockRepository(Protocol):
    def get_by_ticker(self, ticker: Ticker) -> Stock | None: ...
    def get_by_tickers(self, tickers: Iterable[Ticker]) -> dict[Ticker, Stock]: ...


class UserPortfolioRepository(Protocol):
    def get_by_user_id(self, user_id: int) -> UserPortfolio | None: ...
