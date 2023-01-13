from abc import ABC, abstractmethod
from typing import Optional

from fastapi import Cookie
from pydantic import BaseModel


class AbstractModel(ABC, BaseModel):
    @classmethod
    @abstractmethod
    def load_from_dict(cls, **kwargs):
        pass


class AuthCookies(BaseModel):
    access_token: Optional[str]
    user_id: Optional[str]
    device_id: Optional[str]


def get_auth_cookies(
    access_token: Optional[str] = Cookie(default=None),
    user_id: Optional[str] = Cookie(default=None),
    device_id: Optional[str] = Cookie(default=None),
) -> AuthCookies:
    return AuthCookies(
        access_token=access_token,
        user_id=user_id,
        device_id=device_id,
    )
