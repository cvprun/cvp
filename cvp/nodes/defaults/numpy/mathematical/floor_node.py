# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class FloorNode(NumpyUnaryNode):
    """Return the floor of the input."""

    def __init__(self):
        super().__init__("floor", "x", "Input array")
