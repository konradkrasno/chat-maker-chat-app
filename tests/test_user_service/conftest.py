from typing import Dict

import pytest
from commons.settings import get_common_settings
from fastapi.testclient import TestClient
from user_service.dao import UserDao, get_user_dao
from user_service.settings import ApiSettings, get_api_settings


@pytest.fixture(scope="session")
def user_svc_settings(test_data_dir, auth_service_client) -> ApiSettings:
    return ApiSettings(
        STORAGE_TYPE="files",
        AUTH_SERVICE_URL="fake",
        DATA_DIR=test_data_dir,
        ALLOW_ORIGINS=["*"],
    )


@pytest.fixture(scope="session")
def user_dao(user_svc_settings) -> UserDao:
    return UserDao(user_svc_settings)


@pytest.fixture(scope="session")
def user_service_client(common_settings, user_svc_settings, user_dao) -> TestClient:
    from user_service.app import create_app

    app = create_app(user_svc_settings)
    app.dependency_overrides[get_common_settings] = lambda: common_settings
    app.dependency_overrides[get_api_settings] = lambda: user_svc_settings
    app.dependency_overrides[get_user_dao] = lambda: user_dao

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def sign_in_request() -> Dict:
    return {
        "name": "John",
        "surname": "Doe",
        "email": "another@johndoe.com",
        "password": "secretpassword",
    }
