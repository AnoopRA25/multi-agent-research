import time

from fastapi import APIRouter, HTTPException

from backend.app.database.database import initialize_database
from backend.app.database.research_repository import (
    create_research_run,
    update_research_run,
)
from backend.app.graph.workflow import research_graph
from backend.app.schemas import QueryRequest, QueryResponse

router = APIRouter()

initialize_database()


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    start_time = time.perf_counter()

    run_id = create_research_run(
        query=request.query,
        report="",
        critique="",
        latency_ms=0,
        status="running",
    )

    try:
        initial_state = {
            "run_id": run_id,
            "query": request.query,
            "revision_count": 0,
        }

        final_state = research_graph.invoke(initial_state)

    except Exception as exc:
        latency_ms = (time.perf_counter() - start_time) * 1000

        update_research_run(
            run_id=run_id,
            report="",
            critique=str(exc),
            latency_ms=round(latency_ms, 2),
            status="failed",
        )

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    latency_ms = (time.perf_counter() - start_time) * 1000

    report = final_state["report"]
    critique = final_state.get("critique", "")

    update_research_run(
        run_id=run_id,
        report=report,
        critique=critique,
        latency_ms=round(latency_ms, 2),
        status="completed",
    )

    return QueryResponse(
        run_id=run_id,
        answer=report,
        sources=final_state.get("sources", []),
        critique=critique,
        latency_ms=round(latency_ms, 2),
    )