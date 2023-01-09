from typing import Dict
from uuid import uuid4

import arrow
import jwt
from commons.models import AbstractModel
from pydantic import BaseModel


class TokenPayload(BaseModel):
    user_id: str
    time_to_expiry: int
    session_id: str
    device_id: str

    @classmethod
    def create_payload(cls, user_id: str, session_id: str, device_id: str) -> Dict:
        return cls(
            user_id=user_id,
            time_to_expiry=arrow.now().shift(hours=1).timestamp(),
            session_id=session_id,
            device_id=device_id,
        ).dict()


class Session(AbstractModel):
    id: str
    user_id: str
    device_id: str
    secret: str

    def generate_token(self) -> str:
        token_payload = TokenPayload.create_payload(
            user_id=self.user_id, session_id=self.id, device_id=self.device_id
        )
        return jwt.encode(token_payload, self.secret, algorithm="HS256")

    @classmethod
    def create_item(cls, user_id: str, device_id: str):
        return cls(
            id=uuid4().hex,
            user_id=user_id,
            device_id=device_id,
            secret=uuid4().hex,
        )

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(**kwargs)
