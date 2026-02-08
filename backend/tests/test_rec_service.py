import pytest
from app.services.rec_service import RecService

@pytest.mark.asyncio
async def test_smart_queue_generation(mock_yt_service):
    """
    Test Smart Queue generation logic.
    """
    service = RecService()
    current_song = {"id": "1", "title": "Current", "artist": "Artist", "duration": 180}
    history = [{"video_id": "old1"}]
    
    # Mock YT returns candidates
    mock_yt_service.search_videos.return_value = [
        {"id": "next1", "title": "Next Song", "artist": "Artist", "duration": 180}, # Same artist
        {"id": "next2", "title": "Other Song", "artist": "Different", "duration": 200},
        {"id": "video1", "title": "Test Song", "artist": "Test Artist", "duration": 180},
        {"id": "old1", "title": "Old Song", "artist": "Artist", "duration": 180} # In history
    ]
    
    queue = await service.generate_smart_queue(current_song, history, limit=5)
    
    # Logic verification:
    # 1. 'old1' should be filtered out (history)
    # 2. 'next1' and 'next2' should be in queue
    
    ids = [s['id'] for s in queue]
    assert "old1" not in ids
    assert "next1" in ids
    assert "next2" in ids
