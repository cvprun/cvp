# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class IsnanNode(NumpyUnaryNode):
    """Test for NaN element-wise."""

    def __init__(self):
        super().__init__("isnan", "x", "Input array")
