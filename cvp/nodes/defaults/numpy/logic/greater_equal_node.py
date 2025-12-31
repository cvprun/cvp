# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class GreaterEqualNode(NumpyBinaryNode):
    """Return the truth value of (x1 >= x2) element-wise."""

    def __init__(self):
        super().__init__(
            "greater_equal", "x1", "First input array", "x2", "Second input array"
        )
