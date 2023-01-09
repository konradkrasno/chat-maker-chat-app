import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Union

from commons.settings import CommonSettings, get_common_settings
from fastapi import Depends


class BaseDao(ABC):
    def __init__(self, settings: CommonSettings = Depends(get_common_settings)):
        self.__storage_type = settings.storage_type
        self._settings = settings

    @abstractmethod
    def _get_file_path(self, _type: str) -> str:
        pass

    def _get_base_file_path(self, _type: str) -> Path:
        return self._settings.data_dir / self._get_file_path(_type)

    def _load_data(self, _type: str) -> Union[Dict, List]:
        if self.__storage_type == "files":
            file_path = self._get_base_file_path(_type)
            if file_path.exists():
                with open(file_path, "r") as file:
                    return json.load(file)
            with open(file_path, "w") as file:
                json.dump({}, file)
        return {}

    def _dump_data(self, _type: str) -> None:
        if self.__storage_type == "files":
            file_path = self._get_base_file_path(_type)
            with open(file_path, "w") as file:
                return json.dump(self.__getattribute__(f"_{_type}").serialize(), file)
