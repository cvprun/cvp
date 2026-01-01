# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .dataframe_node import DataFrameNode
from .series_node import SeriesNode


def get_core_nodes() -> List[Node]:
    """Get all core pandas nodes."""
    return [
        DataFrameNode(),
        SeriesNode(),
    ]
