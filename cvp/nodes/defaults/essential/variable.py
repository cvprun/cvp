# -*- coding: utf-8 -*-

from sys import exc_info
from typing import Optional

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.node import Node
from cvp.nodes.record import NodeExecutionRecord
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import Pin
from cvp.pins.special import NextPin, PrevPin
from cvp.types.override import override


class VariableSetterNode(Node):
    def __init__(self, dtype_registry: DtypeRegistry):
        self._prev = PrevPin()
        self._next = NextPin()
        self._key = DataInputPin(
            name="key",
            dtype=dtype_registry.get(str),
            docs="The key of the variable",
            required=True,
            hidden=True,
        )
        self._value = DataInputPin(
            name="value",
            docs="The value of the variable",
        )
        super().__init__(
            name="setter",
            path="cvp.setter",
            docs="Set a variable to a specific value",
            pins=(self._prev, self._next, self._key, self._value),
            tags=("value", "variable", "setter", "mutator"),
        )

    @override
    def run(self, pin: Pin, record: NodeExecutionRecord) -> Optional[Pin]:
        assert pin == self._prev
        try:
            key = record.get(self._key)
            assert isinstance(key, str)
            value = record.get(self._value)
            record.set_shared(key, value)
        except:  # noqa
            record.exception = exc_info()
        return self._next


class VariableGetterNode(Node):
    def __init__(self, dtype_registry: DtypeRegistry):
        self._prev = PrevPin()
        self._next = NextPin()
        self._key = DataInputPin(
            name="key",
            dtype=dtype_registry.get(str),
            docs="The key of the variable",
            required=True,
            hidden=True,
        )
        self._value = DataOutputPin(
            name="value",
            docs="The value of the variable",
        )
        super().__init__(
            name="getter",
            path="cvp.getter",
            docs="Get a variable to a specific value",
            pins=(self._prev, self._next, self._key, self._value),
            tags=("value", "variable", "getter", "accessor"),
        )

    @override
    def run(self, pin: Pin, record: NodeExecutionRecord) -> Optional[Pin]:
        assert pin == self._prev
        try:
            key = record.get(self._key)
            assert isinstance(key, str)
            value = record.get_shared(key)
            record.set(self._value, value)
        except:  # noqa
            record.exception = exc_info()
        return self._next
