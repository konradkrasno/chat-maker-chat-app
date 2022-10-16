import shutil
from pathlib import Path
from typing import Dict
from unittest.mock import patch

import pytest
from auth_service.dao import AuthDao, get_auth_dao
from auth_service.settings import ApiSettings, get_api_settings
from commons.clients import AuthServiceClient
from commons.settings import CommonSettings, get_common_settings
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
def fake_user_id() -> str:
    return "a1b2c3d4e5f6g7"


@pytest.fixture(scope="session")
def test_user_id() -> str:
    return "7d27972e74ef453aadf07fb441c7e619"


@pytest.fixture(scope="session")
def device_id() -> str:
    return "test-id"


@pytest.fixture(scope="session")
def common_settings(test_data_dir) -> CommonSettings:
    return CommonSettings(
        STORAGE_TYPE="files",
        AUTH_SERVICE_URL="fake",
        DATA_DIR=test_data_dir,
        ALLOW_ORIGINS=["*"],
    )


@pytest.fixture(scope="session")
def auth_svc_settings(test_data_dir) -> ApiSettings:
    return ApiSettings(
        STORAGE_TYPE="files",
        AUTH_SERVICE_URL="fake",
        DATA_DIR=test_data_dir,
        ALLOW_ORIGINS=["*"],
    )


@pytest.fixture(scope="session")
def auth_dao(auth_svc_settings) -> AuthDao:
    return AuthDao(auth_svc_settings)


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
        "/user/login", json=login_request, headers={"device_id": device_id}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]


@pytest.fixture(scope="session")
def auth_headers(device_id, access_token) -> Dict:
    return {"device_id": device_id, "authorization": access_token}


@pytest.fixture(scope="function")
def mock_authenticate() -> None:
    with patch.object(AuthServiceClient, "authenticate", return_value=True):
        yield
