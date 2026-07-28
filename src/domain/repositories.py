from abc import ABC, abstractmethod
from collections.abc import Iterable

from domain.models import Stock, Ticker, UserPortfolio


class StockRepository(ABC):
    @abstractmethod
    def get_by_tickers(self, tickers: Iterable[Ticker]) -> dict[Ticker, Stock]: ...


class UserPortfolioRepository(ABC):
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> UserPortfolio | None: ...
