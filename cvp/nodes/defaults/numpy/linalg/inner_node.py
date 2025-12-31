# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class InnerNode(NumpyBinaryNode):
    """Inner product of two arrays."""

    def __init__(self):
        super().__init__("inner", "a", "First input array", "b", "Second input array")
