# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, Optional
from uuid import uuid4

from type_serialize import Serializable

from cvp.types.override import override


class FlowWorkspace(Serializable):

    @unique
    class _Keys(StrEnum):
        uuid = auto()
        name_ = "name"

    def __init__(
        self,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
    ):
        self.uuid = uuid if uuid else str(uuid4())
        self.name = name if name else str()

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.uuid == other.uuid and self.name == other.name

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = copy(self.uuid)
        result.name = copy(self.name)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = deepcopy(self.uuid, memo)
        result.name = deepcopy(self.name, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        return {
            str(self._Keys.uuid): str(self.uuid),
            str(self._Keys.name_): str(self.name),
        }

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.uuid = data.get(self._Keys.uuid, str())
        self.name = data.get(self._Keys.name_, str())

    @property
    def opened(self) -> bool:
        return False

    def open(self) -> bool:
        return False

    def close(self):
        pass
