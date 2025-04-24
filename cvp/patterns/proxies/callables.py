# -*- coding: utf-8 -*-

from typing import Callable, Optional

from cvp.patterns.proxy import ValueProxy, ValueT
from cvp.types.override import override


class CallableTypeProxy(ValueProxy[ValueT]):
    def __init__(
        self,
        getter: Optional[Callable[[], ValueT]] = None,
        setter: Optional[Callable[[ValueT], None]] = None,
    ):
        self._getter = getter
        self._setter = setter

    @override
    def get(self) -> ValueT:
        if self._getter is None:
            raise ValueError("Getter is not defined")

        return self._getter()

    @override
    def set(self, value: ValueT) -> None:
        if self._setter is None:
            raise ValueError("Setter is not defined")

        self._setter(value)
