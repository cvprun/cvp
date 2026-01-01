# -*- coding: utf-8 -*-

from cvp.nodes.defaults.opencv._base import OpenCVUnaryNode


class ContourAreaNode(OpenCVUnaryNode):
    """Calculate contour area."""

    def __init__(self):
        super().__init__(
            "contourArea",
            input_name="contour",
            input_docs="Input contour",
        )
