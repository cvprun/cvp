# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class Expm1Node(NumpyUnaryNode):
    """Calculate exp(x) - 1 for all elements."""

    def __init__(self):
        super().__init__("expm1", "x", "Input array")


# Arithmetic operations
