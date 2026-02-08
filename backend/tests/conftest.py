import pytest
import pytest_asyncio
from httpx import AsyncClient
from unittest.mock import MagicMock
import sys
import os
# Add backend to path
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_path not in sys.path:
    sys.path.append(backend_path)

# MOCK AUTH_UTILS BEFORE IMPORTING APP
mock_utils = MagicMock()
mock_utils.get_current_user.return_value = {"uid": "test_user"}
sys.modules["app.auth_utils"] = mock_utils

from app.main import app

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
def mock_firebase_setup(mocker):
    """
    Mock all Firebase interactions globally.
    """
    # Mock initialize_app
    mocker.patch("app.firebase.initialize_firebase")
    mocker.patch("firebase_admin.initialize_app")
    
    # Mock Firestore
    mock_firestore = MagicMock()
    mocker.patch("firebase_admin.firestore.client", return_value=mock_firestore)
    mock_firestore.collection.return_value.document.return_value.get.return_value.exists = False
    mock_firestore.collection.return_value.document.return_value.get.return_value.to_dict.return_value = {}
    
    # Mock Auth
    mock_auth_admin = MagicMock()
    mocker.patch("firebase_admin.auth.verify_id_token", return_value={"uid": "test_user"})
    
    # Mock RTDB
    mock_db = MagicMock()
    mocker.patch("firebase_admin.db.reference", return_value=MagicMock())
    
    return {
        "firestore": mock_firestore,
        "auth": mock_auth_admin,
        "db": mock_db
    }

@pytest.fixture
def mock_yt_service(mocker):
    """
    Mock YTService to avoid calling YouTube API.
    """
    mock_service = MagicMock()
    # Mock search_videos return
    mock_service.search_videos.return_value = [
        {"id": "video1", "title": "Test Song", "artist": "Test Artist", "duration": 180},
        {"id": "video2", "title": "Another Song", "artist": "Another Artist", "duration": 200}
    ]
    # Mock get_stream_url return
    mock_service.get_stream_url.return_value = {
        "url": "http://mock.stream/url",
        "duration": 180,
        "title": "Test Song",
        "uploader": "Test Artist"
    }
    mocker.patch("app.services.yt_service.yt_service", mock_service)
    return mock_service
