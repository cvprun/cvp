# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class IsfiniteNode(NumpyUnaryNode):
    """Test finiteness element-wise."""

    def __init__(self):
        super().__init__("isfinite", "x", "Input array")
