# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class IdentityNode(NumpyFunctionNode):
    """Create identity matrix."""

    def __init__(self):
        n_pin = DataInputPin(
            name=PinName("n"),
            dtype=Dtype.any(),
            docs="Number of rows (and columns)",
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=float,
        )
        super().__init__("identity", n_pin, dtype_pin)

    def apply_function(self, n, dtype, **kwargs) -> Any:
        return np.identity(n, dtype=dtype)
