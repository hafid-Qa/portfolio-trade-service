from repositories import InMemoryUserPortfolioRepository


class TestInMemoryUserPortfolioRepository:
    def test_get_by_user_id_returns_matching_portfolio(
        self, portfolio_repo: InMemoryUserPortfolioRepository
    ) -> None:
        portfolio = portfolio_repo.get_by_user_id(1)

        assert portfolio is not None
        assert portfolio.user_id == 1
        assert portfolio.target_portfolio == {"A": 40, "B": 60}

    def test_get_by_user_id_returns_none_for_unknown_user(
        self, portfolio_repo: InMemoryUserPortfolioRepository
    ) -> None:
        assert portfolio_repo.get_by_user_id(999) is None
