# -*- coding: utf-8 -*-

from cvp.nodes.defaults.opencv._base import OpenCVUnaryNode


class HConcatNode(OpenCVUnaryNode):
    """Concatenate images horizontally."""

    def __init__(self):
        super().__init__(
            "hconcat",
            input_name="src",
            input_docs="List of images to concatenate horizontally",
        )
