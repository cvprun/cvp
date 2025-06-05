# -*- coding: utf-8 -*-

from typing import Optional, Protocol

from cvp.types.override import override
from cvp.values.proxy import ProxyValue, ValueT


class LockableProtocol(Protocol):
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_val, exc_tb): ...


class LockableProxyValue(ProxyValue[ValueT]):
    def __init__(self, value: ValueT, *, locker: Optional[LockableProtocol] = None):
        self._locker = locker
        self.value = value

    def __bool__(self):
        return bool(self.value)

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"<{type(self).__name__} @{id(self)} {self.value}>"

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __ge__(self, other):
        return self.value >= other

    def __gt__(self, other):
        return self.value > other

    def __le__(self, other):
        return self.value <= other

    def __lt__(self, other):
        return self.value < other

    def __hash__(self):
        return hash(self.value)

    @override
    def get(self) -> ValueT:
        if self._locker is None:
            return self.value
        else:
            with self._locker:
                return self.value

    @override
    def set(self, value: ValueT) -> None:
        if self._locker is None:
            self.value = value
        else:
            with self._locker:
                self.value = value
