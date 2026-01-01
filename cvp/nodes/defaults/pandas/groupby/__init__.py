# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .groupby_node import GroupByNode


def get_groupby_nodes() -> List[Node]:
    """Get all groupby pandas nodes."""
    return [
        GroupByNode(),
    ]
