from typing import Dict

import pytest
from commons.clients import get_auth_service_client
from fastapi.testclient import TestClient
from user_service.app import create_app
from user_service.dao import UserDao, get_user_dao
from user_service.settings import get_api_settings


@pytest.fixture(scope="session")
def user_dao(user_svc_settings) -> UserDao:
    return UserDao(user_svc_settings)


@pytest.fixture(scope="function")
def user_service_client(
    user_svc_settings,
    user_dao,
    mock_auth_service_client,
    mock_resolve_hostname,
) -> TestClient:
    app = create_app(user_svc_settings)
    app.dependency_overrides[get_api_settings] = lambda: user_svc_settings
    app.dependency_overrides[get_user_dao] = lambda: user_dao
    app.dependency_overrides[get_auth_service_client] = lambda: mock_auth_service_client

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def sign_in_request() -> Dict:
    return {
        "name": "John",
        "surname": "Doe",
        "email": "another@johndoe.com",
        "password": "secretpassword",
    }
