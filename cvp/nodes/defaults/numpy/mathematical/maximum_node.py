# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class MaximumNode(NumpyBinaryNode):
    """Element-wise maximum of array elements."""

    def __init__(self):
        super().__init__(
            "maximum", "x1", "First input array", "x2", "Second input array"
        )
