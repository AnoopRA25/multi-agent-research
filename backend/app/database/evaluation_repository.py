from backend.app.database.database import get_connection


def create_evaluation(
    run_id: int,
    relevance_score: float,
    completeness_score: float,
    evidence_score: float,
    factuality_score: float,
    overall_score: float,
    feedback: str,
) -> int:
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO evaluations
            (
                run_id,
                relevance_score,
                completeness_score,
                evidence_score,
                factuality_score,
                overall_score,
                feedback
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                relevance_score,
                completeness_score,
                evidence_score,
                factuality_score,
                overall_score,
                feedback,
            ),
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


def get_evaluation(run_id: int) -> dict | None:
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                id,
                run_id,
                relevance_score,
                completeness_score,
                evidence_score,
                factuality_score,
                overall_score,
                feedback,
                created_at
            FROM evaluations
            WHERE run_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (run_id,),
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()

def get_evaluation_summary() -> dict:
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total_evaluations,
                ROUND(AVG(relevance_score), 2) AS avg_relevance,
                ROUND(AVG(completeness_score), 2) AS avg_completeness,
                ROUND(AVG(evidence_score), 2) AS avg_evidence,
                ROUND(AVG(factuality_score), 2) AS avg_factuality,
                ROUND(AVG(overall_score), 2) AS avg_overall
            FROM evaluations
            """
        ).fetchone()

        return dict(row)

    finally:
        connection.close()