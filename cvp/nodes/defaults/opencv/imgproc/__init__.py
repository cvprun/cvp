# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .adaptive_threshold_node import AdaptiveThresholdNode
from .bilateral_filter_node import BilateralFilterNode
from .blur_node import BlurNode
from .canny_node import CannyNode
from .cvt_color_node import CvtColorNode
from .dilate_node import DilateNode
from .erode_node import ErodeNode
from .find_contours_node import FindContoursNode
from .gaussian_blur_node import GaussianBlurNode
from .get_rotation_matrix_2d_node import GetRotationMatrix2DNode
from .get_structuring_element_node import GetStructuringElementNode
from .median_blur_node import MedianBlurNode
from .morphology_ex_node import MorphologyExNode
from .resize_node import ResizeNode
from .threshold_node import ThresholdNode
from .warp_affine_node import WarpAffineNode


def get_imgproc_nodes() -> List[Node]:
    """Get all image processing OpenCV nodes."""
    return [
        AdaptiveThresholdNode(),
        BilateralFilterNode(),
        BlurNode(),
        CannyNode(),
        CvtColorNode(),
        DilateNode(),
        ErodeNode(),
        FindContoursNode(),
        GaussianBlurNode(),
        GetRotationMatrix2DNode(),
        GetStructuringElementNode(),
        MedianBlurNode(),
        MorphologyExNode(),
        ResizeNode(),
        ThresholdNode(),
        WarpAffineNode(),
    ]
