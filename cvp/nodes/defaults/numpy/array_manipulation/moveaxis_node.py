# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class MoveaxisNode(NumpyFunctionNode):
    """Move axes of an array to new positions."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        source_pin = DataInputPin(
            name=PinName("source"),
            dtype=Dtype.any(),
            docs="Original positions of the axes to move",
        )
        destination_pin = DataInputPin(
            name=PinName("destination"),
            dtype=Dtype.any(),
            docs="Destination positions for each of the original axes",
        )
        super().__init__("moveaxis", array_pin, source_pin, destination_pin)

    def apply_function(self, a, source, destination, **kwargs) -> Any:
        return np.moveaxis(a, source, destination)
