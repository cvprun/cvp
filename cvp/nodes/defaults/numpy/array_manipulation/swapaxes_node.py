# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class SwapaxesNode(NumpyFunctionNode):
    """Interchange two axes of an array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis1_pin = DataInputPin(
            name=PinName("axis1"),
            dtype=Dtype.any(),
            docs="First axis",
        )
        axis2_pin = DataInputPin(
            name=PinName("axis2"),
            dtype=Dtype.any(),
            docs="Second axis",
        )
        super().__init__("swapaxes", array_pin, axis1_pin, axis2_pin)

    def apply_function(self, a, axis1, axis2, **kwargs) -> Any:
        return np.swapaxes(a, axis1, axis2)
