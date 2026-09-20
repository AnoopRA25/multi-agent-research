from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multi-Agent Research System"
    app_env: str = "development"
    debug: bool = True

    gemini_api_key: str
    llm_model: str = "gemini-3.8-flash"

    max_search_results: int = 5

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()