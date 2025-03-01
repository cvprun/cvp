# -*- coding: utf-8 -*-

from sys import exc_info
from typing import Any, Optional

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin
from cvp.pins.special import NextPin, PrevPin, ReturnPin
from cvp.types.override import override


class StringNode(Node):
    def __init__(self, dtype_registry: DtypeRegistry):
        self._prev = PrevPin()
        self._next = NextPin()
        self._value = DataInputPin(
            name="value",
            dtype=dtype_registry.get(Any),
            docs="Source value",
            required=True,
        )
        self._return = ReturnPin(dtype_registry.get(str))

        super().__init__(
            name="String",
            path="cvp.casting.string",
            func=None,
            docs="Logs a message with integer level level on this logger",
            pins=(self._prev, self._next, self._value, self._return),
            tags=("casting", "str", "string"),
        )

    @override
    def run(self, record: NodeRecord) -> Optional[str]:
        try:
            record.result = str(record.get(self._value))
        except:  # noqa
            record.exception = exc_info()
        return self._next.name
