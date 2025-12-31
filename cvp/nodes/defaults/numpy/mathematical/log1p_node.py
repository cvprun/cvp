# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class Log1pNode(NumpyUnaryNode):
    """Return the natural logarithm of one plus the input array."""

    def __init__(self):
        super().__init__("log1p", "x", "Input array")
