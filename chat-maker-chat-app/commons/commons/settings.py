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

    ws_service_url: str
    ws_service_port: int

    data_dir: Path = BASE_DIR.parent.parent / "data"
    allow_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]


def get_common_settings() -> CommonSettings:
    return CommonSettings()
