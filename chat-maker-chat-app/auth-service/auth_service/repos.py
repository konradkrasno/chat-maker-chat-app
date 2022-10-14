from typing import Dict

from auth_service.models import Session

from commons.repos import AbstractRepo


class SessionRepo(AbstractRepo):
    """
    Dict containing all sessions
        key: user id
        value: Chat object
    """

    repo_key = ("user_id", "device_id")
    unique_fields = ("user_id",)

    @classmethod
    def load_from_dict(cls, data: Dict):
        return cls._base_load_from_dict(data, Session)
