from functools import lru_cache
from pathlib import Path

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_NAME: str = "Portfolio API"
    PROD: bool = False

    DATA_DIR: DirectoryPath = Path("/data")

    @property
    def stock_path(self) -> Path:
        return self.DATA_DIR / "stocks.yml"

    @property
    def portfolio_path(self) -> Path:
        return self.DATA_DIR / "portfolio.yml"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
