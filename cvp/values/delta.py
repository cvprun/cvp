# -*- coding: utf-8 -*-

from typing import Callable, Generic, Optional, TypeVar

_T = TypeVar("_T")


class DeltaValue(Generic[_T]):
    """
    A class designed for interoperability with `imgui`.

    Provides a value container that tracks changes and
    optionally triggers a callback when updated.
    """

    def __init__(
        self,
        value: _T,
        prev: _T,
        callback: Optional[Callable[[_T, _T], None]] = None,
    ):
        self.prev = prev
        self.value = value
        self._callback = callback

    @classmethod
    def from_single_value(
        cls,
        value: _T,
        on_change: Optional[Callable[[_T, _T], None]] = None,
    ):
        return cls(value, value, on_change)

    @property
    def changed(self) -> bool:
        return self.prev != self.value

    def update(self, value: _T, *, no_emit=False) -> bool:
        self.prev = self.value
        self.value = value

        changed = self.prev != self.value
        if not no_emit and changed and self._callback is not None:
            self._callback(self.value, self.prev)
        return changed
