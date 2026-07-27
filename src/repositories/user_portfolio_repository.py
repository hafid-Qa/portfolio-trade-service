from typing import Protocol

from domain.models import UserPortfolio


class UserPortfolioRepository(Protocol):
    def get_by_user_id(self, user_id: int) -> UserPortfolio | None: ...
