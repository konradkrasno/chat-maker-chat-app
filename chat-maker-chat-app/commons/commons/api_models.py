import json

from fastapi import HTTPException, Request, status
from pydantic import BaseModel


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
