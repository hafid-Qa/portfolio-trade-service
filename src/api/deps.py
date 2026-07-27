from typing import Annotated

from fastapi import Depends, Request

from domain.repositories import StockRepository, UserPortfolioRepository
from domain.services import TradeCalculator, TradeService
from settings import Settings, get_settings


SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_stock_repo(request: Request) -> StockRepository:
    return request.app.state.stock_repo


def get_portfolio_repo(request: Request) -> UserPortfolioRepository:
    return request.app.state.portfolio_repo


def get_trade_calculator() -> TradeCalculator:
    return TradeCalculator()


StockRepoDep = Annotated[StockRepository, Depends(get_stock_repo)]
PortfolioRepoDep = Annotated[UserPortfolioRepository, Depends(get_portfolio_repo)]
TradeCalculatorDep = Annotated[TradeCalculator, Depends(get_trade_calculator)]


def get_trade_service(
    stock_repo: StockRepoDep, portfolio_repo: PortfolioRepoDep, trade_calculator: TradeCalculatorDep
) -> TradeService:
    return TradeService(stock_repo, portfolio_repo, trade_calculator)


TradeServiceDep = Annotated[TradeService, Depends(get_trade_service)]
