# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class ModNode(NumpyBinaryNode):
    """Return element-wise remainder of division."""

    def __init__(self):
        super().__init__("mod", "x1", "Dividend array", "x2", "Divisor array")
