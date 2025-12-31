# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class ReshapeNode(NumpyFunctionNode):
    """Give a new shape to an array without changing its data."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Array to be reshaped",
        )
        newshape_pin = DataInputPin(
            name=PinName("newshape"),
            dtype=Dtype.any(),
            docs="The new shape should be compatible with the original shape",
        )
        super().__init__("reshape", array_pin, newshape_pin)

    def apply_function(self, a, newshape, **kwargs) -> Any:
        return np.reshape(a, newshape)
