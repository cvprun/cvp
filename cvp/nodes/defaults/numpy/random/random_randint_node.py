# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomRandintNode(NumpyFunctionNode):
    """Return random integers from low (inclusive) to high (exclusive)."""

    def __init__(self):
        low_pin = DataInputPin(
            name=PinName("low"),
            dtype=Dtype.any(),
            docs="Lowest (signed) integer to be drawn",
        )
        high_pin = DataInputPin(
            name=PinName("high"),
            dtype=Dtype.any(),
            docs="Highest (signed) integer to be drawn",
            default=None,
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("randint", low_pin, high_pin, size_pin)

    def apply_function(self, low, high, size, **kwargs) -> Any:
        return np.random.randint(low, high=high, size=size)
