import shutil
from pathlib import Path

import pytest
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
        AUTH_SERVICE_URL="fake",
        DATA_DIR=test_data_dir,
        ALLOW_ORIGINS=["*"],
    )
