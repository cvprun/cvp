# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .background_subtractor_knn_node import BackgroundSubtractorKNNNode
from .background_subtractor_mog2_node import BackgroundSubtractorMOG2Node
from .calc_optical_flow_pyr_lk_node import CalcOpticalFlowPyrLKNode


def get_video_nodes() -> List[Node]:
    """Get all video processing OpenCV nodes."""
    return [
        BackgroundSubtractorKNNNode(),
        BackgroundSubtractorMOG2Node(),
        CalcOpticalFlowPyrLKNode(),
    ]
