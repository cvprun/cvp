# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomRandNode(NumpyFunctionNode):
    """Random values in a given shape."""

    def __init__(self):
        d_pin = DataInputPin(
            name=PinName("d0"),
            dtype=Dtype.any(),
            docs="First dimension",
            default=None,
        )
        super().__init__("rand", d_pin)

    def apply_function(self, d0, **kwargs) -> Any:
        if d0 is None:
            return np.random.rand()
        elif isinstance(d0, (list, tuple)):
            return np.random.rand(*d0)
        else:
            return np.random.rand(d0)
