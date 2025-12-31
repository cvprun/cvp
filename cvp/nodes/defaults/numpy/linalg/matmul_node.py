# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class MatmulNode(NumpyBinaryNode):
    """Matrix product of two arrays."""

    def __init__(self):
        super().__init__(
            "matmul", "x1", "First input array", "x2", "Second input array"
        )
