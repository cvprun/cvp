# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class ReciprocalNode(NumpyUnaryNode):
    """Return the reciprocal of the argument."""

    def __init__(self):
        super().__init__("reciprocal", "x", "Input array")
