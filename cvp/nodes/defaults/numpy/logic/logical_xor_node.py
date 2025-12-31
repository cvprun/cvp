# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class LogicalXorNode(NumpyBinaryNode):
    """Compute the truth value of x1 XOR x2, element-wise."""

    def __init__(self):
        super().__init__(
            "logical_xor", "x1", "First input array", "x2", "Second input array"
        )


# Comparison
