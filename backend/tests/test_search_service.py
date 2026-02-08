import pytest
from app.services.search_service import SearchService, search_service

@pytest.mark.asyncio
async def test_search_service_search(mock_yt_service):
    """
    Test that search service calls YT service and returns results.
    """
    query = "Test Query"
    results = await search_service.search(query, limit=5)
    
    assert len(results) == 2
    assert results[0]['title'] == "Test Song"
    # Ensure YT service was called
    mock_yt_service.search_videos.assert_called_with(query, limit=20) # We fetch more to dedup

def test_deduplication_logic():
    """
    Test the deduplication logic in SearchService.
    """
    # Manually test private methods or logic if exposed, 
    # or rely on integration test above if logic is implicit.
    # Here we can test _is_duplicate if we make it accessible or test via public API behavior with mocked data containing dupes.
    
    # Let's mock a scenario with duplicates
    service = SearchService()
    
    existing = [
        {"id": "1", "title": "Song A", "artist": "Artist A", "duration": 180}
    ]
    
    # Exact duplicate ID
    assert service._is_duplicate({"id": "1", "title": "Song A", "artist": "Artist A", "duration": 180}, existing) == True
    
    # Same title/artist/duration but different ID
    assert service._is_duplicate({"id": "2", "title": "song a", "artist": "artist a", "duration": 180}, existing) == True
    
    # Different song
    assert service._is_duplicate({"id": "3", "title": "Song B", "artist": "Artist A", "duration": 180}, existing) == False
