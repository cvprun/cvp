# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class ZerosNode(NumpyFunctionNode):
    """Create array filled with zeros."""

    def __init__(self):
        shape_pin = DataInputPin(
            name=PinName("shape"),
            dtype=Dtype.any(),
            docs="Shape of the array",
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=float,
        )
        super().__init__("zeros", shape_pin, dtype_pin)

    def apply_function(self, shape, dtype, **kwargs) -> Any:
        return np.zeros(shape, dtype=dtype)
