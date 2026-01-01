# -*- coding: utf-8 -*-

from cvp.nodes.defaults.opencv._base import OpenCVUnaryNode


class BoundingRectNode(OpenCVUnaryNode):
    """Calculate bounding rectangle of contour."""

    def __init__(self):
        super().__init__(
            "boundingRect",
            input_name="array",
            input_docs="Input contour points",
        )
