# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class ArcsinNode(NumpyUnaryNode):
    """Inverse sine."""

    def __init__(self):
        super().__init__("arcsin", "x", "Input array")
