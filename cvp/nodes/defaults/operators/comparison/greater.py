# -*- coding: utf-8 -*-

from typing import Any

from cvp.nodes.defaults.operators.comparison._base import ComparisonOperatorNodeTemplate
from cvp.types.override import override


class GreaterNodeTemplate(ComparisonOperatorNodeTemplate):
    def __init__(self):
        super().__init__("greater-equal")

    @override
    def on_operator(self, first: Any, second: Any) -> bool:
        return first > second
