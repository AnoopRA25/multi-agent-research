from backend.app.evaluation.dataset_loader import load_evaluation_dataset
from backend.app.evaluation.evaluator import evaluate_report


def run_regression_evaluation() -> dict:
    dataset = load_evaluation_dataset()

    results = []

    for case in dataset:
        report = f"""
        Research findings related to {case["question"]}.

        The available evidence and research provide information
        about the key findings, applications, challenges,
        limitations, and uncertainty related to the topic.

        These findings should be interpreted with appropriate
        limitations because available evidence may be incomplete.
        """

        evaluation = evaluate_report(
            question=case["question"],
            report=report,
            criteria=case["criteria"],
        )

        results.append(
            {
                "id": case["id"],
                "relevance": evaluation.relevance_score,
                "completeness": evaluation.completeness_score,
                "evidence": evaluation.evidence_score,
                "factuality": evaluation.factuality_score,
                "overall": evaluation.overall_score,
            }
        )

    if not results:
        return {
            "total_cases": 0,
            "average_relevance": 0.0,
            "average_completeness": 0.0,
            "average_evidence": 0.0,
            "average_factuality": 0.0,
            "average_overall": 0.0,
            "results": [],
        }

    total = len(results)

    return {
        "total_cases": total,
        "average_relevance": round(
            sum(item["relevance"] for item in results) / total,
            2,
        ),
        "average_completeness": round(
            sum(item["completeness"] for item in results) / total,
            2,
        ),
        "average_evidence": round(
            sum(item["evidence"] for item in results) / total,
            2,
        ),
        "average_factuality": round(
            sum(item["factuality"] for item in results) / total,
            2,
        ),
        "average_overall": round(
            sum(item["overall"] for item in results) / total,
            2,
        ),
        "results": results,
    }