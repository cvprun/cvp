# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class RandomChisquareNode(NumpyFunctionNode):
    """Draw samples from a chi-square distribution."""

    def __init__(self):
        df_pin = DataInputPin(
            name=PinName("df"),
            dtype=Dtype.any(),
            docs="Number of degrees of freedom",
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("chisquare", df_pin, size_pin)

    def apply_function(self, df, size, **kwargs) -> Any:
        return np.random.chisquare(df=df, size=size)
