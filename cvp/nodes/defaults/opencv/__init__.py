# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.defaults.opencv.core import get_core_nodes
from cvp.nodes.defaults.opencv.features import get_features_nodes
from cvp.nodes.defaults.opencv.imgproc import get_imgproc_nodes
from cvp.nodes.defaults.opencv.ml import get_ml_nodes
from cvp.nodes.defaults.opencv.objdetect import get_objdetect_nodes
from cvp.nodes.defaults.opencv.video import get_video_nodes
from cvp.nodes.node import Node


def get_opencv_nodes() -> List[Node]:
    """Get all OpenCV nodes."""
    result: List[Node] = []
    result.extend(get_core_nodes())
    result.extend(get_imgproc_nodes())
    result.extend(get_features_nodes())
    result.extend(get_video_nodes())
    result.extend(get_objdetect_nodes())
    result.extend(get_ml_nodes())
    return result
