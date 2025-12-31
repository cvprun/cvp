# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class FloorDivideNode(NumpyBinaryNode):
    """Return the largest integer smaller or equal to the division."""

    def __init__(self):
        super().__init__("floor_divide", "x1", "Dividend array", "x2", "Divisor array")
