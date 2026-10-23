"""Environment-backed settings. Production must provide a unique strong secret."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    app_name: str = "CI × Nasara Risk Management Platform API"
    app_env: str = "development"
    database_url: str = "sqlite:///./risk_platform.db"
    secret_key: str = "development-only-change-me-before-deployment"
    access_token_minutes: int = 30
    cors_origins: str = "http://localhost:3000"
    stale_after_seconds: int = 60

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
