# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class OuterNode(NumpyBinaryNode):
    """Compute the outer product of two vectors."""

    def __init__(self):
        super().__init__("outer", "a", "First input vector", "b", "Second input vector")
