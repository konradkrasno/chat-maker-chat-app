import re
from typing import List, Optional

from commons.api_models import BaseRequestModel
from pydantic import validator


class SignInRequestModel(BaseRequestModel):
    name: str
    surname: str
    email: str
    password: str
    avatar_source: Optional[str] = ""

    @validator("email")
    def check_email(cls, v):
        if not re.findall("^[\\w\\.\\-_]+@[\\w\\.\\-_]+\\.[\\w]+$", v):
            raise ValueError(f"Invalid email value: '{v}'")
        return v

    @validator("password")
    def check_password(cls, v):
        if len(v) < 7:
            raise ValueError("Password must have at least 8 chars")
        return v


class GetUsersByIdsRequestModel(BaseRequestModel):
    user_ids: List[str]


class GetUserCredsRequestModel(BaseRequestModel):
    email: str
