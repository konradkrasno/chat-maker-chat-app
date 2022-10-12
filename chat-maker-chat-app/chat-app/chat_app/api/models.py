import json
from typing import Optional

from fastapi import Request
from pydantic import BaseModel


async def load_request(request: Request) -> json:
    body = await request.body()
    return json.loads(body)


class SignInRequestModel(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    avatar_source: Optional[str] = ""

    @classmethod
    async def load_from_request(cls, request: Request) -> "SignInRequestModel":
        body = await load_request(request)
        return cls(**body)
