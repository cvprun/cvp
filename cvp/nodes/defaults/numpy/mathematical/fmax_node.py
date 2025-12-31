# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class FmaxNode(NumpyBinaryNode):
    """Element-wise maximum, ignores NaNs."""

    def __init__(self):
        super().__init__("fmax", "x1", "First input array", "x2", "Second input array")
