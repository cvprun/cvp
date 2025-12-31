# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class MinimumNode(NumpyBinaryNode):
    """Element-wise minimum of array elements."""

    def __init__(self):
        super().__init__(
            "minimum", "x1", "First input array", "x2", "Second input array"
        )
