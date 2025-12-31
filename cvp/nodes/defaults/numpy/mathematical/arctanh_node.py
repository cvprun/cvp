# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class ArctanhNode(NumpyUnaryNode):
    """Inverse hyperbolic tangent."""

    def __init__(self):
        super().__init__("arctanh", "x", "Input array")


# Exponential and logarithmic functions
