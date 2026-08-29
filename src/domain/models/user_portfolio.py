from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    computed_field,
)

from .ticker import Ticker


def _sums_to_100(v: dict[Ticker, PositiveInt]) -> dict[Ticker, PositiveInt]:
    sum_allocations = sum(v.values())
    if sum_allocations != 100:
        raise ValueError(f"allocations must sum to 100, got {sum_allocations}")
    return v


class UserPortfolio(BaseModel):
    user_id: PositiveInt = Field(description="user id of the target portfolio")
    target_portfolio: Annotated[dict[Ticker, PositiveInt], AfterValidator(_sums_to_100)] = Field(
        description="target allocation of the portfolio,"
        "where key is the stock ticker and value is the target allocation percentage",
    )

    @computed_field
    @property
    def tickers(self) -> list[Ticker]:
        return list(self.target_portfolio.keys())

    model_config = ConfigDict(extra="forbid", from_attributes=True)
