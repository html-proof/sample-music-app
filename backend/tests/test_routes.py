import pytest

@pytest.mark.asyncio
async def test_health_check(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_search_endpoint(async_client, mock_yt_service, mocker):
    """
    Test the /search endpoint.
    """
    # Mock auth dependency
    mocker.patch("app.routes.search.get_current_user", return_value={"uid": "test_user"})
    
    response = await async_client.get("/?q=test")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]['title'] == "Test Song"
