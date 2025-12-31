# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class FftfreqNode(NumpyFunctionNode):
    """Return the Discrete Fourier Transform sample frequencies."""

    def __init__(self):
        n_pin = DataInputPin(
            name=PinName("n"),
            dtype=Dtype.any(),
            docs="Window length",
        )
        d_pin = DataInputPin(
            name=PinName("d"),
            dtype=Dtype.any(),
            docs="Sample spacing",
            default=1.0,
        )
        super().__init__("fftfreq", n_pin, d_pin)

    def apply_function(self, n, d, **kwargs) -> Any:
        return np.fft.fftfreq(n, d=d)
