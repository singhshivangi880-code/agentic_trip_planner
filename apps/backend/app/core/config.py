from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered Agentic Trip Planner"
    API_V1_STR: str = "/api/v1"
    
    GCP_PROJECT_ID: str = ""
    GCP_REGION: str = "us-central1"
    
    GEMINI_MODEL_FAST: str = "gemini-2.5-flash"
    GEMINI_MODEL_REASONING: str = "gemini-2.5-pro"
    GEMINI_EMBEDDING_MODEL: str = "text-embedding-004"
    
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost:5432/tripplanner"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    OTEL_ENDPOINT: str = "http://localhost:4317"
    
    MAPS_API_KEY: str = ""
    WEATHER_API_KEY: str = ""
    SEARCH_API_KEY: str = ""
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
