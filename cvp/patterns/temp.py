# -*- coding: utf-8 -*-

from typing import Generic, TypeVar

from cvp.memory.copy import copy_flexible

_T = TypeVar("_T")


class TempValue(Generic[_T]):
    def __init__(self, value: _T, temp: _T):
        self._value = value
        self._temp = temp

    @classmethod
    def from_single_value(cls, value: _T):
        return cls(value, value)

    @property
    def value(self) -> _T:
        return self._value

    @value.setter
    def value(self, value: _T) -> None:
        """
        This setter is intentionally not implemented.
        Use the 'commit' method to modify 'value' instead.
        """
        raise NotImplementedError("'value' must be modified via the 'commit' method")

    @property
    def temp(self) -> _T:
        return self._temp

    @temp.setter
    def temp(self, value: _T) -> None:
        self._temp = value

    @property
    def changed(self) -> bool:
        return self._value != self._temp

    def reset(self) -> None:
        self._temp = self._value

    def commit(self) -> None:
        self._value = self._temp

    def fill(self, value: _T, *, use_copy=False, use_deepcopy=False) -> None:
        self._value = copy_flexible(value, use_copy=use_copy, use_deepcopy=use_deepcopy)
        self._temp = copy_flexible(value, use_copy=use_copy, use_deepcopy=use_deepcopy)
