# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class FliplrNode(NumpyUnaryNode):
    """Flip array in the left/right direction."""

    def __init__(self):
        super().__init__("fliplr", "m", "Input array")
