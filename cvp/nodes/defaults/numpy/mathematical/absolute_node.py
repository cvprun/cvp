# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class AbsoluteNode(NumpyUnaryNode):
    """Calculate the absolute value element-wise."""

    def __init__(self):
        super().__init__("absolute", "x", "Input array")
