# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class IsscalarNode(NumpyFunctionNode):
    """Returns True if the type of num is a scalar type."""

    def __init__(self):
        num_pin = DataInputPin(
            name=PinName("num"),
            dtype=Dtype.any(),
            docs="Input argument",
        )
        super().__init__("isscalar", num_pin)

    def apply_function(self, num, **kwargs) -> Any:
        return np.isscalar(num)
