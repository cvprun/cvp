# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class PositiveNode(NumpyUnaryNode):
    """Numerical positive, element-wise."""

    def __init__(self):
        super().__init__("positive", "x", "Input array")
