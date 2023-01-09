from typing import Dict

from commons.exceptions import ItemAlreadyExistsError, ItemDoesNotExistsError
from commons.models import AbstractModel


class AbstractRepo:
    repo_key = ("id",)
    unique_fields = ("id",)

    def __init__(self):
        self._store = dict()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} repo"

    def __getitem__(self, item: str):
        return self._store[item]

    def __setitem__(self, key: str, value: AbstractModel):
        self._store[key] = value

    def __len__(self) -> int:
        return len(self._store)

    def get(self, key: str) -> AbstractModel:
        return self._store.get(key)

    def items(self):
        return self._store.items()

    def keys(self):
        return self._store.keys()

    def values(self):
        return self._store.values()

    @classmethod
    def _base_load_from_dict(cls, data: Dict, model: AbstractModel):
        inst = cls()
        for k, v in data.items():
            inst[k] = model.load_from_dict(**v)
        return inst

    def serialize(self) -> Dict:
        return {k: v.dict() for k, v in self.items()}

    def get_item(self, *attrs) -> AbstractModel:
        assert len(attrs) > 0, "Item id keys not provided!"
        key = self._get_key(*attrs)
        item = self.get(key)
        if item:
            return item
        raise ItemDoesNotExistsError(f"Can not find item with provided key: '{key}'.")

    def delete_item(self, *attrs) -> None:
        try:
            del self[self._get_key(*attrs)]
        except KeyError:
            pass

    @staticmethod
    def _get_key(*args) -> str:
        return "{}{}".format(
            args[0],
            "".join(f"-{attr}" for attr in args[1:]),
        )

    @classmethod
    def _get_key_from_item(cls, item: AbstractModel) -> str:
        attrs = [getattr(item, field) for field in cls.repo_key]
        return cls._get_key(*attrs)

    def put_item(self, item: AbstractModel) -> None:
        key = self._get_key_from_item(item)
        if key in self.keys():
            raise ItemAlreadyExistsError(
                f"{item.__class__.__name__} with key: '{key}' already exists"
            )
        for _obj in self.values():
            for field in self.unique_fields:
                f_v = getattr(item, field)
                if f_v == getattr(_obj, field):
                    raise ItemAlreadyExistsError(
                        f"{item.__class__.__name__} with field '{field}'='{f_v}' already exists"
                    )
        self[key] = item

    def update_item(self, item: AbstractModel) -> None:
        key = self._get_key_from_item(item)
        self[key] = item
