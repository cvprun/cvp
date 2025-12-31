# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class GreaterNode(NumpyBinaryNode):
    """Return the truth value of (x1 > x2) element-wise."""

    def __init__(self):
        super().__init__(
            "greater", "x1", "First input array", "x2", "Second input array"
        )
