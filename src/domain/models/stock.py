from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from .ticker import Ticker


class Stock(BaseModel):
    ticker: Ticker = Field(description="ticker symbol of the stock")
    price: PositiveInt = Field(description="current price of the stock")
    tradable: bool = Field(description="Whether the stock is tradable or not")
    model_config = ConfigDict(extra="forbid", from_attributes=True)
