# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class NotEqualNode(NumpyBinaryNode):
    """Return (x1 != x2) element-wise."""

    def __init__(self):
        super().__init__(
            "not_equal", "x1", "First input array", "x2", "Second input array"
        )


# Selection
