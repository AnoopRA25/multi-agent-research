from fastapi import APIRouter, HTTPException

from backend.app.database.research_repository import get_research_run
from backend.app.database.evaluation_repository import (
    create_evaluation,
    get_evaluation,
)
from backend.app.evaluation.evaluator import evaluate_report


router = APIRouter(prefix="/evaluate", tags=["Evaluation"])


@router.post("/{run_id}")
def evaluate_run(run_id: int):
    run = get_research_run(run_id)

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Research run not found",
        )

    if not run.get("report"):
        raise HTTPException(
            status_code=400,
            detail="Research run does not contain a report",
        )

    # Prevent unnecessary duplicate evaluations.
    existing = get_evaluation(run_id)

    if existing is not None:
        return existing

    # Temporary evaluation criteria.
    # These will later come from the evaluation dataset.
    criteria = [
        "key findings",
        "supporting evidence",
        "uncertainty",
        "limitations",
    ]

    result = evaluate_report(
        question=run["query"],
        report=run["report"],
        criteria=criteria,
    )

    evaluation_id = create_evaluation(
        run_id=run_id,
        relevance_score=result.relevance_score,
        completeness_score=result.completeness_score,
        evidence_score=result.evidence_score,
        factuality_score=result.factuality_score,
        overall_score=result.overall_score,
        feedback="\n".join(result.feedback),
    )

    evaluation = get_evaluation(run_id)

    return {
        "evaluation_id": evaluation_id,
        **evaluation,
    }


@router.get("/{run_id}")
def get_run_evaluation(run_id: int):
    run = get_research_run(run_id)

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Research run not found",
        )

    evaluation = get_evaluation(run_id)

    if evaluation is None:
        raise HTTPException(
            status_code=404,
            detail="Evaluation not found",
        )

    return evaluation