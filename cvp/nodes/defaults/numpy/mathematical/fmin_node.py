# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class FminNode(NumpyBinaryNode):
    """Element-wise minimum, ignores NaNs."""

    def __init__(self):
        super().__init__("fmin", "x1", "First input array", "x2", "Second input array")
