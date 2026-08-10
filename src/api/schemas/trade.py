from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, field_validator

from domain.const import MIN_TRADE_AMOUNT, QUANTITY_PRECISION
from domain.models import Order, Ticker


_QUANTITY_EXPONENT = -(len(str(QUANTITY_PRECISION)) - 1)


class TradeRequest(BaseModel):
    amount: PositiveInt = Field(
        description="total amount of money to invest in the target portfolio, in yen",
        ge=MIN_TRADE_AMOUNT,
    )

    model_config = ConfigDict(extra="forbid", from_attributes=False)


class OrderResponse(BaseModel):
    symbol: Ticker = Field(description="ticker symbol of the stock")
    amount: PositiveInt = Field(description="order amount allocated to the symbol, in yen")
    quantity: Decimal = Field(
        description="quantity of shares/units to purchase, precise to 3 decimal places"
    )

    model_config = ConfigDict(extra="forbid", from_attributes=True)

    @classmethod
    def from_order(cls, order: Order) -> "OrderResponse":
        """Places the decimal point QUANTITY_PRECISION implies; the domain layer only
        ever carries the integer unit count. scaleb shifts the decimal point without
        renormalizing, so trailing zeros survive (10000 units -> 10.000, not 10)."""
        return cls(
            symbol=order.symbol,
            amount=order.amount,
            quantity=Decimal(order.quantity_units).scaleb(_QUANTITY_EXPONENT),
        )


class TradeResponse(BaseModel):
    amount: PositiveInt = Field(description="total trade amount, in yen")
    target_portfolio: dict[Ticker, int] = Field(
        description="target allocation of the portfolio, "
        "where key is the stock ticker and value is the target allocation percentage"
    )
    orders: list[OrderResponse] = Field(
        description="orders placed to fulfill the trade, one per eligible symbol"
    )

    model_config = ConfigDict(from_attributes=True)

    @field_validator("orders", mode="before")
    @classmethod
    def _convert_domain_orders(cls, orders: list[Order] | list[dict]) -> list[object]:
        return [
            OrderResponse.from_order(order) if isinstance(order, Order) else order
            for order in orders
        ]
