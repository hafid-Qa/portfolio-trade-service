from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, PositiveInt

from .types import Ticker


class Order(BaseModel):
    symbol: Ticker = Field(description="ticker symbol of the stock")
    amount: PositiveInt = Field(description="order amount allocated to the symbol, in yen")
    quantity: PositiveFloat = Field(
        description="quantity of shares/units to purchase, precise to 3 decimal places"
    )

    model_config = ConfigDict(extra="forbid", from_attributes=True)
