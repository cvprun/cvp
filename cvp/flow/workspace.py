# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from uuid import uuid4
from typing import Any, Dict, NewType, Optional

from type_serialize import Serializable
from cvp.types.override import override

WorkspaceKey = NewType("WorkspaceKey", str)
WorkspaceName = NewType("WorkspaceName", str)


class FlowWorkspace(Serializable):

    @unique
    class _Keys(StrEnum):
        key = auto()
        name_ = "name"

    def __init__(
        self,
        key: Optional[WorkspaceKey] = None,
        name: Optional[WorkspaceName] = None,
    ):
        self.key = key if key else WorkspaceKey(str(uuid4()))
        self.name = name if name else WorkspaceName(str())

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.key == other.key and self.name == other.name

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.key = copy(self.key)
        result.name = copy(self.name)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.key = deepcopy(self.key, memo)
        result.name = deepcopy(self.name, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        return {
            str(self._Keys.key): str(self.key),
            str(self._Keys.name_): str(self.name),
        }

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.key = WorkspaceKey(data.get(self._Keys.key, str()))
        self.name = WorkspaceName(data.get(self._Keys.name_, str()))

    def open(self) -> bool:
        return False

    def close(self):
        pass
