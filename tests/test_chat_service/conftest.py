import pytest

from chat_service.dao import ChatDao, get_chat_dao
from chat_service.settings import ApiSettings, get_api_settings
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def settings(test_data_dir) -> ApiSettings:
    return ApiSettings(
        STORAGE_TYPE="files",
        DATA_DIR=test_data_dir,
        ALLOW_ORIGINS=["*"],
    )


@pytest.fixture(scope="session")
def chat_dao(settings) -> ChatDao:
    return ChatDao(settings)


@pytest.fixture(scope="session")
def chat_service_client(settings, chat_dao) -> TestClient:
    from chat_service.app import create_app

    app = create_app(settings)
    app.dependency_overrides[get_api_settings] = lambda: settings
    app.dependency_overrides[get_chat_dao] = lambda: chat_dao

    with TestClient(app) as client:
        yield client
