# -*- coding: utf-8 -*-

from typing import Any

from cvp.nodes.defaults.operators.arithmetic._base import ArithmeticOperatorNode
from cvp.types.override import override


class DivideNode(ArithmeticOperatorNode):
    def __init__(self):
        super().__init__("divide")

    @override
    def on_operator(self, first: Any, second: Any) -> Any:
        return first / second
