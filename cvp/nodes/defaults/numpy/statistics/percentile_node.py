# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class PercentileNode(NumpyFunctionNode):
    """Compute the qth percentile of the data along the specified axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        q_pin = DataInputPin(
            name=PinName("q"),
            dtype=Dtype.any(),
            docs="Percentile or sequence of percentiles to compute",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which the percentiles are computed",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("percentile", array_pin, q_pin, axis_pin, keepdims_pin)

    def apply_function(self, a, q, axis, keepdims, **kwargs) -> Any:
        return np.percentile(a, q, axis=axis, keepdims=keepdims)
