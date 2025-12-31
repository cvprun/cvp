# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class VdotNode(NumpyBinaryNode):
    """Return the dot product of two vectors."""

    def __init__(self):
        super().__init__("vdot", "a", "First input array", "b", "Second input array")
