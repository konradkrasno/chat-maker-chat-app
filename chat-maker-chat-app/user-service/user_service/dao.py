from typing import Dict, List
from uuid import uuid4

from commons.dao import BaseDao
from fastapi import Depends
from user_service.models import User, UserCreds
from user_service.repos import UserCredsRepo, UserRepo
from user_service.settings import ApiSettings, get_api_settings


class UserDao(BaseDao):
    def __init__(self, settings: ApiSettings = Depends(get_api_settings)):
        super().__init__(settings=settings)
        self._users = UserRepo.load_from_dict(self._load_data("users"))
        self._user_creds = UserCredsRepo.load_from_dict(self._load_data("user_creds"))

    def _get_file_path(self, _type: str) -> str:
        super()._get_file_path(_type)
        file_path_map = {
            "users": "users.json",
            "user_creds": "user_creds.json",
        }
        return file_path_map[_type]

    def create_user(
        self,
        name: str,
        surname: str,
        email: str,
        password: str,
        avatar_source: str = "",
    ) -> User:
        user_id = uuid4().hex
        user = User.create_item(
            _id=user_id, name=name, surname=surname, avatar_source=avatar_source
        )
        user_creds = UserCreds.create_item(
            user_id=user_id, email=email, password=password
        )
        self._users.put_item(user)
        self._user_creds.put_item(user_creds)
        self._dump_data("users")
        self._dump_data("user_creds")
        return user

    def get_users_by_ids(self, user_ids: List[str]) -> List[Dict]:
        return [self._users[_id].dict() for _id in user_ids]

    def get_user_creds(self, email: str) -> Dict:
        return self._user_creds.get_item(email).dict()


def get_user_dao(settings: ApiSettings = Depends(get_api_settings)) -> UserDao:
    return UserDao(settings=settings)
