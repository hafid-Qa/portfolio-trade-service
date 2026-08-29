from pydantic import BaseModel, ConfigDict, PositiveInt

from .order import Order
from .ticker import Ticker


class TradeResult(BaseModel):
    amount: PositiveInt
    target_portfolio: dict[Ticker, int]
    orders: list[Order]

    model_config = ConfigDict(frozen=True)
