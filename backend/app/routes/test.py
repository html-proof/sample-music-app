from fastapi import APIRouter
from app.services.stream_service import stream_service

router = APIRouter(prefix="/test", tags=["Testing"])

@router.get("/stream/{video_id}")
async def test_stream(video_id: str):
    """
    Test endpoint for performance testing (NO AUTH REQUIRED).
    Use this for local testing only. Remove in production.
    """
    return await stream_service.get_stream(video_id)
