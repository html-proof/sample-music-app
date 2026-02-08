from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from app.auth_utils import get_current_user
from models.schemas import PlaybackState
from app.services.rec_service import rec_service
from app.services.user_service import user_service

router = APIRouter(prefix="/player", tags=["Player"])

from app.websocket_manager import manager

@router.post("/queue/generate")
async def generate_queue(current_song: PlaybackState, user = Depends(get_current_user)):
    """
    Generates a smart queue based on the current song.
    """
    try:
        # In a real app we'd fetch history from DB
        history = [] 
        queue = await rec_service.generate_smart_queue(current_song.dict(), history)
        
        # Update RTDB
        await user_service.update_playback_state(user['uid'], {'queue': queue, 'current_song': current_song.dict()})
        
        # Broadcast to devices
        await manager.send_personal_message({"type": "QUEUE_UPDATE", "data": queue}, user['uid'])
        
        return {"queue": queue}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/now-playing")
async def get_now_playing(user = Depends(get_current_user)):
    return {"status": "idle"}

@router.post("/now-playing")
async def update_now_playing(state: PlaybackState, user = Depends(get_current_user)):
    return {"status": "updated"}
