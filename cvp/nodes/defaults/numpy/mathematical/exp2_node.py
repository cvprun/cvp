# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class Exp2Node(NumpyUnaryNode):
    """Calculate 2**p for all p in the input array."""

    def __init__(self):
        super().__init__("exp2", "x", "Input array")
