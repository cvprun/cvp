# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class VarNode(NumpyFunctionNode):
    """Compute the variance along the specified axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Array containing numbers whose variance is desired",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which the variance is computed",
            default=None,
        )
        ddof_pin = DataInputPin(
            name=PinName("ddof"),
            dtype=Dtype.any(),
            docs="Delta degrees of freedom",
            default=0,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("var", array_pin, axis_pin, ddof_pin, keepdims_pin)

    def apply_function(self, a, axis, ddof, keepdims, **kwargs) -> Any:
        return np.var(a, axis=axis, ddof=ddof, keepdims=keepdims)
