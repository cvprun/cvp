# -*- coding: utf-8 -*-


from cvp.nodes.defaults.numpy._base import NumpyUnaryNode


class IscomplexNode(NumpyUnaryNode):
    """Returns a bool array, where True if input element is complex."""

    def __init__(self):
        super().__init__("iscomplex", "x", "Input array")
