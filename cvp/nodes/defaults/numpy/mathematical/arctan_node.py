# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class ArctanNode(NumpyUnaryNode):
    """Inverse tangent."""

    def __init__(self):
        super().__init__("arctan", "x", "Input array")
