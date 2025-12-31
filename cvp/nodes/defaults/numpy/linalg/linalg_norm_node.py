# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class LinalgNormNode(NumpyFunctionNode):
    """Matrix or vector norm."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        ord_pin = DataInputPin(
            name=PinName("ord"),
            dtype=Dtype.any(),
            docs="Order of the norm",
            default=None,
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to compute the norm",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep dimensions",
            default=False,
        )
        super().__init__("norm", array_pin, ord_pin, axis_pin, keepdims_pin)

    def apply_function(self, x, ord, axis, keepdims, **kwargs) -> Any:
        return np.linalg.norm(x, ord=ord, axis=axis, keepdims=keepdims)
