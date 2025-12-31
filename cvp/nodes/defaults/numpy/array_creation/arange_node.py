# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class ArangeNode(NumpyFunctionNode):
    """Create evenly spaced values within a given interval."""

    def __init__(self):
        start_pin = DataInputPin(
            name=PinName("start"),
            dtype=Dtype.any(),
            docs="Start of interval",
            default=0,
        )
        stop_pin = DataInputPin(
            name=PinName("stop"),
            dtype=Dtype.any(),
            docs="End of interval (not included)",
        )
        step_pin = DataInputPin(
            name=PinName("step"),
            dtype=Dtype.any(),
            docs="Spacing between values",
            default=1,
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=None,
        )
        super().__init__("arange", start_pin, stop_pin, step_pin, dtype_pin)

    def apply_function(self, start, stop, step, dtype, **kwargs) -> Any:
        if dtype is None:
            return np.arange(start, stop, step)
        return np.arange(start, stop, step, dtype=dtype)
