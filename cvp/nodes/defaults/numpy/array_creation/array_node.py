# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class ArrayNode(NumpyFunctionNode):
    """Create an array from a list or tuple."""

    def __init__(self):
        input_pin = DataInputPin(
            name=PinName("object"),
            dtype=Dtype.any(),
            docs="Array-like object to convert to array",
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=None,
        )
        super().__init__("array", input_pin, dtype_pin)

    def apply_function(self, obj, dtype, **kwargs) -> Any:
        if dtype is None:
            return np.array(obj)
        return np.array(obj, dtype=dtype)
