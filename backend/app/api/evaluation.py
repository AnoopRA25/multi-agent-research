from fastapi import APIRouter, HTTPException

from backend.app.database.research_repository import get_research_run
from backend.app.database.evaluation_repository import (
    create_evaluation,
    get_evaluation,
    get_evaluation_summary,
)
from backend.app.evaluation.evaluator import evaluate_report
from backend.app.evaluation.dataset_loader import load_evaluation_dataset


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

    # Load evaluation criteria from the dataset.
    dataset = load_evaluation_dataset()

    case = next(
        (
            item
            for item in dataset
            if item["question"].strip().lower()
            == run["query"].strip().lower()
        ),
        None,
    )

    if case is None:
        raise HTTPException(
            status_code=400,
            detail="No evaluation criteria found for this research question",
        )

    criteria = case["criteria"]

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


@router.get("/summary")
def evaluation_summary():
    return get_evaluation_summary()


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

