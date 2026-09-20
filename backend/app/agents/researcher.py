from backend.app.services.llm import generate_answer
from backend.app.services.search import web_search


def research(query: str) -> tuple[str, list[dict]]:
    search_results = web_search(query)

    context = "\n\n".join(
        [
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Snippet: {result['snippet']}"
            for result in search_results
        ]
    )

    prompt = f"""
You are a research assistant.

User research question:
{query}

Use the web search results below to answer the question.

WEB SEARCH RESULTS:
{context}

Instructions:
1. Base your answer primarily on the provided search results.
2. Do not invent facts or sources.
3. Clearly explain the key findings.
4. Mention uncertainty when the search results are insufficient.
5. Do not include a separate Sources section because the API will return the source URLs separately.

Provide a concise but useful answer.
"""

    answer = generate_answer(prompt)

    sources = [
        {
            "title": result["title"],
            "url": result["url"],
            "snippet": result["snippet"],
        }
        for result in search_results
    ]

    return answer, sources