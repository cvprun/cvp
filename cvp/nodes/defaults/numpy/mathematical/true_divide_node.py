# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class TrueDivideNode(NumpyBinaryNode):
    """True division of the inputs, element-wise."""

    def __init__(self):
        super().__init__("true_divide", "x1", "Dividend array", "x2", "Divisor array")
