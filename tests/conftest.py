import pytest
from chat_app.dao import Dao


@pytest.fixture(scope="session")
def dao():
    return Dao("files")
