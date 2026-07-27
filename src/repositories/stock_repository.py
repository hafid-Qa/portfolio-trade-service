from collections.abc import Iterable
from typing import Protocol

from domain.models import Stock, Ticker


class StockRepository(Protocol):
    def get_by_ticker(self, ticker: Ticker) -> Stock | None: ...
    def get_by_tickers(self, tickers: Iterable[Ticker]) -> dict[Ticker, Stock]: ...
