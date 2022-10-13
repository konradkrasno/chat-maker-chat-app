import json
import re
from typing import Optional

from fastapi import HTTPException, Request, status
from pydantic import BaseModel, ValidationError, validator


class BaseHeaders(BaseModel):
    device_id: str

    @classmethod
    async def get_headers(cls, request: Request):
        headers = request.headers
        try:
            return cls(**headers)
        except ValidationError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid headers")


class AuthenticationHeaders(BaseHeaders):
    authorization: str


class BaseRequestModel(BaseModel):
    @staticmethod
    async def load_request(request: Request) -> json:
        body = await request.body()
        return json.loads(body)

    @classmethod
    async def load_from_request(cls, request: Request):
        try:
            body = await cls.load_request(request)
            return cls(**body)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid request body: {e.__str__()}",
            )


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


class LoginRequestModel(BaseRequestModel):
    email: str
    password: str
