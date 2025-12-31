# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class IsneginfiniteNode(NumpyUnaryNode):
    """Test for negative infinity."""

    def __init__(self):
        super().__init__("isneginf", "x", "Input array")
