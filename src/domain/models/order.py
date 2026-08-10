from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from .types import Ticker


class Order(BaseModel):
    symbol: Ticker = Field(description="ticker symbol of the stock")
    amount: PositiveInt = Field(description="order amount allocated to the symbol, in yen")
    quantity_units: PositiveInt = Field(
        description="quantity to purchase, as an integer count of 1/QUANTITY_PRECISION share units"
    )

    model_config = ConfigDict(extra="forbid", from_attributes=True)
