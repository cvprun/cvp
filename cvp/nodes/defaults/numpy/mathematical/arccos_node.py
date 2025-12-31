# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class ArccosNode(NumpyUnaryNode):
    """Inverse cosine."""

    def __init__(self):
        super().__init__("arccos", "x", "Input array")
