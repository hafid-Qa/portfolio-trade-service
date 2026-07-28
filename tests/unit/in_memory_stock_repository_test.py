from repositories import InMemoryStockRepository


class TestInMemoryStockRepository:
    def test_get_by_ticker_returns_matching_stock(
        self, stock_repo: InMemoryStockRepository
    ) -> None:
        stock = stock_repo.get_by_ticker("A")

        assert stock is not None
        assert stock.ticker == "A"
        assert stock.price == 1000
        assert stock.tradable is True

    def test_get_by_ticker_returns_none_for_unknown_ticker(
        self, stock_repo: InMemoryStockRepository
    ) -> None:
        assert stock_repo.get_by_ticker("ZZZ") is None

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
