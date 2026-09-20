from google import genai

from backend.app.config import settings


client = genai.Client(api_key=settings.gemini_api_key)


def generate_answer(prompt: str) -> str:
    response = client.models.generate_content(
        model=settings.llm_model,
        contents=prompt,
    )

    return response.text or ""