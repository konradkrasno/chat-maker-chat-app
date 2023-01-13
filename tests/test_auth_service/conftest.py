from typing import Dict

import pytest
from auth_service.dao import AuthDao, get_auth_dao
from auth_service.settings import ApiSettings, get_api_settings
from commons.settings import get_common_settings
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def auth_svc_settings(test_data_dir) -> ApiSettings:
    return ApiSettings(
        storage_type="files",
        auth_service_url="dummy",
        auth_service_port=5000,
        user_service_url="dummy",
        user_service_port=8080,
        chat_service_url="dummy",
        chat_service_port=8000,
        ws_service_url="dummy",
        ws_service_port=5050,
        data_dir=test_data_dir,
        allow_origins=["*"],
        cookie_expiration_time_in_minutes=5,
        encryption_secret_key="16bytessecretkey",
    )


@pytest.fixture(scope="session")
def auth_dao(auth_svc_settings, mock_user_service_client) -> AuthDao:
    return AuthDao(auth_svc_settings, user_service_client=mock_user_service_client)


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
        "/auth/login",
        data=login_request,
        cookies={"device_id": device_id},
    )
    assert response.status_code == 302
    assert "access_token" in response.cookies
    return response.cookies["access_token"]


@pytest.fixture(scope="function")
def auth_cookies(user_id, device_id, access_token) -> Dict:
    return {"user_id": user_id, "device_id": device_id, "access_token": access_token}
