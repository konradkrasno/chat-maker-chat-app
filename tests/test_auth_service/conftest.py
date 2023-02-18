from typing import Dict

import pytest
from auth_service.app import create_app
from auth_service.dao import AuthDao, get_auth_dao
from auth_service.settings import get_api_settings
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def auth_dao(auth_svc_settings, mock_user_service_client) -> AuthDao:
    return AuthDao(auth_svc_settings, user_service_client=mock_user_service_client)


@pytest.fixture(scope="function")
def auth_service_client(auth_svc_settings, auth_dao) -> TestClient:
    app = create_app(auth_svc_settings)
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


@pytest.fixture(scope="function")
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
