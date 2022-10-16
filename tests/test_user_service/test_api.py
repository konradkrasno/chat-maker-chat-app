from unittest.mock import patch
from uuid import UUID

import pytest


@pytest.mark.dependency()
@patch.object(UUID, "hex", "a1b2c3d4e5f6")
def test_sign_in(user_service_client, sign_in_response):
    response = user_service_client.post("/user/sign-in", json=sign_in_response)
    assert response.status_code == 200
    assert response.json() == {"user_id": "a1b2c3d4e5f6"}


@pytest.mark.dependency(depends=["test_sign_in"])
@patch.object(UUID, "hex", "a1b2c3d4e5f6g7")
def test_sign_in_when_user_exists(user_service_client, sign_in_response):
    response = user_service_client.post("/user/sign-in", json=sign_in_response)
    assert response.status_code == 400
    assert response.json() == {
        "error": f"detail: UserCreds with key: '{sign_in_response['email']}' already exists"
    }
