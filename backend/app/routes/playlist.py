from fastapi import APIRouter, Depends
from app.auth_utils import get_current_user
from typing import List

router = APIRouter(prefix="/playlist", tags=["Playlist"])

@router.post("/create")
async def create_playlist(name: str, user = Depends(get_current_user)):
    return {"playlist_id": "new_id", "name": name}

@router.get("/my")
async def get_my_playlists(user = Depends(get_current_user)):
    return {"playlists": []}

@router.post("/{playlist_id}/add")
async def add_song_to_playlist(playlist_id: str, song_id: str, user = Depends(get_current_user)):
    return {"status": "added"}
