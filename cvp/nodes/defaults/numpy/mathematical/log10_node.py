# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class Log10Node(NumpyUnaryNode):
    """Base-10 logarithm."""

    def __init__(self):
        super().__init__("log10", "x", "Input array")
