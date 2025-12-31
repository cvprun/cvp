# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class FlipudNode(NumpyUnaryNode):
    """Flip array in the up/down direction."""

    def __init__(self):
        super().__init__("flipud", "m", "Input array")
