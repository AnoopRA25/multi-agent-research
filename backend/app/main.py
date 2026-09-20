from fastapi import FastAPI

from backend.app.api.routes import router
from backend.app.api.runs import router as runs_router
from backend.app.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Multi-Agent Research and Report Generation System",
)

app.include_router(router)
app.include_router(runs_router)


@app.get("/")
def root():
    return {
        "project": settings.app_name,
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "environment": settings.app_env,
        "llm": {
            "provider": "Google Gemini",
            "model": settings.llm_model,
            "configured": bool(settings.gemini_api_key),
        },
    }