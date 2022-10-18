from unittest.mock import patch
from uuid import UUID


def test_sign_in(user_service_client, sign_in_request, fake_user_id):
    with patch.object(UUID, "hex", fake_user_id):
        response = user_service_client.post("/user/sign-in", json=sign_in_request)
    assert response.status_code == 200
    assert response.json() == {"user_id": fake_user_id}


def test_sign_in_when_user_exists(user_service_client, sign_in_request, fake_user_id):
    sign_in_request["email"] = "john@doe.com"
    with patch.object(UUID, "hex", fake_user_id):
        response = user_service_client.post("/user/sign-in", json=sign_in_request)
    assert response.status_code == 400
    assert response.json() == {
        "error": f"detail: User with key: '{fake_user_id}' already exists"
    }


def test_get_user_creds_when_host_not_allowed(user_service_client):
    response = user_service_client.post("/user/creds", json={"email": "john@doe.com"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "IP testclient is not allowed to access this resource."
    }
