# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class ArccoshNode(NumpyUnaryNode):
    """Inverse hyperbolic cosine."""

    def __init__(self):
        super().__init__("arccosh", "x", "Input array")
