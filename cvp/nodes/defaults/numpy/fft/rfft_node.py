# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RfftNode(NumpyFunctionNode):
    """Compute the one-dimensional discrete Fourier Transform for real input."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        n_pin = DataInputPin(
            name=PinName("n"),
            dtype=Dtype.any(),
            docs="Number of points along transformation axis",
            default=None,
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis over which to compute the FFT",
            default=-1,
        )
        super().__init__("rfft", array_pin, n_pin, axis_pin)

    def apply_function(self, a, n, axis, **kwargs) -> Any:
        return np.fft.rfft(a, n=n, axis=axis)
