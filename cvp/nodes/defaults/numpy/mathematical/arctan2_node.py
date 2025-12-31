# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class Arctan2Node(NumpyBinaryNode):
    """Element-wise arc tangent of x1/x2."""

    def __init__(self):
        super().__init__("arctan2", "x1", "y-coordinates", "x2", "x-coordinates")


# Hyperbolic functions
