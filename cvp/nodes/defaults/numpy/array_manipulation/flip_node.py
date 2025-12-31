# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class FlipNode(NumpyFunctionNode):
    """Reverse the order of elements in an array along the given axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("m"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis or axes along which to flip over",
            default=None,
        )
        super().__init__("flip", array_pin, axis_pin)

    def apply_function(self, m, axis, **kwargs) -> Any:
        return np.flip(m, axis=axis)
