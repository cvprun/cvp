# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class TruncNode(NumpyUnaryNode):
    """Return the truncated value of the input."""

    def __init__(self):
        super().__init__("trunc", "x", "Input array")


# Other mathematical functions
