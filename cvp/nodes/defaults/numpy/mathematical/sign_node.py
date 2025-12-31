# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class SignNode(NumpyUnaryNode):
    """Returns element-wise indication of the sign of a number."""

    def __init__(self):
        super().__init__("sign", "x", "Input array")
