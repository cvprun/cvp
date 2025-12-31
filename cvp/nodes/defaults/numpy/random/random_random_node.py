# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomRandomNode(NumpyFunctionNode):
    """Return random floats in the half-open interval [0.0, 1.0)."""

    def __init__(self):
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("random", size_pin)

    def apply_function(self, size, **kwargs) -> Any:
        return np.random.random(size=size)
