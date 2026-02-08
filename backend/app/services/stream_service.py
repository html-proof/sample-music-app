from app.services.yt_service import yt_service
from app.services.analytics_service import analytics_service
from fastapi import HTTPException

class StreamService:
    async def get_stream(self, video_id: str):
        """
        Get stream URL with caching support.
        Returns enhanced metadata including cache status and fetch time.
        """
        stream_data = await yt_service.get_stream_url(video_id)
        
        if not stream_data:
            raise HTTPException(status_code=404, detail="Stream not found")
        
        # Return full enhanced response
        return {
            "video_id": stream_data.get("video_id"),
            "stream_url": stream_data.get("stream_url"),
            "duration": stream_data.get("duration"),
            "title": stream_data.get("title"),
            "artist": stream_data.get("artist"),
            "thumbnail": stream_data.get("thumbnail"),
            "cached": stream_data.get("cached", False),
            "fetch_time_ms": stream_data.get("fetch_time_ms", 0)
        }

stream_service = StreamService()
