from typing import Dict

import pytest
from auth_service.dao import AuthDao, get_auth_dao
from auth_service.settings import ApiSettings, get_api_settings
from commons.settings import get_common_settings
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def auth_svc_settings(test_data_dir) -> ApiSettings:
    return ApiSettings(
        STORAGE_TYPE="files",
        AUTH_SERVICE_URL="dummy",
        AUTH_SERVICE_PORT=5000,
        USER_SERVICE_URL="dummy",
        USER_SERVICE_PORT=8080,
        CHAT_SERVICE_URL="dummy",
        CHAT_SERVICE_PORT=8000,
        DATA_DIR=test_data_dir,
        ALLOW_ORIGINS=["*"],
    )


@pytest.fixture(scope="session")
def auth_dao(auth_svc_settings, user_service_client_mock) -> AuthDao:
    return AuthDao(auth_svc_settings, user_service_client=user_service_client_mock)


@pytest.fixture(scope="session")
def auth_service_client(common_settings, auth_svc_settings, auth_dao) -> TestClient:
    from auth_service.app import create_app

    app = create_app(auth_svc_settings)
    app.dependency_overrides[get_common_settings] = lambda: common_settings
    app.dependency_overrides[get_api_settings] = lambda: auth_svc_settings
    app.dependency_overrides[get_auth_dao] = lambda: auth_dao

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def login_request() -> Dict:
    return {
        "email": "john@doe.com",
        "password": "secretpassword",
    }


@pytest.fixture(scope="session")
def access_token(auth_service_client, login_request, device_id) -> str:
    response = auth_service_client.post(
        "/auth/login", json=login_request, headers={"device_id": device_id}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]


@pytest.fixture(scope="session")
def auth_headers(device_id, access_token) -> Dict:
    return {"device_id": device_id, "authorization": access_token}
