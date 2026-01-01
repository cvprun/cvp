# -*- coding: utf-8 -*-

from cvp.nodes.defaults.opencv._base import OpenCVBinaryNode


class BitwiseXorNode(OpenCVBinaryNode):
    """Bitwise XOR operation between two images."""

    def __init__(self):
        super().__init__(
            "bitwise_xor",
            first_name="src1",
            first_docs="First source image",
            second_name="src2",
            second_docs="Second source image",
        )
