# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class CoshNode(NumpyUnaryNode):
    """Hyperbolic cosine."""

    def __init__(self):
        super().__init__("cosh", "x", "Input array")
