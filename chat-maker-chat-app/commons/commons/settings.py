from pathlib import Path
from typing import List

from pydantic import BaseSettings

BASE_DIR: Path = Path(__name__).resolve().parent


class CommonSettings(BaseSettings):
    storage_type: str

    auth_service_url: str
    auth_service_port: int

    user_service_url: str
    user_service_port: int

    chat_service_url: str
    chat_service_port: int

    data_dir: Path = BASE_DIR.parent.parent / "data"
    allow_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost",
        "http://chat-maker-frontend",
        "http://localhost:30470",
    ]


def get_common_settings() -> CommonSettings:
    return CommonSettings()
