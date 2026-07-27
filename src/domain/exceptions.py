class PortfolioNotFound(Exception):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"No portfolio found for user {user_id}")


class UnknownStocksInPortfolio(Exception):
    def __init__(self, tickers: list[str]) -> None:
        self.tickers = tickers
        super().__init__(f"Stocks not found in catalogue: {', '.join(tickers)}")
