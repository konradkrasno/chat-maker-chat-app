from typing import Dict

import pytest

from user_service.dao import UserDao, get_user_dao
from user_service.settings import ApiSettings, get_api_settings
from fastapi.testclient import TestClient


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
def user_service_client(settings, user_dao) -> TestClient:
    from user_service.app import create_app

    app = create_app(settings)
    app.dependency_overrides[get_api_settings] = lambda: settings
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
