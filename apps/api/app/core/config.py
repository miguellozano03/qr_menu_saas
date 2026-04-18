import os
from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env.dev") if os.getenv("ENVIRONMENT") != "production" else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )

    environment: str = "development"

    # -- General -- #
    app_name: str = "Menu QR API"
    secret_key: str = "insecure-secret-key"
    
    # -- CORS -- #
    allowed_origins: list[str] = []

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, value):
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        return value

    # --- Database --- #
    db_url: str

    # --- Cloudflare R2 --- #
    r2_bucket_name: str = ""
    r2_endpoint_url: str = ""
    r2_public_url: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""

    # --- JWT --- #
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    algorithm: str = "HS256"


settings = Settings()  # pyright: ignore[reportCallIssue]