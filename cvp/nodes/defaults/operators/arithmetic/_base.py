# -*- coding: utf-8 -*-

from abc import abstractmethod
from typing import Any, Optional

from cvp.dtypes.dtype import Dtype
from cvp.nodes.record import NodeRecord
from cvp.nodes.template import NodeName, NodePath, NodeTemplate
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import Pin, PinName
from cvp.pins.special import ReturnPin
from cvp.types.override import override


class ArithmeticOperatorNodeTemplate(NodeTemplate):
    def __init__(self, name: str):
        self._first = DataInputPin(
            name=PinName("first"),
            dtype=Dtype.any(),
            docs=f"The first value of the {name.lower()} operator",
        )
        self._second = DataInputPin(
            name=PinName("second"),
            dtype=Dtype.any(),
            docs=f"The second value of the {name.lower()} operator",
        )
        self._return = ReturnPin(Dtype.any())
        super().__init__(
            path=NodePath(f"cvp.operators.arithmetic.{name.lower()}"),
            name=NodeName(name.capitalize()),
            docs=f"Apply the {name.lower()} operator",
            pins=(self._first, self._second, self._return),
            tags=("operator", "arithmetic", name.lower()),
        )

    @override
    def run(self, record: NodeRecord) -> Optional[Pin]:
        first = record.get(self._first)
        second = record.get(self._second)
        result = self.on_operator(first, second)
        record.set(self._return, result)
        return None

    @abstractmethod
    def on_operator(self, first: Any, second: Any) -> Any:
        raise NotImplementedError
