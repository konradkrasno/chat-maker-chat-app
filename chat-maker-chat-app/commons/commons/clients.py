import requests
from commons.settings import CommonSettings, get_common_settings
from fastapi import Depends, Request
from starlette.datastructures import Headers


class AuthServiceClient:
    def __init__(self, request: Request, service_url: str):
        self._service_url = service_url
        self._headers: Headers = request.headers

    def _get_url(self, path) -> str:
        return f"{self._service_url}{path}"

    def authenticate(self, user_id) -> bool:
        response = requests.post(
            self._get_url(f"/user/authenticate/{user_id}"), headers=self._headers
        )
        if response.status_code == 200:
            return True
        return False


def get_auth_service_client(
    request: Request,
    settings: CommonSettings = Depends(get_common_settings),
):
    return AuthServiceClient(request=request, service_url=settings.AUTH_SERVICE_URL)
