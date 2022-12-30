from typing import Dict, List

import requests
from fastapi import Depends, HTTPException, Request
from starlette.datastructures import Headers

from commons.settings import CommonSettings, get_common_settings


class BaseClient:
    def __init__(self, request: Request, service_url: str, service_port: int):
        self._service_url = service_url
        self._service_port = service_port
        self._headers: Headers = request.headers

    def _get_url(self, path) -> str:
        return f"http://{self._service_url}:{self._service_port}{path}"


class AuthServiceClient(BaseClient):
    def __init__(self, request: Request, service_url: str, service_port: int):
        super().__init__(request, service_url, service_port)

    def authenticate(self, user_id) -> bool:
        response = requests.post(
            self._get_url(f"/auth/authenticate/{user_id}"), headers=self._headers
        )
        if response.status_code == 200:
            return True
        return False


class UserServiceClient(BaseClient):
    def __init__(self, request: Request, service_url: str, service_port: int):
        super().__init__(request, service_url, service_port)

    async def get_users_by_ids(self, user_id: str, query_ids: List[str]) -> List[Dict]:
        response = requests.post(
            self._get_url(f"/user/query/{user_id}"),
            headers=self._headers,
            json={"user_ids": query_ids},
        )
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

    async def sign_in(self, request_body: Dict) -> None:
        pass

    async def get_user_creds(self, email: str) -> Dict:
        response = requests.post(self._get_url(f"/user/creds"), json={"email": email})
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)


def get_auth_service_client(
    request: Request,
    settings: CommonSettings = Depends(get_common_settings),
):
    return AuthServiceClient(
        request=request,
        service_url=settings.auth_service_url,
        service_port=settings.auth_service_port,
    )


def get_user_service_client(
    request: Request, settings: CommonSettings = Depends(get_common_settings)
):
    return UserServiceClient(
        request=request,
        service_url=settings.user_service_url,
        service_port=settings.user_service_port,
    )
