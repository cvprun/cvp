# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class SinNode(NumpyUnaryNode):
    """Trigonometric sine."""

    def __init__(self):
        super().__init__("sin", "x", "Input array in radians")
