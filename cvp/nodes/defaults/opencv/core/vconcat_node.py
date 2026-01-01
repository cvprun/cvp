# -*- coding: utf-8 -*-

from cvp.nodes.defaults.opencv._base import OpenCVUnaryNode


class VConcatNode(OpenCVUnaryNode):
    """Concatenate images vertically."""

    def __init__(self):
        super().__init__(
            "vconcat",
            input_name="src",
            input_docs="List of images to concatenate vertically",
        )
