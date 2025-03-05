# -*- coding: utf-8 -*-

from abc import abstractmethod
from typing import Any, Optional

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.record import NodeRecord
from cvp.nodes.template import NodeTemplate
from cvp.pins.datas import DataInputPinTemplate
from cvp.pins.special import ReturnPin
from cvp.pins.template import PinTemplate
from cvp.types.override import override


class ArithmeticOperatorNodeTemplate(NodeTemplate):
    def __init__(self, dtype_registry: DtypeRegistry, name: str):
        self._first = DataInputPinTemplate(
            name="first",
            dtype=dtype_registry.get(Any),
            docs=f"The first value of the {name.lower()} operator",
        )
        self._second = DataInputPinTemplate(
            name="second",
            dtype=dtype_registry.get(Any),
            docs=f"The second value of the {name.lower()} operator",
        )
        self._return = ReturnPin(
            dtype=dtype_registry.get(Any),
            docs=f"The result value of the {name.lower()} operator.",
        )
        super().__init__(
            name=name.capitalize(),
            path=f"cvp.operators.arithmetic.{name.lower()}",
            docs=f"Apply the {name.lower()} operator",
            pins=(self._first, self._second, self._return),
            tags=("operator", "arithmetic", name.lower()),
        )

    @override
    def run(self, record: NodeRecord) -> Optional[PinTemplate]:
        first = record.get(self._first)
        second = record.get(self._second)
        result = self.on_operator(first, second)
        record.set(self._return, result)
        return None

    @abstractmethod
    def on_operator(self, first: Any, second: Any) -> Any:
        raise NotImplementedError
