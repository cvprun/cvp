# -*- coding: utf-8 -*-

from typing import Any

from cvp.nodes.defaults.operators.arithmetic._base import ArithmeticOperatorNode
from cvp.types.override import override


class MultiplyOperator(ArithmeticOperatorNode):
    """Apply the multiply operator"""

    def __init__(self):
        super().__init__("multiply")

    @override
    def on_operator(self, first: Any, second: Any) -> Any:
        return first * second
