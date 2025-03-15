# -*- coding: utf-8 -*-

from typing import Any

from cvp.nodes.defaults.operators.comparison._base import ComparisonOperatorNode
from cvp.types.override import override


class GreaterEqualNode(ComparisonOperatorNode):
    def __init__(self):
        super().__init__("greater-equal")

    @override
    def on_operator(self, first: Any, second: Any) -> bool:
        return first >= second
