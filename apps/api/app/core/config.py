import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env.dev"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    environment: str = "development"

    # -- General -- #
    app_name: str = "Menu QR API"
    secret_key: str = "insecure-secret-key"

    # --- Database --- #
    db_url: str  # ← Neon / prod / local

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