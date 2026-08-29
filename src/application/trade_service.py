from domain.exceptions import PortfolioNotFound, UnknownStocksInPortfolio
from domain.models import TradeResult
from domain.repositories import StockRepository, UserPortfolioRepository
from domain.services import TradeCalculator


class TradeService:
    def __init__(
        self,
        stock_repo: StockRepository,
        portfolio_repo: UserPortfolioRepository,
        trade_calculator: TradeCalculator,
    ) -> None:
        self.stock_repo = stock_repo
        self.portfolio_repo = portfolio_repo
        self.trade_calculator = trade_calculator

    def create_trade(self, user_id: int, amount: int) -> TradeResult:
        portfolio = self.portfolio_repo.get_by_user_id(user_id)
        if portfolio is None:
            raise PortfolioNotFound(user_id)
        tickers = portfolio.tickers

        stocks = self.stock_repo.get_by_tickers(tickers)
        missing = set(tickers) - stocks.keys()

        if missing:
            raise UnknownStocksInPortfolio(sorted(missing))

        orders = self.trade_calculator.calculate(portfolio=portfolio, stocks=stocks, amount=amount)

        return TradeResult(
            amount=amount,
            target_portfolio=portfolio.target_portfolio,
            orders=orders,
        )
