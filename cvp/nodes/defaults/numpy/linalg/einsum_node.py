# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class EinsumNode(NumpyFunctionNode):
    """Evaluates the Einstein summation convention on the operands."""

    def __init__(self):
        subscripts_pin = DataInputPin(
            name=PinName("subscripts"),
            dtype=Dtype.any(),
            docs="Specifies the subscripts for summation",
        )
        operands_pin = DataInputPin(
            name=PinName("operands"),
            dtype=Dtype.any(),
            docs="Arrays for the operation",
        )
        super().__init__("einsum", subscripts_pin, operands_pin)

    def apply_function(self, subscripts, operands, **kwargs) -> Any:
        if isinstance(operands, (list, tuple)):
            return np.einsum(subscripts, *operands)
        else:
            return np.einsum(subscripts, operands)


# Linear algebra functions from np.linalg
