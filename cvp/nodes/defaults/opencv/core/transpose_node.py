# -*- coding: utf-8 -*-

from cvp.nodes.defaults.opencv._base import OpenCVUnaryNode


class TransposeNode(OpenCVUnaryNode):
    """Transpose image (swap rows and columns)."""

    def __init__(self):
        super().__init__(
            "transpose",
            input_name="src",
            input_docs="Source image to transpose",
        )
