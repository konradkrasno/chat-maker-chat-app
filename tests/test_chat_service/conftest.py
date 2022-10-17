import pytest
from chat_service.dao import ChatDao, get_chat_dao
from chat_service.settings import ApiSettings, get_api_settings
from commons.clients import get_auth_service_client
from commons.settings import get_common_settings
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def chat_svc_settings(test_data_dir) -> ApiSettings:
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
def chat_dao(chat_svc_settings, user_service_client_mock) -> ChatDao:
    return ChatDao(chat_svc_settings, user_service_client=user_service_client_mock)


@pytest.fixture(scope="session")
def chat_service_client(
    common_settings, chat_svc_settings, chat_dao, auth_service_client_mock
) -> TestClient:
    from chat_service.app import create_app

    app = create_app(chat_svc_settings)
    app.dependency_overrides[get_common_settings] = lambda: common_settings
    app.dependency_overrides[get_api_settings] = lambda: chat_svc_settings
    app.dependency_overrides[get_chat_dao] = lambda: chat_dao
    app.dependency_overrides[get_auth_service_client] = lambda: auth_service_client_mock

    with TestClient(app) as client:
        yield client
