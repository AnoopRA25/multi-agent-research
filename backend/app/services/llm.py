from google import genai
from google.genai import errors

from backend.app.config import settings


client = genai.Client(api_key=settings.gemini_api_key)


def generate_answer(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=settings.llm_model,
            contents=prompt,
        )

        return response.text or ""

    except errors.ClientError as exc:
        if exc.code == 429:
            raise RuntimeError(
                "Gemini API quota has been exceeded. "
                "Please wait for the quota to reset or check your Gemini API usage."
            ) from exc

        raise RuntimeError(
            f"Gemini API request failed: {exc}"
        ) from exc