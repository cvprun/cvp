# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class ExpandDimsNode(NumpyFunctionNode):
    """Expand the shape of an array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Position in the expanded axes where the new axis is placed",
        )
        super().__init__("expand_dims", array_pin, axis_pin)

    def apply_function(self, a, axis, **kwargs) -> Any:
        return np.expand_dims(a, axis=axis)
