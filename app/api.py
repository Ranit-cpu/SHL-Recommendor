from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.recommender import get_recommendations

router = APIRouter()

class RecommendationRequest(BaseModel):
    query: Optional[str] = None
    url: Optional[str] = None

@router.post("/recommend")
async def recommend(request: RecommendationRequest):
    try:
        if not request.query and not request.url:
            raise HTTPException(status_code=400, detail="Either 'query' or 'url' must be provided.")

        results = get_recommendations(query=request.query, url=request.url)
        return results
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
