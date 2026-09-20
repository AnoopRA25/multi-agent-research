from backend.app.services.llm import generate_answer


def create_plan(query: str) -> list[str]:
    prompt = f"""
You are a research planning agent.

User research question:
{query}

Create a research plan for answering this question.

Return exactly 3 focused research questions.
Each question should:
- help answer the user's original question
- be specific and useful for web research
- avoid unnecessary repetition

Return only the 3 questions, one per line.
Do not add numbering, bullets, explanations, or other text.
"""

    response = generate_answer(prompt)

    questions = [
        line.strip()
        for line in response.text.splitlines()
        if line.strip()
    ]

    return questions[:3]