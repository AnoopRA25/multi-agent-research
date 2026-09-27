from backend.app.database.evaluation_repository import (
    create_evaluation,
    get_evaluation,
)
from backend.app.database.research_repository import get_research_run
from backend.app.evaluation.dataset_loader import load_evaluation_dataset
from backend.app.evaluation.evaluator import evaluate_report


def evaluate_runs(run_ids: list[int]) -> list[dict]:
    dataset = load_evaluation_dataset()

    results = []

    for run_id in run_ids:
        run = get_research_run(run_id)

        if run is None:
            results.append(
                {
                    "run_id": run_id,
                    "status": "not_found",
                }
            )
            continue

        if not run.get("report"):
            results.append(
                {
                    "run_id": run_id,
                    "status": "no_report",
                }
            )
            continue

        existing = get_evaluation(run_id)

        if existing is not None:
            results.append(
                {
                    "run_id": run_id,
                    "evaluation_id": existing["id"],
                    "overall_score": existing["overall_score"],
                    "status": "already_evaluated",
                }
            )
            continue

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
            results.append(
                {
                    "run_id": run_id,
                    "status": "no_matching_dataset_case",
                }
            )
            continue

        evaluation = evaluate_report(
            question=run["query"],
            report=run["report"],
            criteria=case["criteria"],
        )

        evaluation_id = create_evaluation(
            run_id=run_id,
            relevance_score=evaluation.relevance_score,
            completeness_score=evaluation.completeness_score,
            evidence_score=evaluation.evidence_score,
            factuality_score=evaluation.factuality_score,
            overall_score=evaluation.overall_score,
            feedback="\n".join(evaluation.feedback),
        )

        results.append(
            {
                "run_id": run_id,
                "evaluation_id": evaluation_id,
                "overall_score": evaluation.overall_score,
                "status": "evaluated",
            }
        )

    return results