# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .approx_poly_dp_node import ApproxPolyDPNode
from .arc_length_node import ArcLengthNode
from .bounding_rect_node import BoundingRectNode
from .contour_area_node import ContourAreaNode
from .draw_contours_node import DrawContoursNode
from .hough_circles_node import HoughCirclesNode
from .hough_lines_node import HoughLinesNode
from .hough_lines_p_node import HoughLinesPNode
from .min_area_rect_node import MinAreaRectNode


def get_objdetect_nodes() -> List[Node]:
    """Get all object detection OpenCV nodes."""
    return [
        ApproxPolyDPNode(),
        ArcLengthNode(),
        BoundingRectNode(),
        ContourAreaNode(),
        DrawContoursNode(),
        HoughCirclesNode(),
        HoughLinesNode(),
        HoughLinesPNode(),
        MinAreaRectNode(),
    ]
