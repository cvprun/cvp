# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class SinhNode(NumpyUnaryNode):
    """Hyperbolic sine."""

    def __init__(self):
        super().__init__("sinh", "x", "Input array")
