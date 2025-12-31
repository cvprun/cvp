# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class FabsNode(NumpyUnaryNode):
    """Compute the absolute values element-wise."""

    def __init__(self):
        super().__init__("fabs", "x", "Input array")
