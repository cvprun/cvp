# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class ArcsinhNode(NumpyUnaryNode):
    """Inverse hyperbolic sine."""

    def __init__(self):
        super().__init__("arcsinh", "x", "Input array")
