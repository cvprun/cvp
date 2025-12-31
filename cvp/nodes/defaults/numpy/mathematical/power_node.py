# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyBinaryNode


class PowerNode(NumpyBinaryNode):
    """First array elements raised to powers from second array."""

    def __init__(self):
        super().__init__("power", "x1", "Base array", "x2", "Exponents array")
