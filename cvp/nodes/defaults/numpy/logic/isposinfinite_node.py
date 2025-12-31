# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class IsposinfiniteNode(NumpyUnaryNode):
    """Test for positive infinity."""

    def __init__(self):
        super().__init__("isposinf", "x", "Input array")


# Logical operations
