from fastapi import APIRouter,Request
from app.recommender import get_recommendations

router = APIRouter()

@router.post("/recommend")
async def recommend(request: Request):
    try:
        body = await request.json()
        query = body.get("query")
        url = body.get("url")
        print("Received:", query, url)

        results = get_recommendations(query=query, url=url)
        return results
    except Exception as e:
        import traceback
        traceback.print_exc()  # Shows full traceback in terminal
        return {"error": str(e)}
