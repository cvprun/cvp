# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from importlib import import_module
from typing import (
    Any,
    Dict,
    Final,
    Generic,
    NewType,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from type_serialize import Serializable

from cvp.inspect.parameter import NoDefault
from cvp.types.override import override
from cvp.variables import MODULE_PATH_SEPARATOR

_T = TypeVar("_T")
TypePath = NewType("TypePath", str)

NONE_TYPE_CLS: Final[type] = type(None)
NONE_TYPE_PATH: Final[TypePath] = TypePath("builtins.NoneType")
NONE_TYPE_CLS_PATH: Final[Tuple[type, TypePath]] = NONE_TYPE_CLS, NONE_TYPE_PATH


def generate_type_path(cls: type) -> TypePath:
    return TypePath(cls.__module__ + MODULE_PATH_SEPARATOR + cls.__name__)


def load_with_path(path: str) -> Tuple[type, TypePath]:
    if path == NONE_TYPE_PATH:
        return NONE_TYPE_CLS_PATH

    module_path, class_name = path.rsplit(MODULE_PATH_SEPARATOR, 1)
    module = import_module(module_path)
    cls = getattr(module, class_name)
    if not isinstance(cls, type):
        raise TypeError(f"This is not a class type: '{path}'")
    return cls, TypePath(path)


def load_with_cls(cls: type) -> Tuple[type, TypePath]:
    if cls is NoDefault:
        return Any, generate_type_path(Any)  # type: ignore[return-value,arg-type]
    else:
        return cls, generate_type_path(cls)


def load(cls: Union[None, str, type]) -> Tuple[type, TypePath]:
    if cls is None:
        return NONE_TYPE_CLS_PATH
    elif isinstance(cls, str):
        return load_with_path(TypePath(cls))
    else:
        return load_with_cls(cls)


class Dtype(Generic[_T], Serializable):
    _type: Type[_T]
    _path: TypePath

    def __init__(self, cls: Union[None, str, type, Type[_T]]):
        self._type, self._path = load(cls)
        assert isinstance(self._type, type)
        assert isinstance(self._path, str)

    @classmethod
    def none(cls):
        return cls(None)

    @classmethod
    def any(cls):
        return cls(Any)

    def __str__(self) -> str:
        return self._path

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self._path}>"

    def __hash__(self) -> int:
        return hash((self.__class__, self._type, self._path))

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False

        if self._type is other._type:
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
        return str(self._path)

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, str):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")
        self._type, self._path = load_with_path(data)
        assert isinstance(self._type, type)
        assert isinstance(self._path, str)

    @property
    def type(self) -> Type[_T]:
        return self._type

    @property
    def path(self) -> TypePath:
        return self._path

    @property
    def docs(self) -> str:
        return self._type.__doc__ if self._type.__doc__ else str()

    def split(self) -> Tuple[str, str]:
        module_path, class_name = self._path.rsplit(MODULE_PATH_SEPARATOR, 1)
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
