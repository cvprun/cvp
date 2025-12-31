# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomUniformNode(NumpyFunctionNode):
    """Draw samples from a uniform distribution."""

    def __init__(self):
        low_pin = DataInputPin(
            name=PinName("low"),
            dtype=Dtype.any(),
            docs="Lower boundary of the output interval",
            default=0.0,
        )
        high_pin = DataInputPin(
            name=PinName("high"),
            dtype=Dtype.any(),
            docs="Upper boundary of the output interval",
            default=1.0,
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("uniform", low_pin, high_pin, size_pin)

    def apply_function(self, low, high, size, **kwargs) -> Any:
        return np.random.uniform(low=low, high=high, size=size)
