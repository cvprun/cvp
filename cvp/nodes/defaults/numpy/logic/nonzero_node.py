# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class NonzeroNode(NumpyUnaryNode):
    """Return the indices of the elements that are non-zero."""

    def __init__(self):
        super().__init__("nonzero", "a", "Input array")
