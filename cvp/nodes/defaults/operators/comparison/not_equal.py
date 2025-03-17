# -*- coding: utf-8 -*-

from typing import Any

from cvp.nodes.defaults.operators.comparison._base import ComparisonOperatorNode
from cvp.types.override import override


class NotEqualOperator(ComparisonOperatorNode):
    """Apply the not-equal operator"""

    def __init__(self):
        super().__init__("not-equal")

    @override
    def on_operator(self, first: Any, second: Any) -> bool:
        return first != second
