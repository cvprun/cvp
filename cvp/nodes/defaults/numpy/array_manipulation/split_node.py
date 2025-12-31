# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class SplitNode(NumpyFunctionNode):
    """Split an array into multiple sub-arrays as views into array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("ary"),
            dtype=Dtype.any(),
            docs="Array to be divided into sub-arrays",
        )
        indices_pin = DataInputPin(
            name=PinName("indices_or_sections"),
            dtype=Dtype.any(),
            docs="If integer, number of equal sections",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to split",
            default=0,
        )
        super().__init__("split", array_pin, indices_pin, axis_pin)

    def apply_function(self, ary, indices_or_sections, axis, **kwargs) -> Any:
        return np.split(ary, indices_or_sections, axis=axis)
