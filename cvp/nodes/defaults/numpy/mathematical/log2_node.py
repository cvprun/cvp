# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class Log2Node(NumpyUnaryNode):
    """Base-2 logarithm."""

    def __init__(self):
        super().__init__("log2", "x", "Input array")
