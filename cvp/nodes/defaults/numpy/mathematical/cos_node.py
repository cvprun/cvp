# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class CosNode(NumpyUnaryNode):
    """Trigonometric cosine."""

    def __init__(self):
        super().__init__("cos", "x", "Input array in radians")
