from pathlib import Path
from typing import List

from pydantic import BaseSettings

BASE_DIR: Path = Path(__name__).resolve().parent


class ApiSettings(BaseSettings):
    STORAGE_TYPE: str
    DATA_DIR: Path = BASE_DIR.parent.parent / "data"
    ALLOW_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost",
        "http://chat-maker-frontend",
        "http://localhost:30470",
    ]


def get_api_settings() -> ApiSettings:
    return ApiSettings()
