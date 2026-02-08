from fastapi import APIRouter, Depends, Query, HTTPException
from app.auth_utils import get_current_user
from app.services.search_service import search_service
from typing import Optional

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
async def search_songs(q: str, limit: int = 10, user = Depends(get_current_user)):
    """
    Quick Search: Returns top N clean, unique song results.
    """
    if not q:
        return {"results": []}
    
    try:
        # The service now handles deduplication and strict filtering
        results = await search_service.search(q, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/suggestions")
async def get_suggestions(q: str):
    # For now, suggestions can just be a lighter search or distinct logic
    # We could implement a specific suggestion service method later
    if not q:
        return {"suggestions": []}
    return {"suggestions": []} # Todo: Implement suggestions logic
