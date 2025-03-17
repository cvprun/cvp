# -*- coding: utf-8 -*-

from typing import Any

from cvp.nodes.defaults.operators.comparison._base import ComparisonOperatorNode
from cvp.types.override import override


class GreaterOperator(ComparisonOperatorNode):
    """Apply the greater operator"""

    def __init__(self):
        super().__init__("greater")

    @override
    def on_operator(self, first: Any, second: Any) -> bool:
        return first > second
