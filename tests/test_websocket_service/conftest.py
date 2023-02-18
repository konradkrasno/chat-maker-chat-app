import pytest
from commons.clients import get_auth_service_client, get_chat_service_client
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from websocket_service.app import create_app
from websocket_service.settings import WSSettings, get_ws_settings
from websocket_service.websocket.connection_manager import (
    ConnectionManager,
    get_connection_manager,
)


@pytest.fixture(scope="session")
def websocket_svc_settings(test_data_dir) -> WSSettings:
    return WSSettings(
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


@pytest.fixture(scope="function")
def connection_manager(mock_chat_service_client) -> ConnectionManager:
    return ConnectionManager(chat_service_client=mock_chat_service_client)


@pytest.fixture(scope="function")
def websocket_app(
    websocket_svc_settings,
    mock_auth_service_client,
    mock_chat_service_client,
    connection_manager,
) -> FastAPI:
    app = create_app()

    app.dependency_overrides[get_ws_settings] = lambda: websocket_svc_settings
    app.dependency_overrides[get_auth_service_client] = lambda: mock_auth_service_client
    app.dependency_overrides[get_chat_service_client] = lambda: mock_chat_service_client
    app.dependency_overrides[get_connection_manager] = lambda: connection_manager

    return app


@pytest.fixture(scope="function")
def websocket_1(websocket_app) -> WebSocket:
    client = TestClient(websocket_app)
    with client.websocket_connect(
        "/ws", cookies={"user_id": "test_user_1"}
    ) as websocket:
        yield websocket


@pytest.fixture(scope="function")
def websocket_2(websocket_app) -> WebSocket:
    client = TestClient(websocket_app)
    with client.websocket_connect(
        "/ws", cookies={"user_id": "test_user_2"}
    ) as websocket:
        yield websocket
