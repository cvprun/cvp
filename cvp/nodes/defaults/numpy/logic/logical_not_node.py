# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class LogicalNotNode(NumpyUnaryNode):
    """Compute the truth value of NOT x element-wise."""

    def __init__(self):
        super().__init__("logical_not", "x", "Input array")
