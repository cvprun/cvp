# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class FullNode(NumpyFunctionNode):
    """Create array filled with fill_value."""

    def __init__(self):
        shape_pin = DataInputPin(
            name=PinName("shape"),
            dtype=Dtype.any(),
            docs="Shape of the array",
        )
        fill_value_pin = DataInputPin(
            name=PinName("fill_value"),
            dtype=Dtype.any(),
            docs="Fill value",
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=None,
        )
        super().__init__("full", shape_pin, fill_value_pin, dtype_pin)

    def apply_function(self, shape, fill_value, dtype, **kwargs) -> Any:
        return np.full(shape, fill_value, dtype=dtype)
