import time

from fastapi import APIRouter

from backend.app.agents.researcher import research
from backend.app.schemas import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    start_time = time.perf_counter()

    answer, sources = research(request.query)

    latency_ms = (time.perf_counter() - start_time) * 1000

    return QueryResponse(
        answer=answer,
        sources=sources,
        latency_ms=round(latency_ms, 2),
    )