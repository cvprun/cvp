# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class SqrtNode(NumpyUnaryNode):
    """Return the positive square-root of an array."""

    def __init__(self):
        super().__init__("sqrt", "x", "Input array")
