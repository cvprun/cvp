# -*- coding: utf-8 -*-

import os
from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import Any, List, Optional, Union

from cvp.system.path import PathFlavour
from cvp.types.override import override


class FormatInterface(ABC):
    @abstractmethod
    def dumps(self, data: Any) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def loads(self, data: bytes) -> Any:
        raise NotImplementedError


class BaseFormatPath(PathFlavour, FormatInterface):
    def __init__(
        self,
        path: Union[str, PathLike[str]],
        *,
        extension: Optional[str] = None,
    ):
        super().__init__(path)
        self._extension = extension if extension else str()

    @property
    def extension(self) -> str:
        return self._extension

    @override
    def dumps(self, data: Any) -> bytes:
        raise NotImplementedError

    @override
    def loads(self, data: bytes) -> Any:
        raise NotImplementedError

    def object_path(self, *subpaths: str):
        if not subpaths:
            raise ValueError("At least one path must be specified")
        path = os.path.join(self, *subpaths)
        ext = os.path.splitext(path)[1]
        if ext != self._extension:
            path += self._extension
        return Path(path)

    def has_object(self, *subpaths: str) -> bool:
        return self.object_path(*subpaths).is_file()

    def read_object(self, *subpaths: str) -> Any:
        obj_path = self.object_path(*subpaths)
        obj_data = obj_path.read_bytes()
        return self.loads(obj_data)

    def write_object(self, o: Any, *subpaths: str) -> int:
        obj_path = self.object_path(*subpaths)
        obj_path.parent.mkdir(parents=True, exist_ok=True)
        obj_data = self.dumps(o)
        return obj_path.write_bytes(obj_data)

    def remove_object(self, *subpaths: str) -> None:
        return os.remove(self.object_path(*subpaths))

    def find_object_filepaths(self) -> List[str]:
        return self._find_files_with_extensions(self._extension, join_dirpath=True)

    def find_object_filenames(self) -> List[str]:
        return self._find_files_with_extensions(self._extension, join_dirpath=False)
