# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class CovNode(NumpyFunctionNode):
    """Estimate a covariance matrix, given data and weights."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("m"),
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
        bias_pin = DataInputPin(
            name=PinName("bias"),
            dtype=Dtype.any(),
            docs="Default normalization (False) is by (N-1)",
            default=False,
        )
        ddof_pin = DataInputPin(
            name=PinName("ddof"),
            dtype=Dtype.any(),
            docs="Delta degrees of freedom",
            default=None,
        )
        super().__init__("cov", array_pin, y_pin, rowvar_pin, bias_pin, ddof_pin)

    def apply_function(self, m, y, rowvar, bias, ddof, **kwargs) -> Any:
        return np.cov(m, y=y, rowvar=rowvar, bias=bias, ddof=ddof)
