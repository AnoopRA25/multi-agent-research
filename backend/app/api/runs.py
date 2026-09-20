from fastapi import APIRouter, HTTPException

from backend.app.database.research_repository import (
    get_research_run,
    list_research_runs,
)

router = APIRouter(prefix="/runs", tags=["Research Runs"])


@router.get("")
def get_runs():
    return {
        "runs": list_research_runs(),
    }


@router.get("/{run_id}")
def get_run(run_id: int):
    run = get_research_run(run_id)

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Research run not found",
        )

    return run