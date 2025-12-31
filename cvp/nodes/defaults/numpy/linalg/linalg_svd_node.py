# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class LinalgSvdNode(NumpyFunctionNode):
    """Singular Value Decomposition."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Array to decompose",
        )
        full_matrices_pin = DataInputPin(
            name=PinName("full_matrices"),
            dtype=Dtype.any(),
            docs="If True, U and Vh are of shape (M, M) and (N, N)",
            default=True,
        )
        compute_uv_pin = DataInputPin(
            name=PinName("compute_uv"),
            dtype=Dtype.any(),
            docs="Whether to compute U and Vh in addition to s",
            default=True,
        )
        super().__init__("svd", array_pin, full_matrices_pin, compute_uv_pin)

    def apply_function(self, a, full_matrices, compute_uv, **kwargs) -> Any:
        return np.linalg.svd(a, full_matrices=full_matrices, compute_uv=compute_uv)
