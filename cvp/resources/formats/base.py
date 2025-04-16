# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from os import PathLike
from typing import Any, Final, Union

from cvp.system.path import PathFlavour
from cvp.types.override import override

BASE_EXTENSION: Final[str] = ".bin"


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
        *path: Union[str, PathLike[str]],
        extension=BASE_EXTENSION,
    ):
        super().__init__(*path)
        self._extension = extension

    @property
    def extension(self) -> str:
        return self._extension

    @override
    def dumps(self, data: Any) -> bytes:
        raise NotImplementedError

    @override
    def loads(self, data: bytes) -> Any:
        raise NotImplementedError

    def make_object_path(self, *subpaths: str):
        path = self.joinpath(*subpaths)
        if path.suffix == self._extension:
            return path
        else:
            return path.with_suffix(self._extension)

    def has_object(self, *subpaths: str) -> bool:
        return self.make_object_path(*subpaths).is_file()

    def read_object(self, *subpaths: str) -> Any:
        obj_path = self.make_object_path(*subpaths)
        obj_data = obj_path.read_bytes()
        return self.loads(obj_data)

    def write_object(self, o: Any, *subpaths: str) -> int:
        obj_path = self.make_object_path(*subpaths)
        obj_path.parent.mkdir(parents=True, exist_ok=True)
        obj_data = self.dumps(o)
        return obj_path.write_bytes(obj_data)

    def remove_object(self, *subpaths: str) -> None:
        return self.make_object_path(*subpaths).unlink()

    def list_object_filenames(self):
        return self.list_first_depth_filenames(self._extension, ignore_case=False)
