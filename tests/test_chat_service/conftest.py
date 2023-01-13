import pytest
from chat_service.dao import ChatDao, get_chat_dao
from chat_service.settings import ApiSettings, get_api_settings
from commons.clients import get_auth_service_client
from commons.settings import get_common_settings
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def chat_svc_settings(test_data_dir) -> ApiSettings:
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
    )


@pytest.fixture(scope="session")
def chat_dao(user_id, chat_svc_settings, mock_user_service_client) -> ChatDao:
    return ChatDao(
        user_id, chat_svc_settings, user_service_client=mock_user_service_client
    )


@pytest.fixture(scope="session")
def chat_service_client(
    common_settings, chat_svc_settings, chat_dao, mock_auth_service_client
) -> TestClient:
    from chat_service.app import create_app

    app = create_app(chat_svc_settings)
    app.dependency_overrides[get_common_settings] = lambda: common_settings
    app.dependency_overrides[get_api_settings] = lambda: chat_svc_settings
    app.dependency_overrides[get_chat_dao] = lambda: chat_dao
    app.dependency_overrides[get_auth_service_client] = lambda: mock_auth_service_client

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def chat_id() -> str:
    return "a37259242eeb40bda35c41be4172a32f"
