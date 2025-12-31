# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class IsnatNode(NumpyUnaryNode):
    """Test for NaT (not a time) element-wise."""

    def __init__(self):
        super().__init__("isnat", "x", "Input array")
