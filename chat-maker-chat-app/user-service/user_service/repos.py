from typing import Dict

from user_service.models import User, UserCreds

from commons.repos import AbstractRepo


class UserRepo(AbstractRepo):
    """
    Dict containing all users
        key: user id
        value: User object
    """

    @classmethod
    def load_from_dict(cls, data: Dict):
        return cls._base_load_from_dict(data, User)


class UserCredsRepo(AbstractRepo):
    """
    Dict containing hashed users credentials
        key: email
        value: User credentials
    """

    repo_key = ("email",)
    unique_fields = ("email",)

    @classmethod
    def load_from_dict(cls, data: Dict):
        return cls._base_load_from_dict(data, UserCreds)
