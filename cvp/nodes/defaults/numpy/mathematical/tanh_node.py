# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class TanhNode(NumpyUnaryNode):
    """Hyperbolic tangent."""

    def __init__(self):
        super().__init__("tanh", "x", "Input array")
