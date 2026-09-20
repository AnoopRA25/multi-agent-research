from backend.app.services.llm import generate_answer


def research(query: str) -> str:
    prompt = f"""
You are a research assistant.

User research question:
{query}

Provide a concise, factual answer.

Structure your answer with:
1. Key findings
2. Important details
3. Limitations or uncertainty

Do not invent sources or facts.
"""

    return generate_answer(prompt)