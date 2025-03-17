# -*- coding: utf-8 -*-

from cvp.dtypes.dtype import Dtype
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import Pin, PinName
from cvp.pins.special import NextPin, PrevPin, ReturnPin
from cvp.types.override import override


class CastingNode(Node):
    def __init__(self, cls: type):
        self._prev = PrevPin()
        self._next = NextPin()
        self._value = DataInputPin(
            name=PinName("value"),
            dtype=Dtype.any(),
            docs="Source value",
            required=True,
        )
        self._return = ReturnPin(Dtype(cls))
        super().__init__(self._prev, self._next, self._value, self._return)

    @override
    def run(self, record: NodeRecord) -> Pin:
        record.set(self._return, self._return.dtype(record.get(self._value)))
        return self._next
