from datetime import datetime
from typing import Optional

import jwt
from auth_service.models import Session
from auth_service.repos import SessionRepo
from auth_service.settings import ApiSettings, get_api_settings
from commons.clients import UserServiceClient, get_user_service_client
from commons.dao import BaseDao
from commons.exceptions import ItemDoesNotExistsError
from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidSignatureError
from user_service.models import UserCreds


class AuthDao(BaseDao):
    def __init__(
        self,
        settings: ApiSettings = Depends(get_api_settings),
        user_service_client: UserServiceClient = Depends(get_user_service_client),
    ):
        super().__init__(settings=settings)
        self._session = SessionRepo.load_from_dict(self._load_data("session"))
        self._user_service_client = user_service_client

    def _get_file_path(self, _type: str) -> str:
        super()._get_file_path(_type)
        file_path_map = {
            "user_creds": "user_creds.json",
            "session": "session.json",
        }
        return file_path_map[_type]

    async def login(self, email: str, password: str, device_id: str) -> Optional[str]:
        try:
            user_creds_data = await self._user_service_client.get_user_creds(email)
        except HTTPException:
            return None
        user_creds = UserCreds.load_from_dict(**user_creds_data)
        if user_creds.is_valid(password=password):
            session = Session.create_item(
                user_id=user_creds.user_id, device_id=device_id
            )
            self._session.update_item(item=session)
            self._dump_data(_type="session")
            return session.generate_token()

    def authenticate(self, token: str, user_id: str, device_id: str) -> bool:
        try:
            session = self._session.get_item(user_id, device_id)
        except ItemDoesNotExistsError:
            return False
        try:
            payload = jwt.decode(token, session.secret, algorithms=["HS256"])
        except InvalidSignatureError:
            return False
        if payload.get("time_to_expiry", 0) > datetime.now().timestamp():
            if payload.get("device_id") == device_id:
                return True
        return False

    def logout(self, user_id: str, device_id: str):
        self._session.delete_item(user_id, device_id)
        self._dump_data("session")


def get_auth_dao(
    settings: ApiSettings = Depends(get_api_settings),
    user_service_client: UserServiceClient = Depends(get_user_service_client),
) -> AuthDao:
    return AuthDao(settings=settings, user_service_client=user_service_client)
