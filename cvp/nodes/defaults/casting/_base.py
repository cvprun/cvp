# -*- coding: utf-8 -*-

from typing import Any, Optional

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPinTemplate
from cvp.pins.special import NextPin, PrevPin, ReturnPin
from cvp.pins.template import PinTemplate
from cvp.types.override import override


class CastingNode(Node):
    def __init__(self, dtype_registry: DtypeRegistry, cls: type):
        self._prev = PrevPin()
        self._next = NextPin()
        self._value = DataInputPinTemplate(
            name="value",
            dtype=dtype_registry.get(Any),
            docs="Source value",
            required=True,
        )
        self._return = ReturnPin(dtype_registry.get(cls))
        super().__init__(
            name=cls.__name__,
            path=f"cvp.casting.{cls.__name__}",
            func=None,
            docs=f"Casting to {cls.__name__} type",
            pins=(self._prev, self._next, self._value, self._return),
            tags=("casting", cls.__name__),
        )

    @override
    def run(self, record: NodeRecord) -> Optional[PinTemplate]:
        record.set(self._return, self._return.dtype.type(record.get(self._value)))
        return self._next
