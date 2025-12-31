# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class CeilNode(NumpyUnaryNode):
    """Return the ceiling of the input."""

    def __init__(self):
        super().__init__("ceil", "x", "Input array")
