# -*- coding: utf-8 -*-

from typing import Optional

from cvp.dtypes.dtype import Dtype
from cvp.nodes.record import NodeRecord
from cvp.nodes.template import NodeName, NodePath, NodeTemplate
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import Pin, PinName
from cvp.pins.special import NextPin, PrevPin, ReturnPin
from cvp.types.override import override


class CastingNodeTemplate(NodeTemplate):
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
        super().__init__(
            path=NodePath(f"cvp.casting.{cls.__name__}"),
            name=NodeName(cls.__name__),
            func=None,
            docs=f"Casting to {cls.__name__} type",
            pins=(self._prev, self._next, self._value, self._return),
            tags=("casting", cls.__name__),
        )

    @override
    def run(self, record: NodeRecord) -> Optional[Pin]:
        record.set(self._return, self._return.dtype(record.get(self._value)))
        return self._next
