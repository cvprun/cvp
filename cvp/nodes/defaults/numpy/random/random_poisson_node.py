# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomPoissonNode(NumpyFunctionNode):
    """Draw samples from a Poisson distribution."""

    def __init__(self):
        lam_pin = DataInputPin(
            name=PinName("lam"),
            dtype=Dtype.any(),
            docs="Expected number of events occurring in a fixed-time interval",
            default=1.0,
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("poisson", lam_pin, size_pin)

    def apply_function(self, lam, size, **kwargs) -> Any:
        return np.random.poisson(lam=lam, size=size)
