import pytest
from chat_service.dao import ChatDao, get_chat_dao
from chat_service.settings import ApiSettings, get_api_settings
from commons.settings import get_common_settings
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def chat_svc_settings(test_data_dir) -> ApiSettings:
    return ApiSettings(
        STORAGE_TYPE="files",
        AUTH_SERVICE_URL="fake",
        DATA_DIR=test_data_dir,
        ALLOW_ORIGINS=["*"],
    )


@pytest.fixture(scope="session")
def chat_dao(chat_svc_settings) -> ChatDao:
    return ChatDao(chat_svc_settings)


@pytest.fixture(scope="session")
def chat_service_client(common_settings, chat_svc_settings, chat_dao) -> TestClient:
    from chat_service.app import create_app

    app = create_app(chat_svc_settings)
    app.dependency_overrides[get_common_settings] = lambda: common_settings
    app.dependency_overrides[get_api_settings] = lambda: chat_svc_settings
    app.dependency_overrides[get_chat_dao] = lambda: chat_dao

    with TestClient(app) as client:
        yield client
