from typing import Dict, List

import requests
from chat_service.models import Message
from commons.models import AuthCookies, get_auth_cookies
from commons.settings import CommonSettings, get_common_settings
from fastapi import Depends, HTTPException


class BaseClient:
    def __init__(self, service_url: str, service_port: int, auth_cookies: AuthCookies):
        self._service_url: str = service_url
        self._service_port: int = service_port
        self._auth_cookies: AuthCookies = auth_cookies

    @property
    def auth_cookies(self) -> Dict:
        return self._auth_cookies.dict()

    def _get_url(self, path) -> str:
        return f"http://{self._service_url}:{self._service_port}{path}"


class AuthServiceClient(BaseClient):
    def __init__(self, service_url: str, service_port: int, auth_cookies: AuthCookies):
        super().__init__(service_url, service_port, auth_cookies)

    def authenticate(self) -> bool:
        response = requests.post(
            self._get_url("/auth/authenticate"), cookies=self.auth_cookies
        )
        if response.status_code == 200:
            return True
        return False


class UserServiceClient(BaseClient):
    def __init__(self, service_url: str, service_port: int, auth_cookies: AuthCookies):
        super().__init__(service_url, service_port, auth_cookies)

    async def get_users_by_ids(self, query_ids: List[str]) -> List[Dict]:
        response = requests.post(
            self._get_url("/user/query"),
            cookies=self.auth_cookies,
            json={"user_ids": query_ids},
        )
        if response.status_code == 200:
            return response.json()["users"]
        raise HTTPException(status_code=response.status_code, detail=response.text)

    async def get_user_by_id(self, user_id: str) -> Dict:
        response = requests.post(
            self._get_url(f"/user/id/{user_id}"),
            cookies=self.auth_cookies,
        )
        if response.status_code == 200:
            return response.json()["user"]
        raise HTTPException(status_code=response.status_code, detail=response.text)

    async def sign_in(self, request_body: Dict) -> None:
        pass

    async def get_user_creds(self, email: str) -> Dict:
        response = requests.post(self._get_url("/user/creds"), json={"email": email})
        if response.status_code == 200:
            return response.json()["user_creds"]
        raise HTTPException(status_code=response.status_code, detail=response.text)


class ChatServiceClient(BaseClient):
    def __init__(self, service_url: str, service_port: int, auth_cookies: AuthCookies):
        super().__init__(service_url, service_port, auth_cookies)

    async def put_message(self, chat_id: str, message: Message) -> None:
        pass


def get_auth_service_client(
    auth_cookies: AuthCookies = Depends(get_auth_cookies),
    settings: CommonSettings = Depends(get_common_settings),
) -> AuthServiceClient:
    return AuthServiceClient(
        service_url=settings.auth_service_url,
        service_port=settings.auth_service_port,
        auth_cookies=auth_cookies,
    )


def get_user_service_client(
    auth_cookies: AuthCookies = Depends(get_auth_cookies),
    settings: CommonSettings = Depends(get_common_settings),
) -> UserServiceClient:
    return UserServiceClient(
        service_url=settings.user_service_url,
        service_port=settings.user_service_port,
        auth_cookies=auth_cookies,
    )


def get_chat_service_client(
    auth_cookies: AuthCookies = Depends(get_auth_cookies),
    settings: CommonSettings = Depends(get_common_settings),
) -> ChatServiceClient:
    return ChatServiceClient(
        service_url=settings.chat_service_url,
        service_port=settings.chat_service_port,
        auth_cookies=auth_cookies,
    )
