from pathlib import Path
from typing import List

import pytest
from chat_app.dao import ChatDao
from pydantic import BaseSettings

BASE_DIR: Path = Path(__name__).resolve().parent


class ApiSettings(BaseSettings):
    STORAGE_TYPE: str = "files"
    DATA_DIR: Path = BASE_DIR / "data"
    ALLOW_ORIGINS: List[str] = ["*"]


@pytest.fixture(scope="session")
def settings() -> ApiSettings:
    return ApiSettings()


@pytest.fixture(scope="session")
def dao(settings):
    return ChatDao(settings)
