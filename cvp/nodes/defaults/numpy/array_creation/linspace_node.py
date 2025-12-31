# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class LinspaceNode(NumpyFunctionNode):
    """Create evenly spaced numbers over a specified interval."""

    def __init__(self):
        start_pin = DataInputPin(
            name=PinName("start"),
            dtype=Dtype.any(),
            docs="Start of sequence",
        )
        stop_pin = DataInputPin(
            name=PinName("stop"),
            dtype=Dtype.any(),
            docs="End of sequence",
        )
        num_pin = DataInputPin(
            name=PinName("num"),
            dtype=Dtype.any(),
            docs="Number of samples",
            default=50,
        )
        endpoint_pin = DataInputPin(
            name=PinName("endpoint"),
            dtype=Dtype.any(),
            docs="Include endpoint",
            default=True,
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=None,
        )
        super().__init__(
            "linspace", start_pin, stop_pin, num_pin, endpoint_pin, dtype_pin
        )

    def apply_function(self, start, stop, num, endpoint, dtype, **kwargs) -> Any:
        return np.linspace(start, stop, num=num, endpoint=endpoint, dtype=dtype)
