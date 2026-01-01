# -*- coding: utf-8 -*-

from cvp.nodes.defaults.opencv._base import OpenCVUnaryNode


class MinAreaRectNode(OpenCVUnaryNode):
    """Calculate minimum area rectangle enclosing contour."""

    def __init__(self):
        super().__init__(
            "minAreaRect",
            input_name="points",
            input_docs="Input contour points",
        )
