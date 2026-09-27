from backend.app.database.database import get_connection


def create_research_sources(
    run_id: int,
    sources: list[dict],
) -> None:
    connection = get_connection()

    try:
        connection.executemany(
            """
            INSERT INTO research_sources
            (run_id, title, url, snippet)
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    run_id,
                    source["title"],
                    source["url"],
                    source.get("snippet", ""),
                )
                for source in sources
            ],
        )

        connection.commit()

    finally:
        connection.close()


def list_research_sources(
    run_id: int,
) -> list[dict]:
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                run_id,
                title,
                url,
                snippet,
                created_at
            FROM research_sources
            WHERE run_id = ?
            ORDER BY id ASC
            """,
            (run_id,),
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()