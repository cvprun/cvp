# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomPermutationNode(NumpyFunctionNode):
    """Randomly permute a sequence, or return a permuted range."""

    def __init__(self):
        x_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="Array-like or int",
        )
        super().__init__("permutation", x_pin)

    def apply_function(self, x, **kwargs) -> Any:
        return np.random.permutation(x)
