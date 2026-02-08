from fastapi import APIRouter, Depends, HTTPException, Body
from app.auth_utils import get_current_user
from app.services.user_service import user_service

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/onboarding")
async def save_onboarding(data: dict = Body(...), user = Depends(get_current_user)):
    """
    Saves user onboarding preferences (Country, Language, Artists, Modes).
    """
    try:
        await user_service.save_onboarding_data(user['uid'], data)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/profile")
async def get_profile(user = Depends(get_current_user)):
    # Fetch detailed profile from DB
    return {"uid": user['uid'], "profile": {}}
