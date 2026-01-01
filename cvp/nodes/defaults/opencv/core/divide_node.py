# -*- coding: utf-8 -*-

from cvp.nodes.defaults.opencv._base import OpenCVBinaryNode


class DivideNode(OpenCVBinaryNode):
    """Divide first image by second image element-wise."""

    def __init__(self):
        super().__init__(
            "divide",
            first_name="src1",
            first_docs="First source image",
            second_name="src2",
            second_docs="Second source image",
        )
