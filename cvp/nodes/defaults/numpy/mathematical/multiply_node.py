# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class MultiplyNode(NumpyBinaryNode):
    """Multiply arguments element-wise."""

    def __init__(self):
        super().__init__(
            "multiply", "x1", "First input array", "x2", "Second input array"
        )
