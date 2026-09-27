from backend.app.evaluation.dataset_loader import load_evaluation_dataset
from backend.app.evaluation.evaluator import evaluate_report


def test_regression_evaluation_dataset():
    dataset = load_evaluation_dataset()

    assert len(dataset) == 20

    for case in dataset:
        report = f"""
        Research findings related to {case["question"]}.

        The available evidence and research provide information
        about the key findings, applications, challenges,
        limitations, and uncertainty related to the topic.

        These findings should be interpreted with appropriate
        limitations because available evidence may be incomplete.
        """

        result = evaluate_report(
            question=case["question"],
            report=report,
            criteria=case["criteria"],
        )

        assert 0 <= result.relevance_score <= 10
        assert 0 <= result.completeness_score <= 10
        assert 0 <= result.evidence_score <= 10
        assert 0 <= result.factuality_score <= 10
        assert 0 <= result.overall_score <= 10


def test_regression_evaluation_produces_feedback():
    dataset = load_evaluation_dataset()

    case = dataset[0]

    result = evaluate_report(
        question=case["question"],
        report="A short research report.",
        criteria=case["criteria"],
    )

    assert isinstance(result.feedback, list)
    assert len(result.feedback) > 0