# -*- coding: utf-8 -*-

from typing import Optional

from cvp.dtypes.dtype import Dtype
from cvp.nodes.node import Node, NodeName, NodePath
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import Pin, PinName
from cvp.pins.special import NextPin, PrevPin
from cvp.types.override import override


class SetterNode(Node):
    def __init__(self):
        self._prev = PrevPin()
        self._next = NextPin()
        self._key = DataInputPin(
            name=PinName("key"),
            dtype=Dtype(str),
            docs="The key of the variable",
            required=True,
            hidden=True,
            default=None,
        )
        self._value = DataInputPin(
            name=PinName("value"),
            dtype=Dtype.any(),
            docs="The value of the variable",
        )
        super().__init__(
            path=NodePath("cvp.essential.setter"),
            name=NodeName("Setter"),
            docs="Set a variable to a specific value",
            pins=(self._prev, self._next, self._key, self._value),
            tags=("value", "variable", "setter", "mutator"),
        )

    @property
    def key_name(self):
        return self._key.name

    @property
    def value_name(self):
        return self._value.name

    @override
    def run(self, record: NodeRecord) -> Optional[Pin]:
        key = record.get(self._key)
        assert isinstance(key, str)
        value = record.get(self._value)
        record.set_shared(key, value)
        return self._next
