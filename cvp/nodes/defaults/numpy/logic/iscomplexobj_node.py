# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class IscomplexobjNode(NumpyUnaryNode):
    """Check for a complex type or an array of complex numbers."""

    def __init__(self):
        super().__init__("iscomplexobj", "x", "Input array")
