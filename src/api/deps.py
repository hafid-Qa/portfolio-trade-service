from typing import Annotated

from fastapi import Depends, Request

from repositories import StockRepository, UserPortfolioRepository
from settings import Settings, get_settings


SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_stock_repo(request: Request) -> StockRepository:
    return request.app.state.stock_repo


def get_portfolio_repo(request: Request) -> UserPortfolioRepository:
    return request.app.state.portfolio_repo


StockRepoDep = Annotated[StockRepository, Depends(get_stock_repo)]
PortfolioRepoDep = Annotated[UserPortfolioRepository, Depends(get_portfolio_repo)]
