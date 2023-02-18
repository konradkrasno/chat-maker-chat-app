import asyncio
import shutil
from pathlib import Path
from typing import Dict
from unittest.mock import MagicMock, patch

import pytest
from auth_service.settings import ApiSettings as AuthServiceSettings
from chat_service.settings import ApiSettings as ChatServiceSettings
from commons.clients import AuthServiceClient, ChatServiceClient, UserServiceClient
from commons.settings import CommonSettings
from user_service.settings import ApiSettings as UserServiceSettings

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
def user_id() -> str:
    return "7d27972e74ef453aadf07fb441c7e619"


@pytest.fixture(scope="session")
def device_id() -> str:
    return "test-id"


@pytest.fixture(scope="session")
def common_settings(test_data_dir) -> CommonSettings:
    return CommonSettings(
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
def auth_svc_settings(test_data_dir) -> AuthServiceSettings:
    return AuthServiceSettings(
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
        cookie_expiration_time_in_minutes=5,
        encryption_secret_key="16bytessecretkey",
    )


@pytest.fixture(scope="session")
def chat_svc_settings(test_data_dir) -> ChatServiceSettings:
    return ChatServiceSettings(
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
def user_svc_settings(test_data_dir) -> UserServiceSettings:
    return UserServiceSettings(
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
def mock_auth_service_client() -> AuthServiceClient:
    client = MagicMock()
    client.authenticate.return_value = True
    return client


@pytest.fixture(scope="session")
def user_data(user_id) -> Dict:
    return {
        "id": user_id,
        "avatarSource": "test",
        "name": "John",
        "surname": "Doe",
        "active": True,
        "status": " ",
        "lastSeen": "online",
    }


@pytest.fixture(scope="session")
def user_creds() -> Dict:
    return {
        "user_id": "7d27972e74ef453aadf07fb441c7e619",
        "email": "john@doe.com",
        "password": "e649b8d4d47f7b5e9bbcb171c77010f17d4f85e26cbd2f2b3d109b931d1c69ec",
        "salt": "45c784",
    }


@pytest.fixture(scope="function")
def mock_user_service_client(user_creds, user_data) -> UserServiceClient:
    user_creds_future = asyncio.Future()
    user_creds_future.set_result(user_creds)
    user_future = asyncio.Future()
    user_future.set_result(user_data)

    client = MagicMock()
    client.get_user_creds.return_value = user_creds_future
    client.get_user_by_id.return_value = user_future
    return client


@pytest.fixture(scope="function")
def mock_chat_service_client() -> ChatServiceClient:
    chat_members_future = asyncio.Future()
    chat_members_future.set_result(["test_user_1", "test_user_2", "test_user_3"])

    put_message_future = asyncio.Future()
    put_message_future.set_result(None)

    client = MagicMock()
    client.get_chat_members.return_value = chat_members_future
    client.put_message.return_value = put_message_future
    return client


@pytest.fixture(scope="session")
def mock_resolve_hostname() -> None:
    with patch(
        "user_service.api.endpoints.socket.gethostbyname", return_value="127.0.0.1"
    ):
        yield
