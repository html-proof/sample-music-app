import pytest
import pandas as pd
from app.services.ml_service import MLService
from unittest.mock import MagicMock, patch

@pytest.mark.asyncio
async def test_train_als_model(mocker):
    """
    Test ALS model training with mocked interactions.
    """
    mock_user_service = mocker.patch("app.services.ml_service.user_service")
    mock_user_service.get_all_interactions.return_value = [
        {'user_id': 'u1', 'video_id': 'v1', 'weight': 1},
        {'user_id': 'u2', 'video_id': 'v2', 'weight': 1}
    ]
    
    service = MLService()
    
    # Mock implicit to avoid actual heavy training
    mock_als = mocker.patch("implicit.als.AlternatingLeastSquares")
    mock_model_instance = MagicMock()
    mock_als.return_value = mock_model_instance
    
    await service.train_als_model()
    
    mock_user_service.get_all_interactions.assert_called_once()
    mock_model_instance.fit.assert_called_once()
    assert len(service.user_map) > 0
    assert len(service.item_map) > 0

def test_get_recommendations():
    """
    Test generating recommendations with a mocked model.
    """
    service = MLService()
    service.model = MagicMock()
    service.user_map = {0: 'u1'}
    service.item_map = {'v1': 0, 'v2': 1}
    service.reverse_item_map = {0: 'v1', 1: 'v2'}
    
    # Mock recommend output (ids, scores)
    service.model.recommend.return_value = ([0, 1], [0.9, 0.8])
    
    recs = service.get_recommendations('u1', n=2)
    assert recs == ['v1', 'v2']
    
    # Test unknown user
    recs = service.get_recommendations('unknown')
    assert recs == []
