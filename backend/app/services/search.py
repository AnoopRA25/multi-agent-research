from ddgs import DDGS

from backend.app.config import settings


def web_search(query: str) -> list[dict]:
    results = DDGS().text(
        query,
        max_results=settings.max_search_results,
    )

    return [
        {
            "title": result.get("title", ""),
            "url": result.get("href", ""),
            "snippet": result.get("body", ""),
        }
        for result in results
    ]