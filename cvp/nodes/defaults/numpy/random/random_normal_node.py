# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomNormalNode(NumpyFunctionNode):
    """Draw random samples from a normal (Gaussian) distribution."""

    def __init__(self):
        loc_pin = DataInputPin(
            name=PinName("loc"),
            dtype=Dtype.any(),
            docs="Mean of the distribution",
            default=0.0,
        )
        scale_pin = DataInputPin(
            name=PinName("scale"),
            dtype=Dtype.any(),
            docs="Standard deviation of the distribution",
            default=1.0,
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("normal", loc_pin, scale_pin, size_pin)

    def apply_function(self, loc, scale, size, **kwargs) -> Any:
        return np.random.normal(loc=loc, scale=scale, size=size)
