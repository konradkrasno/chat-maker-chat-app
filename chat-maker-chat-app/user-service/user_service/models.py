from hashlib import sha256
from uuid import uuid4

from commons.models import AbstractModel


class User(AbstractModel):
    id: str
    avatarSource: str
    name: str
    surname: str

    @classmethod
    def create_item(cls, _id: str, avatar_source: str, name: str, surname: str):
        return cls.load_from_dict(
            id=_id, avatarSource=avatar_source, name=name, surname=surname
        )

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(**kwargs)


class UserCreds(AbstractModel):
    user_id: str
    email: str
    password: str
    salt: str

    @classmethod
    def create_item(cls, user_id: str, email: str, password: str):
        salt = cls._get_salt()
        return cls.load_from_dict(
            user_id=user_id,
            email=email,
            password=cls._hash_password(password, salt),
            salt=salt,
        )

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(**kwargs)

    @staticmethod
    def _get_salt() -> str:
        return uuid4().hex[:6]

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        salted_password = f"{salt}{password}"
        return sha256(salted_password.encode()).hexdigest()

    def is_valid(self, password: str) -> bool:
        if self._hash_password(password, self.salt) == self.password:
            return True
        return False
