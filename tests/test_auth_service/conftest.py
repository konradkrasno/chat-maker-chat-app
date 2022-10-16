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
