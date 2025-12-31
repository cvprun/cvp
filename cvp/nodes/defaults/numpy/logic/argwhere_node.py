# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class ArgwhereNode(NumpyUnaryNode):
    """Find the indices of array elements that are non-zero, grouped by element."""

    def __init__(self):
        super().__init__("argwhere", "a", "Input array")


# Type testing
