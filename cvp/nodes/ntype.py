# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from importlib import import_module
from inspect import isfunction
from typing import (
    Any,
    Callable,
    Dict,
    NewType,
    Optional,
    Tuple,
    Type,
    Union,
)

from type_serialize import Serializable

from cvp.nodes.interface import NodeInterface
from cvp.types.override import override
from cvp.variables import MODULE_PATH_SEPARATOR

NodeUnion = Union[Callable[..., Any], Type[NodeInterface]]
NodePath = NewType("NodePath", str)


def isnodetype(obj) -> bool:
    if isinstance(obj, type) and issubclass(obj, NodeInterface):
        return True
    return isfunction(obj)


def generate_node_path(cls: NodeUnion) -> NodePath:
    return NodePath(cls.__module__ + MODULE_PATH_SEPARATOR + cls.__name__)


def load_with_path(path: str) -> Tuple[type, NodePath]:
    module_path, class_name = path.rsplit(MODULE_PATH_SEPARATOR, 1)
    module = import_module(module_path)
    cls = getattr(module, class_name)

    if not isnodetype(cls):
        raise TypeError(f"This is not a node type: '{path}'")

    return cls, NodePath(path)


def load_with_cls(cls: NodeUnion) -> Tuple[NodeUnion, NodePath]:
    return cls, generate_node_path(cls)


def load(cls: Union[str, NodeUnion]) -> Tuple[NodeUnion, NodePath]:
    if isinstance(cls, str):
        return load_with_path(NodePath(cls))
    else:
        return load_with_cls(cls)


class Ntype(Serializable):
    _type: NodeUnion
    _path: NodePath

    def __init__(self, cls: Union[str, NodeUnion]):
        self._type, self._path = load(cls)
        assert isnodetype(self._type)
        assert isinstance(self._path, str)

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
        assert isnodetype(self._type)
        assert isinstance(self._path, str)

    @property
    def type(self) -> NodeUnion:
        return self._type

    @property
    def path(self) -> NodePath:
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

    def __call__(self, *args, **kwargs) -> Any:
        if isfunction(self._type):
            return self._type(*args, **kwargs)

        if isinstance(self._type, type):
            assert issubclass(self._type, NodeInterface)
            if 0 == len(args):
                raise ValueError("The first argument must be a NodeInterface instance")
            if not isinstance(args[0], NodeInterface):
                raise ValueError("The first argument must be a NodeInterface instance")
            return self._type.run(*args, **kwargs)
        else:
            assert isinstance(self._type, NodeInterface)
            return self._type.run(*args, **kwargs)
