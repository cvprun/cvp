# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class LinalgCholeskyNode(NumpyFunctionNode):
    """Compute the Cholesky decomposition of a matrix."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Hermitian positive-definite matrix",
        )
        super().__init__("cholesky", array_pin)

    def apply_function(self, a, **kwargs) -> Any:
        return np.linalg.cholesky(a)
