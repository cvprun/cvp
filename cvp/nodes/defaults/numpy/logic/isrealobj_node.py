# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class IsrealobjNode(NumpyUnaryNode):
    """Return True if x is a not complex type or an array of complex numbers."""

    def __init__(self):
        super().__init__("isrealobj", "x", "Input array")
