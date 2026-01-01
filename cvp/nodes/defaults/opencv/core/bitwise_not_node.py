# -*- coding: utf-8 -*-

from cvp.nodes.defaults.opencv._base import OpenCVUnaryNode


class BitwiseNotNode(OpenCVUnaryNode):
    """Bitwise NOT operation on an image."""

    def __init__(self):
        super().__init__(
            "bitwise_not",
            input_name="src",
            input_docs="Source image for bitwise NOT operation",
        )
