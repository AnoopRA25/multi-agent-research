from backend.app.evaluation.evaluator import evaluate_report


def test_evaluate_report_returns_scores():
    result = evaluate_report(
        question="What are the major applications of generative AI?",
        report=(
            "Generative AI has major applications in software development "
            "and content creation. Research and evidence show that these "
            "systems are increasingly used in multiple industries."
        ),
        criteria=[
            "Identifies major application areas",
            "Provides supporting evidence",
            "Explains important use cases",
        ],
    )

    assert 0 <= result.relevance_score <= 10
    assert 0 <= result.completeness_score <= 10
    assert 0 <= result.evidence_score <= 10
    assert 0 <= result.factuality_score <= 10
    assert 0 <= result.overall_score <= 10


def test_empty_report_gets_low_scores():
    result = evaluate_report(
        question="What are the applications of generative AI?",
        report="",
        criteria=[
            "Identifies major application areas",
            "Provides supporting evidence",
        ],
    )

    assert result.relevance_score == 0
    assert result.completeness_score == 0
    assert result.evidence_score == 0


def test_feedback_is_generated():
    result = evaluate_report(
        question="What are the applications of generative AI?",
        report="",
        criteria=[
            "Identifies major application areas",
        ],
    )

    assert isinstance(result.feedback, list)
    assert len(result.feedback) > 0