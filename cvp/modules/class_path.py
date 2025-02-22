# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from importlib import import_module
from typing import Any, Dict, Generic, Optional, Tuple, Type, TypeVar, Union

from type_serialize import Serializable

from cvp.types.override import override

_T = TypeVar("_T")


def _load_with_path(path: str) -> Tuple[type, str]:
    module_path, class_name = path.rsplit(".", 1)
    module = import_module(module_path)
    cls = getattr(module, class_name)
    if not isinstance(cls, type):
        raise TypeError(f"This is not a class type: '{path}'")
    return cls, path


def _load_with_cls(cls: type) -> Tuple[type, str]:
    path = cls.__module__ + "." + cls.__name__
    return cls, path


def _load(cls: Union[str, Type[_T]]) -> Tuple[type, str]:
    if isinstance(cls, str):
        return _load_with_path(cls)
    else:
        return _load_with_cls(cls)


@unique
class ClassPathKey(StrEnum):
    path = auto()


class ClassPath(Generic[_T], Serializable):
    Keys = ClassPathKey

    _type: Type[_T]
    _path: str

    def __init__(self, cls: Union[None, str, type, Type[_T]] = None):
        if cls is None:
            # For Lazy-loading
            return

        self._type, self._path = _load(cls)
        assert isinstance(self._type, type)
        assert isinstance(self._path, str)

    def __str__(self) -> str:
        """In `cvp.flow` module, this return value is used as a key value."""
        return self._path

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False

        if self._type == other._type:
            assert self._path == other._path
            return True
        else:
            assert self._path != other._path
            return False

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result._type = copy(self._type)
        result._path = copy(self._path)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result._type = deepcopy(self._type, memo)
        result._path = deepcopy(self._path, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        result = {self.Keys.path: self._path}
        return {str(key): val for key, val in result.items()}

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        path = data.get(self.Keys.path)
        if not path:
            raise ValueError("Undefined class path")

        if not isinstance(path, str):
            raise TypeError(f"The type of '{str(self.Keys.path)}' only allows str")

        self._type, self._path = _load_with_path(path)
        assert isinstance(self._type, type)
        assert isinstance(self._path, str)

    @property
    def type(self) -> Type[_T]:
        return self._type

    @property
    def path(self) -> str:
        return self._path

    def split(self) -> Tuple[str, str]:
        module_path, class_name = self._path.rsplit(".", 1)
        assert isinstance(module_path, str)
        assert isinstance(class_name, str)
        return module_path, class_name

    @property
    def module_path(self) -> str:
        return self.split()[0]

    @property
    def class_name(self) -> str:
        return self.split()[1]

    def __call__(self, *args, **kwargs) -> _T:
        return self._type(*args, **kwargs)
