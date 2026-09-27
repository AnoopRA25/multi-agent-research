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


def _score_relevance(question: str, report: str) -> float:
    question_words = {
        word.lower().strip(".,?!")
        for word in question.split()
        if len(word) > 4
    }

    if not question_words:
        return 0.0

    report_lower = report.lower()

    matched = sum(
        word in report_lower
        for word in question_words
    )

    return round(
        min(10.0, (matched / len(question_words)) * 10),
        2,
    )


def _score_evidence(report: str) -> float:
    report_lower = report.lower()

    evidence_keywords = [
        "evidence",
        "study",
        "research",
        "source",
        "according",
        "data",
        "report",
        "finding",
        "findings",
    ]

    matches = sum(
        keyword in report_lower
        for keyword in evidence_keywords
    )

    return round(
        min(10.0, (matches / 4) * 10),
        2,
    )


def _score_factuality(report: str) -> float:
    """
    Deterministic proxy for factual consistency.

    This does not verify facts against external sources.
    It checks whether the report avoids obvious unsupported
    certainty and acknowledges limitations/uncertainty.
    """

    report_lower = report.lower()

    uncertainty_keywords = [
        "uncertainty",
        "uncertain",
        "limitation",
        "limitations",
        "may",
        "might",
        "could",
        "available evidence",
    ]

    matched = sum(
        keyword in report_lower
        for keyword in uncertainty_keywords
    )

    if not report.strip():
        return 0.0

    if matched >= 4:
        return 10.0

    if matched >= 2:
        return 7.5

    if matched >= 1:
        return 5.0

    return 3.0


def evaluate_report(
    question: str,
    report: str,
    criteria: list[str],
) -> EvaluationResult:

    relevance_score = _score_relevance(
        question,
        report,
    )

    completeness_score = _score_criteria(
        report,
        criteria,
    )

    evidence_score = _score_evidence(
        report,
    )

    factuality_score = _score_factuality(
        report,
    )

    feedback = []

    if relevance_score < 7:
        feedback.append(
            "The report may not directly address enough of the research question."
        )

    if completeness_score < 7:
        feedback.append(
            "The report may not cover enough of the evaluation criteria."
        )

    if evidence_score < 5:
        feedback.append(
            "The report contains limited explicit evidence-related language."
        )

    if factuality_score < 7:
        feedback.append(
            "The report contains limited explicit uncertainty or limitation language."
        )

    overall_score = round(
        (
            relevance_score
            + completeness_score
            + evidence_score
            + factuality_score
        ) / 4,
        2,
    )

    if not feedback:
        feedback.append(
            "The report satisfies the deterministic evaluation checks."
        )

    return EvaluationResult(
        relevance_score=relevance_score,
        completeness_score=completeness_score,
        evidence_score=evidence_score,
        factuality_score=factuality_score,
        overall_score=overall_score,
        feedback=feedback,
    )