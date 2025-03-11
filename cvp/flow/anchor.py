# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, Optional

from type_serialize import Serializable

from cvp.types.override import override
from cvp.types.shapes import Point


class FlowAnchor(Serializable):

    @unique
    class _Keys(StrEnum):
        x = auto()
        y = auto()

    def __init__(
        self,
        x=0.0,
        y=0.0,
        *,
        selected=False,
        hovering=False,
    ):
        self.x = x
        self.y = y
        self._selected = selected
        self._hovering = hovering

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.x == other.x and self.y == other.y

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.x = copy(self.x)
        result.y = copy(self.y)
        result._selected = copy(self._selected)
        result._hovering = copy(self._hovering)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.x = deepcopy(self.x, memo)
        result.y = deepcopy(self.y, memo)
        result._selected = deepcopy(self._selected, memo)
        result._hovering = deepcopy(self._hovering, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        result = {self._Keys.x: self.x, self._Keys.y: self.y}
        return {str(key): val for key, val in result.items()}

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.x = data.get(self._Keys.x, 0.0)
        self.y = data.get(self._Keys.y, 0.0)
        self._selected = False
        self._hovering = False

    @property
    def point(self):
        return self.x, self.y

    @point.setter
    def point(self, value: Point) -> None:
        self.x = value[0]
        self.y = value[1]

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        self._selected = value

    @property
    def hovering(self):
        return self._hovering

    @hovering.setter
    def hovering(self, value: bool) -> None:
        self._hovering = value
