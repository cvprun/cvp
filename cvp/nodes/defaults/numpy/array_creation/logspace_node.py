# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class LogspaceNode(NumpyFunctionNode):
    """Create numbers spaced evenly on a log scale."""

    def __init__(self):
        start_pin = DataInputPin(
            name=PinName("start"),
            dtype=Dtype.any(),
            docs="Start exponent",
        )
        stop_pin = DataInputPin(
            name=PinName("stop"),
            dtype=Dtype.any(),
            docs="End exponent",
        )
        num_pin = DataInputPin(
            name=PinName("num"),
            dtype=Dtype.any(),
            docs="Number of samples",
            default=50,
        )
        base_pin = DataInputPin(
            name=PinName("base"),
            dtype=Dtype.any(),
            docs="Base of the log scale",
            default=10.0,
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=None,
        )
        super().__init__("logspace", start_pin, stop_pin, num_pin, base_pin, dtype_pin)

    def apply_function(self, start, stop, num, base, dtype, **kwargs) -> Any:
        return np.logspace(start, stop, num=num, base=base, dtype=dtype)
