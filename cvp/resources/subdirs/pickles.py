# -*- coding: utf-8 -*-

import os
from os import PathLike
from pathlib import Path
from pickle import dumps, loads
from typing import Any, Final, Union

from cvp.system.path import PathFlavour

PICKLE_PROTOCOL_VERSION: Final[int] = 5
PICKLE_ENCODING: Final[str] = "ASCII"


class PicklesPath(PathFlavour):
    def __init__(self, *path: Union[str, PathLike[str]]):
        super().__init__(*path)
        self._pickle_protocol_version = PICKLE_PROTOCOL_VERSION
        self._pickle_encoding = PICKLE_ENCODING

    def pickling(self, data: Any) -> bytes:
        return dumps(data, protocol=self._pickle_protocol_version)

    def unpickling(self, data: bytes) -> Any:
        return loads(data, encoding=self._pickle_encoding)

    def object_path(self, *paths: str):
        if not paths:
            raise ValueError("At least one path must be specified.")
        return Path(os.path.join(self, *paths))

    def has_object(self, *paths: str) -> bool:
        return self.object_path(*paths).is_file()

    def read_object(self, *paths: str) -> Any:
        obj_path = self.object_path(*paths)
        obj_data = obj_path.read_bytes()
        return self.unpickling(obj_data)

    def write_object(self, o: Any, *paths: str) -> int:
        obj_path = self.object_path(*paths)
        obj_path.parent.mkdir(parents=True, exist_ok=True)
        obj_data = self.pickling(o)
        return obj_path.write_bytes(obj_data)

    def remove_object(self, *paths: str) -> None:
        return os.remove(self.object_path(*paths))
