import pytest
from app.services.device_service import DeviceService
from unittest.mock import MagicMock

def test_register_device(mock_firebase_admin):
    """
    Test device registration using mocked Firebase DB.
    """
    service = DeviceService()
    
    # Mock DB reference
    mock_db = mock_firebase_admin.db
    mock_ref = MagicMock()
    mock_db.reference.return_value = mock_ref
    
    # Mock active device check to return None so it sets new one
    mock_ref.get.return_value = None 
    
    success = service.register_device("u1", "d1", {"name": "Test Device"})
    
    assert success == True
    mock_ref.set.assert_called()

def test_active_device_locking(mock_firebase_admin):
    """
    Test setting and getting active device.
    """
    service = DeviceService()
    mock_db = mock_firebase_admin.db
    
    # Mock getting active device
    mock_ref = MagicMock()
    mock_db.reference.return_value = mock_ref
    mock_ref.get.return_value = "d1"
    
    assert service.get_active_device("u1") == "d1"
