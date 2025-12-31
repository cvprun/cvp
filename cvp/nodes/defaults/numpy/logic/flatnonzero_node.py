# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class FlatnonzeroNode(NumpyUnaryNode):
    """Return indices that are non-zero in the flattened version of a."""

    def __init__(self):
        super().__init__("flatnonzero", "a", "Input array")
