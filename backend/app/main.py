from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import router
from backend.app.api.runs import router as runs_router
from backend.app.api.evaluation import router as evaluation_router
from backend.app.config import settings


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Multi-Agent Research and Report Generation System",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
app.include_router(runs_router)
app.include_router(evaluation_router)


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