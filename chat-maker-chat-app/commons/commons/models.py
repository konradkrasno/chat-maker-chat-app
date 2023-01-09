from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractModel(ABC, BaseModel):
    @abstractmethod
    def load_from_dict(self, **kwargs):
        pass
