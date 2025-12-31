# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class ConcatenateNode(NumpyFunctionNode):
    """Join a sequence of arrays along an existing axis."""

    def __init__(self):
        arrays_pin = DataInputPin(
            name=PinName("arrays"),
            dtype=Dtype.any(),
            docs="Sequence of arrays",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which the arrays will be joined",
            default=0,
        )
        super().__init__("concatenate", arrays_pin, axis_pin)

    def apply_function(self, arrays, axis, **kwargs) -> Any:
        return np.concatenate(arrays, axis=axis)
