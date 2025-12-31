# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class CorrcoefNode(NumpyFunctionNode):
    """Return Pearson product-moment correlation coefficients."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="A 1-D or 2-D array containing multiple variables and observations",
        )
        y_pin = DataInputPin(
            name=PinName("y"),
            dtype=Dtype.any(),
            docs="An additional set of variables and observations",
            default=None,
        )
        rowvar_pin = DataInputPin(
            name=PinName("rowvar"),
            dtype=Dtype.any(),
            docs="If True, then each row represents a variable",
            default=True,
        )
        super().__init__("corrcoef", array_pin, y_pin, rowvar_pin)

    def apply_function(self, x, y, rowvar, **kwargs) -> Any:
        return np.corrcoef(x, y=y, rowvar=rowvar)
