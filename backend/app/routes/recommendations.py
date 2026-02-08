from fastapi import APIRouter, Depends, HTTPException
from app.auth_utils import get_current_user
from app.services.rec_service import rec_service

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/home")
async def get_home_view(user = Depends(get_current_user)):
    """
    Returns the personalized Home view content:
    - Jump Back In
    - Made For You
    - Trending
    """
    try:
        content = await rec_service.get_home_recommendations(user['uid'])
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
