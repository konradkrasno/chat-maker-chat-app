import shutil
from pathlib import Path
from typing import Dict

import pytest
from chat_service.dao import ChatDao, UserDao, get_chat_dao, get_user_dao
from chat_service.settings import ApiSettings, get_api_settings
from fastapi.testclient import TestClient

BASE_DIR: Path = Path(__name__).resolve().parent
DATA_DIR = BASE_DIR / "data"


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    test_data_dir = BASE_DIR / "test_data"
    shutil.copytree(DATA_DIR, test_data_dir)
    yield test_data_dir
    shutil.rmtree(test_data_dir)


@pytest.fixture(scope="session")
def settings(test_data_dir) -> ApiSettings:
    return ApiSettings(
        STORAGE_TYPE="files",
        DATA_DIR=test_data_dir,
        ALLOW_ORIGINS=["*"],
    )


@pytest.fixture(scope="session")
def user_dao(settings) -> UserDao:
    return UserDao(settings)


@pytest.fixture(scope="session")
def chat_dao(settings) -> ChatDao:
    return ChatDao(settings)


@pytest.fixture(scope="session")
def app_client(settings, chat_dao, user_dao) -> TestClient:
    from chat_service.app import create_app

    app = create_app(settings)
    app.dependency_overrides[get_api_settings] = lambda: settings
    app.dependency_overrides[get_chat_dao] = lambda: chat_dao
    app.dependency_overrides[get_user_dao] = lambda: user_dao

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def sign_in_response() -> Dict:
    return {
        "name": "John",
        "surname": "Doe",
        "email": "john@doe.com",
        "password": "secretpassword",
    }
