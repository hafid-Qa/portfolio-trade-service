from functools import lru_cache
from pathlib import Path

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: DirectoryPath = Path(__file__).parent.parent
    API_NAME: str = "Portfolio API"
    PROD: bool = False

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
