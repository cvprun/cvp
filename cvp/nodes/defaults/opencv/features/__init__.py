# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .bf_matcher_node import BFMatcherNode
from .corner_harris_node import CornerHarrisNode
from .draw_keypoints_node import DrawKeypointsNode
from .good_features_to_track_node import GoodFeaturesToTrackNode
from .orb_detect_node import ORBDetectNode
from .sift_detect_node import SIFTDetectNode


def get_features_nodes() -> List[Node]:
    """Get all features OpenCV nodes."""
    return [
        BFMatcherNode(),
        CornerHarrisNode(),
        DrawKeypointsNode(),
        GoodFeaturesToTrackNode(),
        ORBDetectNode(),
        SIFTDetectNode(),
    ]
