def test_authenticate_when_200(auth_service_client, test_user_id, auth_headers):
    response = auth_service_client.post(
        f"/user/authenticate/{test_user_id}", headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json() == {"ok": "User successfully authenticated"}
