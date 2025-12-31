# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class TransposeNode(NumpyUnaryNode):
    """Reverse or permute the axes of an array."""

    def __init__(self):
        super().__init__("transpose", "a", "Input array")
