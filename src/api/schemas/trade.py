from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from domain.const import MIN_TRADE_AMOUNT
from domain.models import Order, Ticker


class TradeRequest(BaseModel):
    amount: PositiveInt = Field(
        description="total amount of money to invest in the target portfolio, in yen",
        ge=MIN_TRADE_AMOUNT,
    )

    model_config = ConfigDict(extra="forbid", from_attributes=False)


class TradeResponse(BaseModel):
    amount: PositiveInt = Field(description="total trade amount, in yen")
    target_portfolio: dict[Ticker, int] = Field(
        description="target allocation of the portfolio, "
        "where key is the stock ticker and value is the target allocation percentage"
    )
    orders: list[Order] = Field(
        description="orders placed to fulfill the trade, one per eligible symbol"
    )

    model_config = ConfigDict(from_attributes=True)
