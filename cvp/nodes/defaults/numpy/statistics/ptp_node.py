# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class PtpNode(NumpyFunctionNode):
    """Range of values (maximum - minimum) along an axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to find the peaks",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("ptp", array_pin, axis_pin, keepdims_pin)

    def apply_function(self, a, axis, keepdims, **kwargs) -> Any:
        return np.ptp(a, axis=axis, keepdims=keepdims)
