import time

from fastapi import APIRouter, HTTPException

from backend.app.database.database import initialize_database
from backend.app.database.research_repository import create_research_run
from backend.app.graph.workflow import research_graph
from backend.app.schemas import QueryRequest, QueryResponse

router = APIRouter()

initialize_database()


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    start_time = time.perf_counter()

    try:
        initial_state = {
            "query": request.query,
            "revision_count": 0,
        }

        final_state = research_graph.invoke(initial_state)

    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    latency_ms = (time.perf_counter() - start_time) * 1000

    run_id = create_research_run(
        query=request.query,
        report=final_state["report"],
        critique=final_state.get("critique", ""),
        latency_ms=round(latency_ms, 2),
    )

    return QueryResponse(
        run_id=run_id,
        answer=final_state["report"],
        sources=final_state.get("sources", []),
        critique=final_state.get("critique", ""),
        latency_ms=round(latency_ms, 2),
    )