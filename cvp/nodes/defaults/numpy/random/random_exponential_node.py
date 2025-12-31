# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomExponentialNode(NumpyFunctionNode):
    """Draw samples from an exponential distribution."""

    def __init__(self):
        scale_pin = DataInputPin(
            name=PinName("scale"),
            dtype=Dtype.any(),
            docs="Scale parameter (inverse of the rate parameter lambda)",
            default=1.0,
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("exponential", scale_pin, size_pin)

    def apply_function(self, scale, size, **kwargs) -> Any:
        return np.random.exponential(scale=scale, size=size)
