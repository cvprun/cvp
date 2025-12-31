# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class OnesNode(NumpyFunctionNode):
    """Create array filled with ones."""

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
        super().__init__("ones", shape_pin, dtype_pin)

    def apply_function(self, shape, dtype, **kwargs) -> Any:
        return np.ones(shape, dtype=dtype)
