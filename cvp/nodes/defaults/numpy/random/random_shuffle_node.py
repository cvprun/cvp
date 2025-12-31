# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomShuffleNode(NumpyFunctionNode):
    """Modify a sequence in-place by shuffling its contents."""

    def __init__(self):
        x_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="The array or list to be shuffled",
        )
        super().__init__("shuffle", x_pin)

    def apply_function(self, x, **kwargs) -> Any:
        x_copy = x.copy() if hasattr(x, "copy") else list(x)
        np.random.shuffle(x_copy)
        return x_copy
