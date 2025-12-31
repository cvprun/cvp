# -*- coding: utf-8 -*-

from typing import Any

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class LinalgPinvNode(NumpyFunctionNode):
    """Compute the (Moore-Penrose) pseudo-inverse of a matrix."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Matrix to be pseudo-inverted",
        )
        rcond_pin = DataInputPin(
            name=PinName("rcond"),
            dtype=Dtype.any(),
            docs="Cutoff for small singular values",
            default=1e-15,
        )
        super().__init__("pinv", array_pin, rcond_pin)

    def apply_function(self, a, rcond, **kwargs) -> Any:
        return np.linalg.pinv(a, rcond=rcond)
