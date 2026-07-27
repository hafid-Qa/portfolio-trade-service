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
        path = self.DATA_DIR / "stocks.yml"
        if not path.is_file():
            raise ValueError(f"Stocks file not found: {path}")
        return path

    @property
    def portfolio_path(self) -> Path:
        path = self.DATA_DIR / "portfolio.yml"
        if not path.is_file():
            raise ValueError(f"Portfolio file not found: {path}")
        return path

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
