from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractModel(ABC, BaseModel):
    @classmethod
    @abstractmethod
    def load_from_dict(cls, **kwargs):
        pass
