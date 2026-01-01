# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .corr_node import CorrNode
from .describe_node import DescribeNode
from .mean_node import MeanNode
from .std_node import StdNode


def get_statistics_nodes() -> List[Node]:
    """Get all statistics pandas nodes."""
    return [
        DescribeNode(),
        MeanNode(),
        StdNode(),
        CorrNode(),
    ]
