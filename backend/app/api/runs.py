from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.database.execution_repository import list_agent_executions
from backend.app.database.research_repository import (
    get_research_run,
    list_research_runs,
)


router = APIRouter(prefix="/runs", tags=["Research Runs"])


class RunStatusResponse(BaseModel):
    run_id: int
    query: str
    status: str
    report: str
    critique: str
    latency_ms: float


@router.get("")
def get_runs():
    return {"runs": list_research_runs()}


@router.get("/{run_id}", response_model=RunStatusResponse)
def get_run(run_id: int):
    run = get_research_run(run_id)

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Research run not found",
        )

    return RunStatusResponse(
        run_id=run["id"],
        query=run["query"],
        status=run["status"],
        report=run["report"] or "",
        critique=run["critique"] or "",
        latency_ms=run["latency_ms"] or 0,
    )


@router.get("/{run_id}/executions")
def get_run_executions(run_id: int):
    run = get_research_run(run_id)

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Research run not found",
        )

    return {
        "run_id": run_id,
        "executions": list_agent_executions(run_id),
    }