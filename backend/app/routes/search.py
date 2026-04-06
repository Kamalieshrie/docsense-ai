# ============================================================
# search.py — GET /api/search?q=your+query
# Semantic search across all stored documents
# ============================================================
from fastapi import APIRouter, Query
from app.storage.vector_store import semantic_search

router = APIRouter()


@router.get("/search")
async def search_documents(
    q: str = Query(..., description="Natural language search query")
):
    results = semantic_search(q, n_results=10)
    return {
        "query":   q,
        "total":   len(results),
        "results": results
    }