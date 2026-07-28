from repositories import InMemoryStockRepository


class TestInMemoryStockRepository:
    def test_get_by_tickers_returns_only_known_tickers(
        self, stock_repo: InMemoryStockRepository
    ) -> None:
        stocks = stock_repo.get_by_tickers(["A", "B", "ZZZ"])

        assert set(stocks) == {"A", "B"}
        assert stocks["A"].price == 1000
        assert stocks["B"].price == 155

    def test_get_by_tickers_with_no_matches_returns_empty_dict(
        self, stock_repo: InMemoryStockRepository
    ) -> None:
        assert stock_repo.get_by_tickers(["ZZZ", "YYY"]) == {}
