# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomGammaNode(NumpyFunctionNode):
    """Draw samples from a Gamma distribution."""

    def __init__(self):
        shape_pin = DataInputPin(
            name=PinName("shape"),
            dtype=Dtype.any(),
            docs="Parameter of the distribution",
        )
        scale_pin = DataInputPin(
            name=PinName("scale"),
            dtype=Dtype.any(),
            docs="Scale parameter of the distribution",
            default=1.0,
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("gamma", shape_pin, scale_pin, size_pin)

    def apply_function(self, shape, scale, size, **kwargs) -> Any:
        return np.random.gamma(shape=shape, scale=scale, size=size)
