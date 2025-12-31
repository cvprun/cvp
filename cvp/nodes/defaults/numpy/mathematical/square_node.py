# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class SquareNode(NumpyUnaryNode):
    """Return the element-wise square of the input."""

    def __init__(self):
        super().__init__("square", "x", "Input array")
