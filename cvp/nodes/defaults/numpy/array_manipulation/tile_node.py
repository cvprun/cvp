# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class TileNode(NumpyFunctionNode):
    """Construct an array by repeating A the number of times given by reps."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("A"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        reps_pin = DataInputPin(
            name=PinName("reps"),
            dtype=Dtype.any(),
            docs="Number of repetitions along each axis",
        )
        super().__init__("tile", array_pin, reps_pin)

    def apply_function(self, A, reps, **kwargs) -> Any:
        return np.tile(A, reps)
