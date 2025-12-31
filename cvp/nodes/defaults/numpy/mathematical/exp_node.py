# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class ExpNode(NumpyUnaryNode):
    """Calculate the exponential of all elements."""

    def __init__(self):
        super().__init__("exp", "x", "Input array")
