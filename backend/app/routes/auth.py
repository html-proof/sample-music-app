from fastapi import APIRouter, Depends
from app.auth_utils import get_current_user
from app.services.user_service import user_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/me")
async def get_current_user_profile(user = Depends(get_current_user)):
    # This endpoint is called on frontend init. 
    # We ensure the user exists in our DB.
    
    uid = user['uid']
    email = user.get('email')
    picture = user.get('picture')
    name = user.get('name')
    
    # Auto-create or get profile
    profile = await user_service.create_user_profile(uid, email, name, picture)
    
    return {"uid": uid, "email": email, "profile": profile}
