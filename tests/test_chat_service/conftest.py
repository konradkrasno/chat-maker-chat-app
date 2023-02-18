import pytest
from chat_service.app import create_app
from chat_service.dao import ChatDao, get_chat_dao
from chat_service.settings import get_api_settings
from commons.clients import get_auth_service_client
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def chat_dao(user_id, chat_svc_settings, mock_user_service_client) -> ChatDao:
    return ChatDao(
        user_id, chat_svc_settings, user_service_client=mock_user_service_client
    )


@pytest.fixture(scope="function")
def chat_service_client(
    chat_svc_settings, chat_dao, mock_auth_service_client
) -> TestClient:
    app = create_app(chat_svc_settings)
    app.dependency_overrides[get_api_settings] = lambda: chat_svc_settings
    app.dependency_overrides[get_chat_dao] = lambda: chat_dao
    app.dependency_overrides[get_auth_service_client] = lambda: mock_auth_service_client

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def chat_id() -> str:
    return "a37259242eeb40bda35c41be4172a32f"
