import pytest
from pydantic import ValidationError

from domain.models import UserPortfolio


class TestUserPortfolio:
    def test_creates_valid_user_portfolio(self) -> None:
        portfolio = UserPortfolio(user_id=1, target_portfolio={"A": 40, "B": 60})

        assert portfolio.user_id == 1
        assert portfolio.target_portfolio == {"A": 40, "B": 60}

    def test_tickers_returns_target_portfolio_keys(self) -> None:
        portfolio = UserPortfolio(user_id=1, target_portfolio={"A": 40, "B": 60})

        assert portfolio.tickers == ["A", "B"]

    def test_rejects_allocations_not_summing_to_100(self) -> None:
        with pytest.raises(ValidationError):
            UserPortfolio(user_id=1, target_portfolio={"A": 40, "B": 50})

    def test_rejects_extra_fields(self) -> None:
        with pytest.raises(ValidationError):
            UserPortfolio(user_id=1, target_portfolio={"A": 100}, extra="nope")
