# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class TanNode(NumpyUnaryNode):
    """Trigonometric tangent."""

    def __init__(self):
        super().__init__("tan", "x", "Input array in radians")
