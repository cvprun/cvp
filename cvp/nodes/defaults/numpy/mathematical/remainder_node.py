# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class RemainderNode(NumpyBinaryNode):
    """Return element-wise remainder of division."""

    def __init__(self):
        super().__init__("remainder", "x1", "Dividend array", "x2", "Divisor array")


# Rounding
