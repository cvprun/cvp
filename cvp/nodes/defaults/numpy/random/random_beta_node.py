# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomBetaNode(NumpyFunctionNode):
    """Draw samples from a Beta distribution."""

    def __init__(self):
        a_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Alpha parameter",
        )
        b_pin = DataInputPin(
            name=PinName("b"),
            dtype=Dtype.any(),
            docs="Beta parameter",
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("beta", a_pin, b_pin, size_pin)

    def apply_function(self, a, b, size, **kwargs) -> Any:
        return np.random.beta(a=a, b=b, size=size)
