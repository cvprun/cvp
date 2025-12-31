# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class EyeNode(NumpyFunctionNode):
    """Create 2-D array with ones on diagonal and zeros elsewhere."""

    def __init__(self):
        n_pin = DataInputPin(
            name=PinName("N"),
            dtype=Dtype.any(),
            docs="Number of rows (and columns)",
        )
        m_pin = DataInputPin(
            name=PinName("M"),
            dtype=Dtype.any(),
            docs="Number of columns (optional)",
            default=None,
        )
        k_pin = DataInputPin(
            name=PinName("k"),
            dtype=Dtype.any(),
            docs="Index of the diagonal",
            default=0,
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=float,
        )
        super().__init__("eye", n_pin, m_pin, k_pin, dtype_pin)

    def apply_function(self, n, m, k, dtype, **kwargs) -> Any:
        return np.eye(n, M=m, k=k, dtype=dtype)
