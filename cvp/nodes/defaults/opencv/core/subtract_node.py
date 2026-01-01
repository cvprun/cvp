# -*- coding: utf-8 -*-

from cvp.nodes.defaults.opencv._base import OpenCVBinaryNode


class SubtractNode(OpenCVBinaryNode):
    """Subtract second image from first image element-wise."""

    def __init__(self):
        super().__init__(
            "subtract",
            first_name="src1",
            first_docs="First source image",
            second_name="src2",
            second_docs="Second source image",
        )
