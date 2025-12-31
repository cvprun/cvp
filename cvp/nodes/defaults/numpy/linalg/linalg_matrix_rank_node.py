# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class LinalgMatrixRankNode(NumpyFunctionNode):
    """Return matrix rank using SVD method."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("M"),
            dtype=Dtype.any(),
            docs="Input matrix",
        )
        tol_pin = DataInputPin(
            name=PinName("tol"),
            dtype=Dtype.any(),
            docs="Threshold below which SVD values are considered zero",
            default=None,
        )
        super().__init__("matrix_rank", array_pin, tol_pin)

    def apply_function(self, M, tol, **kwargs) -> Any:
        return np.linalg.matrix_rank(M, tol=tol)
