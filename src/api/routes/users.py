from fastapi import APIRouter, HTTPException, status


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/{user_id}/trades")
def user_trades():
    try:
        pass
    except HTTPException:
        raise HTTPException
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
