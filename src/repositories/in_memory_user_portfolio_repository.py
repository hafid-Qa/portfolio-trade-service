from pathlib import Path
from typing import Any

from domain.models import UserPortfolio
from domain.repositories import UserPortfolioRepository
from yaml_io import read_yaml


class InMemoryUserPortfolioRepository(UserPortfolioRepository):
    def __init__(self, portfolios: list[UserPortfolio]) -> None:
        self._portfolios: dict[int, UserPortfolio] = {
            portfolio.user_id: portfolio for portfolio in portfolios
        }

    @classmethod
    def from_yaml(cls, path: Path) -> "InMemoryUserPortfolioRepository":
        raw: list[dict[str, Any]] = read_yaml(path)
        portfolios: list[UserPortfolio] = [UserPortfolio.model_validate(item) for item in raw]
        return cls(portfolios)

    def get_by_user_id(self, user_id: int) -> UserPortfolio | None:
        return self._portfolios.get(user_id)
