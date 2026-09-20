from fastapi import APIRouter, HTTPException

from backend.app.database.execution_repository import (
    list_agent_executions,
)
from backend.app.database.research_repository import (
    get_research_run,
    list_research_runs,
)

router = APIRouter(prefix="/runs", tags=["Research Runs"])


@router.get("")
def get_runs():
    return {"runs": list_research_runs()}


@router.get("/{run_id}")
def get_run(run_id: int):
    run = get_research_run(run_id)

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Research run not found",
        )

    return run


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