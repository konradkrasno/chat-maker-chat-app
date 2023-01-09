import re
from typing import List, Optional

from pydantic import validator

from pydantic import BaseModel


class SignInRequestModel(BaseModel):
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


class GetUsersByIdsRequestModel(BaseModel):
    user_ids: List[str]


class GetUserCredsRequestModel(BaseModel):
    email: str
