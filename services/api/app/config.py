"""Environment-backed settings. Production must provide a unique strong secret."""
from pydantic import model_validator
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

    @model_validator(mode="after")
    def require_production_secret(self):
        if self.app_env.lower() in {"production", "prod"} and (
            self.secret_key == "development-only-change-me-before-deployment" or len(self.secret_key) < 32
        ):
            raise ValueError("Production requires a unique SECRET_KEY of at least 32 characters")
        return self

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
