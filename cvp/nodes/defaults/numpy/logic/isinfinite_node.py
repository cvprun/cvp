# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class IsinfiniteNode(NumpyUnaryNode):
    """Test for positive or negative infinity."""

    def __init__(self):
        super().__init__("isinf", "x", "Input array")
