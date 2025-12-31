# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class TensordotNode(NumpyFunctionNode):
    """Compute tensor dot product along specified axes."""

    def __init__(self):
        a_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="First input array",
        )
        b_pin = DataInputPin(
            name=PinName("b"),
            dtype=Dtype.any(),
            docs="Second input array",
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes to be summed over",
            default=2,
        )
        super().__init__("tensordot", a_pin, b_pin, axes_pin)

    def apply_function(self, a, b, axes, **kwargs) -> Any:
        return np.tensordot(a, b, axes=axes)
