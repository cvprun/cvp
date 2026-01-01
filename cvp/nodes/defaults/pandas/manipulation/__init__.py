# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .concat_node import ConcatNode
from .drop_node import DropNode
from .filter_node import FilterNode
from .merge_node import MergeNode
from .select_node import SelectNode
from .sort_values_node import SortValuesNode


def get_manipulation_nodes() -> List[Node]:
    """Get all manipulation pandas nodes."""
    return [
        SelectNode(),
        FilterNode(),
        DropNode(),
        SortValuesNode(),
        ConcatNode(),
        MergeNode(),
    ]
