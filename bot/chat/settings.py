import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    HOST = os.environ.get("HOST", "127.0.0.1")
    TITLE: str = os.environ.get("TITLE", "AI-bot")
    DEBUG: bool = bool(os.environ.get("DEBUG", True))
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite+aiosqlite://")
    DATABASE_ECHO: bool = bool(os.environ.get("DATABASE_ECHO", True))
    VERSION: str = os.environ.get("VERSION", "0.0.1")
    JWT_KEY: str | None = os.environ.get("JWT_KEY")

    class Config:
        env_file_encoding = "utf-8"


settings = Settings()
