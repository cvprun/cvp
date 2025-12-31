# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class RoundNode(NumpyUnaryNode):
    """Round elements to the nearest integer."""

    def __init__(self):
        super().__init__("round", "x", "Input array")
