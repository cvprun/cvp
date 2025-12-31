# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class Irfft2Node(NumpyFunctionNode):
    """Compute the 2-dimensional inverse FFT of a real array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        s_pin = DataInputPin(
            name=PinName("s"),
            dtype=Dtype.any(),
            docs="Shape of the input",
            default=None,
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes over which to compute the inverse FFT",
            default=(-2, -1),
        )
        super().__init__("irfft2", array_pin, s_pin, axes_pin)

    def apply_function(self, a, s, axes, **kwargs) -> Any:
        return np.fft.irfft2(a, s=s, axes=axes)
