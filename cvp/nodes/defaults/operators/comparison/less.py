# -*- coding: utf-8 -*-

from typing import Any

from cvp.nodes.defaults.operators.comparison._base import ComparisonOperatorNode
from cvp.types.override import override


class LessOperator(ComparisonOperatorNode):
    """Apply the less operator"""

    def __init__(self):
        super().__init__("less")

    @override
    def on_operator(self, first: Any, second: Any) -> bool:
        return first < second
