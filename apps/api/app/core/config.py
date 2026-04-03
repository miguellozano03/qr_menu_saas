import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env.dev"), env_file_encoding='utf-8', extra="ignore")

    # -- General -- #
    app_name: str = "Menu QR API"
    secret_key: str = "insecure-secret-key"

    #--- Database --- 
    db_motor: str = "postgresql"
    db_driver_async: str = "asyncpg"
    db_driver_sync: str = "psycopg2"
    
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    # --- JWT --- 
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    algorithm: str = "HS256"

    def _build_url(self, driver: str) -> str:
        "Makes a database url template."
        return str(URL.create(
            drivername=f'{self.db_motor}+{driver}',
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name
        ))
    
    @property
    def db_url_async(self) -> str:
        "Get an async database url"
        return self._build_url(self.db_driver_async)
    
    @property
    def db_url_sync(self) -> str:
        "Get a sync database url"
        return self._build_url(self.db_driver_sync)
    

settings = Settings() # pyright: ignore[reportCallIssue]