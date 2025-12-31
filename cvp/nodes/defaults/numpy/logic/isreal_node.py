# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class IsrealNode(NumpyUnaryNode):
    """Returns a bool array, where True if input element is real."""

    def __init__(self):
        super().__init__("isreal", "x", "Input array")
