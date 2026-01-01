# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .kmeans_node import KMeansNode


def get_ml_nodes() -> List[Node]:
    """Get all machine learning OpenCV nodes."""
    return [
        KMeansNode(),
    ]
