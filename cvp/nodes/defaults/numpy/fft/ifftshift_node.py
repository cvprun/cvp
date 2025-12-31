# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class IfftshiftNode(NumpyFunctionNode):
    """The inverse of fftshift."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes over which to calculate",
            default=None,
        )
        super().__init__("ifftshift", array_pin, axes_pin)

    def apply_function(self, x, axes, **kwargs) -> Any:
        return np.fft.ifftshift(x, axes=axes)
