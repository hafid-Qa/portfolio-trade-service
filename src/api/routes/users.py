from fastapi import APIRouter, HTTPException, status
from pydantic import PositiveInt

from api.deps import TradeServiceDep
from api.schemas import TradeRequest, TradeResponse
from domain.exceptions import PortfolioNotFound


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
def user_trades(
    trade_service: TradeServiceDep,
    user_id: PositiveInt,
    trade: TradeRequest,
) -> TradeResponse:

    try:
        result = trade_service.create_trade(user_id, trade.amount)
    except PortfolioNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    return TradeResponse.model_validate(result)
