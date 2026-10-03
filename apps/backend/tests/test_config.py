from app.core.config import Settings


def test_settings_defaults():
    settings = Settings()
    assert settings.PROJECT_NAME == "AI-Powered Agentic Trip Planner"
    assert settings.API_V1_STR == "/api/v1"
    assert settings.GEMINI_MODEL_FAST == "gemini-2.5-flash"
    assert "postgresql://" in settings.DATABASE_URL
    assert "redis://" in settings.REDIS_URL
