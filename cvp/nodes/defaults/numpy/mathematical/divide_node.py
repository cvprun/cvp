# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class DivideNode(NumpyBinaryNode):
    """Divide arguments element-wise."""

    def __init__(self):
        super().__init__("divide", "x1", "Dividend array", "x2", "Divisor array")
