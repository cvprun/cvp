# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class HistogramNode(NumpyFunctionNode):
    """Compute the histogram of a dataset."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input data",
        )
        bins_pin = DataInputPin(
            name=PinName("bins"),
            dtype=Dtype.any(),
            docs="Number of equal-width bins or bin edges",
            default=10,
        )
        range_pin = DataInputPin(
            name=PinName("range"),
            dtype=Dtype.any(),
            docs="Lower and upper range of the bins",
            default=None,
        )
        density_pin = DataInputPin(
            name=PinName("density"),
            dtype=Dtype.any(),
            docs="If True, draw a density instead of a frequency histogram",
            default=False,
        )
        super().__init__("histogram", array_pin, bins_pin, range_pin, density_pin)

    def apply_function(self, a, bins, range, density, **kwargs) -> Any:
        return np.histogram(a, bins=bins, range=range, density=density)
