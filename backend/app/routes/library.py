from fastapi import APIRouter, Depends
from app.auth_utils import get_current_user

router = APIRouter(prefix="/library", tags=["Library"])

@router.get("/liked")
async def get_liked_songs(user = Depends(get_current_user)):
    return {"liked_songs": []}

@router.post("/like")
async def like_song(song_id: str, user = Depends(get_current_user)):
    return {"status": "liked"}
