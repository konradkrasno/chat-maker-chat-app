import asyncio
import shutil
from pathlib import Path
from typing import Dict
from unittest.mock import MagicMock, patch

import pytest
from commons.clients import AuthServiceClient, UserServiceClient
from commons.settings import CommonSettings

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
def mock_auth_service_client() -> AuthServiceClient:
    client = MagicMock()
    client.authenticate = MagicMock(return_value=True)
    return client


@pytest.fixture(scope="session")
def user_creds() -> Dict:
    return {
        "user_id": "7d27972e74ef453aadf07fb441c7e619",
        "email": "john@doe.com",
        "password": "e649b8d4d47f7b5e9bbcb171c77010f17d4f85e26cbd2f2b3d109b931d1c69ec",
        "salt": "45c784",
    }


@pytest.fixture(scope="session")
def mock_user_service_client(user_creds) -> UserServiceClient:
    future = asyncio.Future()
    future.set_result(user_creds)

    client = MagicMock()
    client.get_user_creds = MagicMock(return_value=future)
    return client


@pytest.fixture(scope="session")
def mock_resolve_hostname() -> None:
    with patch(
        "user_service.api.endpoints.socket.gethostbyname", return_value="127.0.0.1"
    ):
        yield
