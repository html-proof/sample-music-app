from fastapi import APIRouter, Depends, HTTPException
from app.auth_utils import get_current_user
from app.services.stream_service import stream_service

router = APIRouter(prefix="/stream", tags=["Stream"])

@router.get("/{song_id}")
async def stream_song(song_id: str, user = Depends(get_current_user)):
    # In a full app, song_id might map to a database entry which has the yt_video_id
    # For now, we assume song_id IS the yt_video_id for simplicity, or we should look it up
    try:
        # Assuming song_id passed here is actually the YT video ID for now
        # OR we need a DB lookup: song = await db.get_song(song_id)
        # For this prototype level, let's treat song_id as yt_video_id or verify
        return await stream_service.get_stream(song_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/yt/{yt_video_id}")
async def stream_yt(yt_video_id: str, user = Depends(get_current_user)):
    try:
        return await stream_service.get_stream(yt_video_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
