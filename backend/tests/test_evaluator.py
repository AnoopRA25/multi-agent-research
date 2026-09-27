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

def test_factuality_score_rewards_uncertainty():
    result = evaluate_report(
        question="What are the major applications of generative AI?",
        report="""
        Generative AI has applications in software development and education.
        Available evidence has limitations and uncertainty.
        Results may vary depending on the available data and study.
        """,
        criteria=[
            "major applications",
            "supporting evidence",
            "uncertainty",
            "limitations",
        ],
    )

    assert result.factuality_score >= 7.5


def test_factuality_score_is_lower_without_limitations():
    result = evaluate_report(
        question="What are the major applications of generative AI?",
        report="""
        Generative AI is used in software development.
        It is used in education.
        It is used in content generation.
        """,
        criteria=[
            "major applications",
            "supporting evidence",
            "uncertainty",
            "limitations",
        ],
    )

    assert result.factuality_score < 7.5


def test_relevance_uses_question_coverage():
    result = evaluate_report(
        question="What are the major applications of generative AI?",
        report="""
        Generative AI has major applications in software development,
        education, content generation, and healthcare.
        """,
        criteria=["major applications"],
    )

    assert result.relevance_score >= 5.0