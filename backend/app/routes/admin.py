from fastapi import APIRouter, Depends, HTTPException

# Todo: Add Admin role check dependency
router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/stats")
async def get_stats():
    return {"users": 0, "songs": 0}
