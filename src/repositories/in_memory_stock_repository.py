from collections.abc import Iterable
from pathlib import Path
from typing import Any

from domain.models import Stock, Ticker
from yaml_io import read_yaml


class InMemoryStockRepository:
    def __init__(self, stocks: list[Stock]) -> None:
        self._stocks: dict[Ticker, Stock] = {stock.ticker: stock for stock in stocks}

    @classmethod
    def from_yaml(cls, path: Path) -> "InMemoryStockRepository":
        raw: list[dict[str, Any]] = read_yaml(path)
        stocks: list[Stock] = [Stock.model_validate(item) for item in raw]
        return cls(stocks)

    def get_by_ticker(self, ticker: Ticker) -> Stock | None:
        return self._stocks.get(ticker)

    def get_by_tickers(self, tickers: Iterable[Ticker]) -> dict[Ticker, Stock]:
        return {t: self._stocks[t] for t in tickers if t in self._stocks}
