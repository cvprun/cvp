# -*- coding: utf-8 -*-

from typing import Any

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.operators.arithmetic._base import ArithmeticOperatorNode
from cvp.types.override import override


class SubtractNode(ArithmeticOperatorNode):
    def __init__(self, dtype_registry: DtypeRegistry):
        super().__init__(dtype_registry, "subtract")

    @override
    def on_operator(self, first: Any, second: Any) -> Any:
        return first - second
