# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class LogNode(NumpyUnaryNode):
    """Natural logarithm."""

    def __init__(self):
        super().__init__("log", "x", "Input array")
