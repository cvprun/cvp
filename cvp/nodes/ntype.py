# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from importlib import import_module
from typing import (
    Any,
    Callable,
    Dict,
    Final,
    NewType,
    Optional,
    Tuple,
    Type,
    TypeGuard,
    Union,
)

from type_serialize import Serializable

from cvp.inspect.islambda import islambda
from cvp.nodes.base import NodeBase
from cvp.nodes.record import NodeRecord
from cvp.pins.pin import Pin
from cvp.types.override import override
from cvp.variables import MODULE_PATH_SEPARATOR

NodeUnion = Union[Callable[..., Any], Type[NodeBase]]
NodePath = NewType("NodePath", str)


class _NodeFaker(NodeBase):
    @override
    def run(self, record: NodeRecord) -> Pin:
        raise NotImplementedError("This object should not be called")

    @override
    def render(self, record: NodeRecord) -> None:
        raise NotImplementedError("This object should not be called")


_DEFAULT_NODE_FAKER: Final[_NodeFaker] = _NodeFaker()


def is_node_interface_type(obj) -> TypeGuard[Type[NodeBase]]:
    return isinstance(obj, type) and issubclass(obj, NodeBase)


def isnode(obj) -> bool:
    if islambda(obj):
        return False

    return is_node_interface_type(obj) or callable(obj)


def create_node_interface(obj) -> NodeBase:
    if isinstance(obj, type) and issubclass(obj, NodeBase):
        return obj()
    else:
        return _DEFAULT_NODE_FAKER


def generate_node_path(cls: NodeUnion) -> NodePath:
    return NodePath(cls.__module__ + MODULE_PATH_SEPARATOR + cls.__name__)


def load_with_path(path: str) -> Tuple[NodeUnion, NodePath]:
    module_path, class_name = path.rsplit(MODULE_PATH_SEPARATOR, 1)
    module = import_module(module_path)
    cls = getattr(module, class_name)

    if not isnode(cls):
        raise TypeError(f"This is not a node type: '{path}'")

    return cls, NodePath(path)


def load_with_cls(cls: NodeUnion) -> Tuple[NodeUnion, NodePath]:
    if not isnode(cls):
        raise TypeError(f"This is not a node type: '{cls.__name__}'")

    return cls, generate_node_path(cls)


def load(cls: Union[str, NodeUnion]) -> Tuple[NodeUnion, NodePath]:
    if isinstance(cls, str):
        return load_with_path(NodePath(cls))
    else:
        return load_with_cls(cls)


class Ntype(Serializable):
    _type: NodeUnion
    _path: NodePath
    _node: NodeBase

    def __init__(self, cls: Union[str, NodeUnion], node: Optional[NodeBase] = None):
        self._type, self._path = load(cls)
        assert isnode(self._type)
        assert isinstance(self._path, str)

        self._node = node if node is not None else create_node_interface(self._type)
        assert isinstance(self._node, NodeBase)

        if is_node_interface_type(self._type):
            if type(self._node) is not self._type:
                raise TypeError(
                    f"Expected node type {self._type.__name__}, "
                    f"but got {type(self._node).__name__}"
                )
        else:
            if not isinstance(self._node, _NodeFaker):
                raise TypeError(
                    f"Expected node type {_NodeFaker.__name__}, "
                    f"but got {type(self._node).__name__}"
                )

    @classmethod
    def from_node(cls, node: NodeBase):
        result = cls(type(node), node=node)
        assert result._node is node
        return result

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
        assert isnode(self._type)
        assert isinstance(self._path, str)

        self._node = create_node_interface(self._type)
        assert isinstance(self._node, NodeBase)

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

    def run(self, record: NodeRecord) -> Any:
        if is_node_interface_type(self._type):
            assert not isinstance(self._node, _NodeFaker)
            return self._node.run(record)
        elif callable(self._type):
            assert isinstance(self._node, _NodeFaker)
            return self._type(*record.args, **record.kwargs)
        else:
            assert False, "Inaccessible section"

    def render(self, record: NodeRecord) -> None:
        if is_node_interface_type(self._type):
            assert not isinstance(self._node, _NodeFaker)
            self._node.render(record)
        elif callable(self._type):
            assert isinstance(self._node, _NodeFaker)
        else:
            assert False, "Inaccessible section"

    def __call__(self, *args, **kwargs) -> Any:
        return self.run(NodeRecord.from_call(*args, **kwargs))
