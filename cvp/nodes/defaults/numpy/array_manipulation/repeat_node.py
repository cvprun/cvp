# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RepeatNode(NumpyFunctionNode):
    """Repeat elements of an array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        repeats_pin = DataInputPin(
            name=PinName("repeats"),
            dtype=Dtype.any(),
            docs="Number of repetitions for each element",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to repeat values",
            default=None,
        )
        super().__init__("repeat", array_pin, repeats_pin, axis_pin)

    def apply_function(self, a, repeats, axis, **kwargs) -> Any:
        return np.repeat(a, repeats, axis=axis)
