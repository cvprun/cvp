# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class BincountNode(NumpyFunctionNode):
    """Count number of occurrences of each value in array of non-negative ints."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        weights_pin = DataInputPin(
            name=PinName("weights"),
            dtype=Dtype.any(),
            docs="Weights, array of the same shape as x",
            default=None,
        )
        minlength_pin = DataInputPin(
            name=PinName("minlength"),
            dtype=Dtype.any(),
            docs="Minimum number of bins for the output array",
            default=0,
        )
        super().__init__("bincount", array_pin, weights_pin, minlength_pin)

    def apply_function(self, x, weights, minlength, **kwargs) -> Any:
        return np.bincount(x, weights=weights, minlength=minlength)
