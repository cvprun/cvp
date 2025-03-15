# -*- coding: utf-8 -*-

from typing import Any

from cvp.nodes.defaults.operators.arithmetic._base import ArithmeticOperatorNode
from cvp.types.override import override


class AddNode(ArithmeticOperatorNode):
    def __init__(self):
        super().__init__("add")

    @override
    def on_operator(self, first: Any, second: Any) -> Any:
        return first + second
