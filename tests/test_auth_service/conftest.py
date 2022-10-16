from typing import Dict

import pytest
from auth_service.dao import AuthDao, get_auth_dao
from auth_service.settings import ApiSettings, get_api_settings
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def settings(test_data_dir) -> ApiSettings:
    return ApiSettings(
        STORAGE_TYPE="files",
        DATA_DIR=test_data_dir,
        ALLOW_ORIGINS=["*"],
    )


@pytest.fixture(scope="session")
def auth_dao(settings) -> AuthDao:
    return AuthDao(settings)


@pytest.fixture(scope="session")
def auth_service_client(settings, auth_dao) -> TestClient:
    from auth_service.app import create_app

    app = create_app(settings)
    app.dependency_overrides[get_api_settings] = lambda: settings
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
        "/user/login", json=login_request, headers={"device_id": device_id}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]


@pytest.fixture(scope="session")
def auth_headers(device_id, access_token) -> Dict:
    return {"device_id": device_id, "authorization": access_token}
