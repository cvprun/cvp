# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class SqueezeNode(NumpyFunctionNode):
    """Remove single-dimensional entries from the shape of an array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Selects a subset of the single-dimensional entries",
            default=None,
        )
        super().__init__("squeeze", array_pin, axis_pin)

    def apply_function(self, a, axis, **kwargs) -> Any:
        return np.squeeze(a, axis=axis)
