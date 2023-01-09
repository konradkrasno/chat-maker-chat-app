def test_authenticate_when_200(auth_service_client, user_id, auth_cookies):
    response = auth_service_client.post(f"/auth/authenticate", cookies=auth_cookies)
    assert response.status_code == 200
    assert response.json() == {"ok": "User successfully authenticated"}


def test_authenticate_when_401(auth_service_client, fake_user_id, auth_cookies):
    auth_cookies["access_token"] = "fake"
    response = auth_service_client.post(f"/auth/authenticate", cookies=auth_cookies)
    assert response.status_code == 401
    assert response.json() == {"detail": "Token invalid or expired"}
