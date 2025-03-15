# -*- coding: utf-8 -*-

from typing import List, Sequence

from cvp.nodes.defaults.operators.arithmetic import get_arithmetic_nodes
from cvp.nodes.defaults.operators.comparison import get_comparison_nodes
from cvp.nodes.template import NodeTemplate


def get_operators_nodes() -> Sequence[NodeTemplate]:
    result: List[NodeTemplate] = list()
    result.extend(get_arithmetic_nodes())
    result.extend(get_comparison_nodes())
    return tuple(result)
