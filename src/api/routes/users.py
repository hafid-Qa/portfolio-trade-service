from fastapi import APIRouter
from pydantic import PositiveInt

from api.schemas import TradeRequest, TradeResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/{user_id}/trades",
    response_model=TradeResponse,
    summary="Create a trade for a user",
    description=(
        "Calculates buy orders for a user's target portfolio from a given trade amount. "
        "The amount is apportioned across the portfolio's stocks by their target percentages; "
        "stocks that are not tradable or whose allocation falls below the minimum order amount "
        "are excluded and the remainder is redistributed among the rest."
    ),
)
def user_trades(user_id: PositiveInt, trade: TradeRequest) -> TradeResponse:
    ...
    # try:
    #     pass
    # except HTTPException:
    #     raise
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
