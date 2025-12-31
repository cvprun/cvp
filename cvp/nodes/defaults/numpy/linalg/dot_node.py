# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class DotNode(NumpyBinaryNode):
    """Dot product of two arrays."""

    def __init__(self):
        super().__init__("dot", "a", "First input array", "b", "Second input array")
