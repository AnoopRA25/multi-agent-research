from dataclasses import dataclass


@dataclass
class EvaluationResult:
    relevance_score: float
    completeness_score: float
    evidence_score: float
    factuality_score: float
    overall_score: float
    feedback: list[str]


def _score_criteria(report: str, criteria: list[str]) -> float:
    if not criteria:
        return 0.0

    report_lower = report.lower()

    matched = 0

    for criterion in criteria:
        keywords = [
            word.lower()
            for word in criterion.split()
            if len(word) > 4
        ]

        if any(keyword in report_lower for keyword in keywords):
            matched += 1

    return round((matched / len(criteria)) * 10, 2)


def evaluate_report(
    question: str,
    report: str,
    criteria: list[str],
) -> EvaluationResult:
    report_lower = report.lower()

    relevance_score = 10.0 if any(
        word.lower() in report_lower
        for word in question.split()
        if len(word) > 4
    ) else 0.0

    completeness_score = _score_criteria(
        report,
        criteria,
    )

    evidence_keywords = [
        "evidence",
        "study",
        "research",
        "source",
        "according",
        "data",
        "report",
    ]

    evidence_matches = sum(
        keyword in report_lower
        for keyword in evidence_keywords
    )

    evidence_score = min(
        10.0,
        round((evidence_matches / 4) * 10, 2),
    )

    factuality_score = 10.0

    feedback = []

    if relevance_score < 10:
        feedback.append(
            "The report may not directly address the research question."
        )

    if completeness_score < 7:
        feedback.append(
            "The report may not cover enough of the evaluation criteria."
        )

    if evidence_score < 5:
        feedback.append(
            "The report contains limited explicit evidence-related language."
        )

    overall_score = round(
        (
            relevance_score
            + completeness_score
            + evidence_score
            + factuality_score
        )
        / 4,
        2,
    )

    if not feedback:
        feedback.append(
            "The report satisfies the basic deterministic evaluation checks."
        )

    return EvaluationResult(
        relevance_score=relevance_score,
        completeness_score=completeness_score,
        evidence_score=evidence_score,
        factuality_score=factuality_score,
        overall_score=overall_score,
        feedback=feedback,
    )