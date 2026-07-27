from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, PositiveInt

from .types import Ticker, sums_to_100


class UserPortfolio(BaseModel):
    user_id: PositiveInt = Field(description="user id of the target portfolio")
    target_portfolio: Annotated[dict[Ticker, PositiveInt], AfterValidator(sums_to_100)] = Field(
        description="target allocation of the portfolio,"
        "where key is the stock ticker and value is the target allocation percentage",
    )

    model_config = ConfigDict(extra="forbid", from_attributes=True)
