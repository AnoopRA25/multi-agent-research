import time

from fastapi import APIRouter, BackgroundTasks

from backend.app.database.database import initialize_database
from backend.app.database.research_repository import (
    create_research_run,
    update_research_run,
)
from backend.app.graph.workflow import research_graph
from backend.app.schemas import JobResponse, QueryRequest


router = APIRouter()

initialize_database()


def run_research_job(run_id: int, query: str) -> None:
    start_time = time.perf_counter()

    # Mark the job as running before starting the workflow.
    update_research_run(
        run_id=run_id,
        report="",
        critique="",
        latency_ms=0,
        status="running",
    )

    try:
        # Test-only failure condition.
        # This does NOT call Gemini.
        # if query == "__TEST_FAILURE__":
        #     raise RuntimeError("Intentional test failure")

        initial_state = {
            "run_id": run_id,
            "query": query,
            "revision_count": 0,
        }

        final_state = research_graph.invoke(initial_state)

        latency_ms = (time.perf_counter() - start_time) * 1000

        update_research_run(
            run_id=run_id,
            report=final_state["report"],
            critique=final_state.get("critique", ""),
            latency_ms=round(latency_ms, 2),
            status="completed",
        )

    except Exception as exc:
        latency_ms = (time.perf_counter() - start_time) * 1000

        update_research_run(
            run_id=run_id,
            report="",
            critique=str(exc),
            latency_ms=round(latency_ms, 2),
            status="failed",
        )


@router.post("/query", response_model=JobResponse)
def query(
    request: QueryRequest,
    background_tasks: BackgroundTasks,
):
    run_id = create_research_run(
        query=request.query,
        report="",
        critique="",
        latency_ms=0,
        status="queued",
    )

    background_tasks.add_task(
        run_research_job,
        run_id,
        request.query,
    )

    return JobResponse(
        run_id=run_id,
        status="queued",
    )